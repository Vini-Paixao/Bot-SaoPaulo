import os
import json
import requests
import logging
from datetime import datetime, timedelta
import pytz
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account

# --- Configuração do logging ---
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# --- Funções de Configuração ---
def load_config():
    """Carrega as configurações do arquivo config.json."""
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            # Validar chaves essenciais
            if "api_football" not in config or "google_calendar" not in config:
                raise ValueError(
                    "Arquivo de configuração inválido. Faltando seções 'api_football' ou 'google_calendar'."
                )
            return config
    except FileNotFoundError:
        logging.error(
            "Arquivo 'config.json' não encontrado. Crie o arquivo com base no exemplo."
        )
        return None
    except json.JSONDecodeError:
        logging.error(
            "Erro ao decodificar o 'config.json'. Verifique a formatação do arquivo."
        )
        return None
    except ValueError as e:
        logging.error(e)
        return None


# Carrega as configurações globais
CONFIG = load_config()

if CONFIG:
    # --- Constantes do Script (carregadas do config.json) ---
    API_TOKEN = CONFIG.get("api_football", {}).get("token")
    BASE_URL = "https://api.football-data.org/v4"
    HEADERS = {"X-Auth-Token": API_TOKEN}

    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    SERVICE_ACCOUNT_FILE = CONFIG.get("google_calendar", {}).get("service_account_file")
    GOOGLE_CALENDAR_ID = CONFIG.get("google_calendar", {}).get("calendar_id")

    EVENT_SETTINGS = CONFIG.get("event_settings", {})
    EVENT_DURATION_HOURS = EVENT_SETTINGS.get("duration_hours", 2)
    REMINDER_MINUTES = EVENT_SETTINGS.get("reminder_minutes", 30)
    EVENT_TITLE = EVENT_SETTINGS.get("title", "Jogo")
    EVENT_COLOR_ID = EVENT_SETTINGS.get("color_id", "1")  # Default color

    PUSHBULLET_TOKEN = CONFIG.get("pushbullet", {}).get("access_token")


# --- Funções de Notificação ---
def send_push_notification(message):
    """Envia uma notificação por Pushbullet se o token estiver configurado."""
    if not PUSHBULLET_TOKEN:
        logging.info("Token do Pushbullet não configurado. Notificação pulada.")
        return

    url = "https://api.pushbullet.com/v2/pushes"
    payload = {
        "type": "note",
        "title": f"🔔 {EVENT_TITLE} - Novo Evento 🔔",
        "body": message,
    }
    headers = {"Access-Token": PUSHBULLET_TOKEN, "Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            logging.info("Notificação Pushbullet enviada com sucesso.")
        else:
            logging.error(f"Erro ao enviar notificação Pushbullet: {response.text}")
    except Exception as e:
        logging.error(f"Exceção ao enviar notificação Pushbullet: {e}")


# --- Função de Autenticação ---
def get_calendar_service():
    """Autentica usando uma Conta de Serviço e retorna o serviço do Google Calendar."""
    if not SERVICE_ACCOUNT_FILE or not os.path.exists(SERVICE_ACCOUNT_FILE):
        logging.error(
            f"Arquivo de conta de serviço '{SERVICE_ACCOUNT_FILE}' não encontrado ou não configurado."
        )
        return None
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = build("calendar", "v3", credentials=creds)
        logging.info("Serviço Google Calendar autenticado com sucesso.")
        return service
    except Exception as e:
        logging.error(
            f"Erro ao carregar credenciais ou construir serviço do Google Calendar: {e}"
        )
        return None


# --- Função para Criar Evento ---
def criar_evento_google_calendar(
    service, start_time_brt, end_time_brt, summary, description, match_api_id
):
    """Cria um evento no Google Calendar se ele ainda não existir."""
    event_unique_id_key = "match_api_id"
    event_search_property = f"{event_unique_id_key}={match_api_id}"

    try:
        logging.info(
            f"Verificando se já existe evento para match_api_id: {match_api_id}"
        )
        events_result = (
            service.events()
            .list(
                calendarId=GOOGLE_CALENDAR_ID,
                privateExtendedProperty=event_search_property,
                maxResults=1,
            )
            .execute()
        )
        if events_result.get("items", []):
            logging.info(
                f"Evento para a partida ID {match_api_id} já existe. Ignorando."
            )
            return

        logging.info(f"Criando evento para a partida ID {match_api_id}...")
        timezone_brt = "America/Sao_Paulo"
        event_body = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_time_brt.isoformat(), "timeZone": timezone_brt},
            "end": {"dateTime": end_time_brt.isoformat(), "timeZone": timezone_brt},
            "reminders": {
                "useDefault": False,
                "overrides": [{"method": "popup", "minutes": REMINDER_MINUTES}],
            },
            "extendedProperties": {"private": {event_unique_id_key: str(match_api_id)}},
            "colorId": EVENT_COLOR_ID,
        }

        created_event = (
            service.events()
            .insert(calendarId=GOOGLE_CALENDAR_ID, body=event_body)
            .execute()
        )
        logging.info(f"Evento criado com sucesso: {created_event.get('htmlLink')}")

        push_message = (
            f"Novo evento: {summary}\nData: {start_time_brt.strftime('%d/%m/%Y %H:%M')}"
        )
        send_push_notification(push_message)

    except HttpError as error:
        logging.error(f"Ocorreu um erro na API do Google Calendar: {error}")
    except Exception as e:
        logging.error(f"Ocorreu um erro inesperado ao criar/verificar evento: {e}")


# --- Funções para Integração com Football Data ---
def obter_nome_competicao(id_competicao):
    """Obtém o nome de uma competição a partir de seu ID."""
    url = f"{BASE_URL}/competitions/{id_competicao}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json().get("name", f"ID {id_competicao}")
    except requests.RequestException as e:
        logging.error(f"Erro ao obter nome da competição {id_competicao}: {e}")
        return f"ID {id_competicao}"


def obter_id_time(nome_time, id_competicao):
    """Obtém o ID e o nome de um time em uma determinada competição."""
    url = f"{BASE_URL}/competitions/{id_competicao}/teams"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        for time in response.json().get("teams", []):
            if time["name"].strip().lower() == nome_time.strip().lower():
                return time["id"], time["name"]
    except requests.RequestException as e:
        logging.error(f"Erro ao obter times da competição {id_competicao}: {e}")
    return None, None


def listar_partidas_semana(
    calendar_service,
    id_seu_time,
    nome_seu_time_api,
    id_competicao,
    data_inicio,
    data_fim,
):
    """Busca partidas agendadas e cria os eventos no Google Calendar."""
    if not calendar_service:
        logging.error(
            "Serviço do Google Calendar indisponível. Não é possível criar eventos."
        )
        return False

    url = f"{BASE_URL}/teams/{id_seu_time}/matches"
    params = {
        "dateFrom": data_inicio,
        "dateTo": data_fim,
        "competitions": id_competicao,
        "status": "SCHEDULED",
    }
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        partidas = response.json().get("matches", [])
        if not partidas:
            return False

        logging.info("-" * 40)
        for partida in partidas:
            match_api_id = partida["id"]
            home_team, away_team = partida["homeTeam"], partida["awayTeam"]
            competicao_info = partida["competition"]
            utc_dt = datetime.strptime(
                partida["utcDate"], "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=pytz.utc)
            brt_dt_start = utc_dt.astimezone(pytz.timezone("America/Sao_Paulo"))
            brt_dt_end = brt_dt_start + timedelta(hours=EVENT_DURATION_HOURS)

            descricao_evento = (
                f"⚽ Partida: {home_team['name']} vs {away_team['name']}\n"
                f"🏆 Competição: {competicao_info.get('name', '')}\n"
                f"📅 Data: {brt_dt_start.strftime('%d/%m/%Y')}\n"
                f"⏰ Hora: {brt_dt_start.strftime('%H:%M')}"
            )
            logging.info(
                f"Jogo Encontrado: {home_team['name']} vs {away_team['name']} em {brt_dt_start.strftime('%d/%m/%Y %H:%M')}"
            )

            criar_evento_google_calendar(
                service=calendar_service,
                start_time_brt=brt_dt_start,
                end_time_brt=brt_dt_end,
                summary=f"{EVENT_TITLE}: {home_team['shortName']} vs {away_team['shortName']}",
                description=descricao_evento,
                match_api_id=str(match_api_id),
            )
        return True
    except requests.RequestException as e:
        logging.error(f"Erro na API football-data ao listar partidas: {e}")
        return False


# --- Bloco Principal ---
def main():
    """Função principal que orquestra a execução do script."""
    if not CONFIG:
        logging.error(
            "Script não pode continuar sem um arquivo de configuração válido."
        )
        return

    logging.info("Iniciando script de busca de jogos e criação de eventos...")
    google_service = get_calendar_service()
    if not google_service:
        logging.error("Falha na autenticação com o Google Calendar. Encerrando script.")
        return

    team_settings = CONFIG.get("team_settings", {})
    nome_time_alvo = team_settings.get("team_name")
    competicoes_ids = team_settings.get("competitions", [])

    if not nome_time_alvo or not competicoes_ids:
        logging.error(
            "Nome do time ou IDs de competições não configurados no 'config.json'."
        )
        return

    hoje_brt = datetime.now(pytz.timezone("America/Sao_Paulo"))
    data_inicio_str = hoje_brt.strftime("%Y-%m-%d")
    data_fim_str = (hoje_brt + timedelta(days=7)).strftime(
        "%Y-%m-%d"
    )  # Busca jogos para os próximos 7 dias

    logging.info(
        f"Buscando jogos para '{nome_time_alvo}' entre {data_inicio_str} e {data_fim_str}..."
    )

    id_time_global, nome_time_api_global = None, None
    encontrou_algum_jogo = False

    for id_comp in competicoes_ids:
        nome_competicao = obter_nome_competicao(id_comp)
        logging.info(f"\nVerificando competição: {nome_competicao} (ID: {id_comp})")

        if not id_time_global:  # Otimização: busca o ID do time apenas uma vez
            id_time_global, nome_time_api_global = obter_id_time(
                nome_time_alvo, id_comp
            )

        if id_time_global:
            jogo_encontrado = listar_partidas_semana(
                google_service,
                id_time_global,
                nome_time_api_global,
                id_comp,
                data_inicio_str,
                data_fim_str,
            )
            if jogo_encontrado:
                encontrou_algum_jogo = True
        else:
            logging.warning(
                f"Time '{nome_time_alvo}' não encontrado na competição '{nome_competicao}'."
            )

    if not encontrou_algum_jogo:
        logging.info(
            f"Nenhum jogo agendado encontrado para '{nome_time_alvo}' nos próximos 7 dias."
        )
    else:
        logging.info("Busca e processamento de eventos finalizados.")


if __name__ == "__main__":
    main()
