<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Brasao_do_Sao_Paulo_Futebol_Clube.svg/2054px-Brasao_do_Sao_Paulo_Futebol_Clube.svg.png" width="100px" alt="Logo SPFC">
  <h1>Bot de Agenda de Jogos do São Paulo</h1>
  <p>Um bot em Python que automatiza a criação de eventos no seu Google Calendar para os jogos do Tricolor!</p>
  
  <p>
    <a href="https://opensource.org/licenses/MIT">
      <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
    </a>
    <img src="https://img.shields.io/badge/Python-3.7+-blue.svg" alt="Python Version">
  </p>
</div>

<div align="center">
  <h3>Competições Suportadas</h3>
  <img src="https://i.namu.wiki/i/ERiBtFg1CI8uCA2WQjlo25QR7pHAP6KPE271lVupZxa3AvVq_uvexbiMIZD-UYUPkGwF1dCmiLqsA5wQ0XQYzQ.webp" width="100px" alt="Logo Libertadores">
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://www.ogol.com.br/img/logos/competicoes/51_imgbank_d1_20250313102859.png" width="100px" alt="Logo Brasileirão">
</div>

<br>

Este projeto verifica automaticamente os próximos jogos do São Paulo Futebol Clube e cria eventos detalhados na sua agenda do Google. Ideal para nunca mais perder uma partida importante!

*Caso queira, é possível alterar o time e as competições facilmente no arquivo `config.json`. Os IDs necessários podem ser encontrados na documentação da API Football-data.*

---

## Sumário

- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Obtenção das Chaves de API](#obtenção-das-chaves-de-api)
- [Configuração do Projeto](#configuração-do-projeto)
- [Executando o Bot](#executando)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Funcionalidades

- **Busca de Jogos**: Conecta-se à API da [football-data.org](https://www.football-data.org/) para encontrar jogos agendados.
- **Agenda Inteligente**: Cria eventos no Google Calendar para cada jogo, evitando a criação de eventos duplicados.
- **Notificações**: Envia notificações via [Pushbullet](https://www.pushbullet.com/) quando um novo jogo é adicionado à agenda (opcional).
- **Altamente Configurável**: Todas as chaves de API, IDs e preferências são gerenciadas em um único arquivo `config.json`.

## Tecnologias Utilizadas

<p align="left">
  <a href="https://www.python.org" target="_blank" rel="noreferrer">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="30" height="30"/>
  </a>
  <a href="https://developers.google.com/calendar" target="_blank" rel="noreferrer">
    <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/google/google-original.svg" alt="google" width="30" height="30"/>
  </a>
</p>

- **Linguagem**: Python 3.7+
- **APIs Externas**:
  - [API-Football (football-data.org)](https://www.football-data.org/)
  - [Google Calendar API](https://developers.google.com/calendar/api/guides/overview)
  - [Pushbullet API](https://www.pushbullet.com/)
- **Bibliotecas Python**: `requests`, `google-api-python-client`, `google-auth-oauthlib`, `pytz`.

## Pré-requisitos

- [Python 3.7](https://www.python.org/downloads/) ou superior instalado.
- Uma conta no Google para usar a Agenda.
- Conta no [football-data.org](https://www.football-data.org/) (o plano gratuito é suficiente para ligas europeias).
- Conta no [Pushbullet](https://www.pushbullet.com/) (opcional, para notificações).

## Instalação

1. **Clone o repositório:**

    ```bash
    git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git
    cd SEU-REPOSITORIO
    ```

2. **Crie e ative um ambiente virtual (recomendado):**

    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3. **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

## Obtenção das Chaves de API

Para que o bot funcione, você precisa obter chaves de API para os serviços que ele utiliza.

### 1. API-Football

1. Acesse [football-data.org](https://www.football-data.org/client/register) e registre-se.
2. Após o login, copie sua chave na seção "API Key" do seu perfil.

### 2. Google Calendar API

É necessário criar uma "Conta de Serviço" que dará ao script permissão para gerenciar seus eventos.

1. **Acesse o Google Cloud Console**: Vá para [https://console.cloud.google.com/](https://console.cloud.google.com/).
2. **Crie um Novo Projeto** e **ative a API do Google Calendar** para ele.
3. **Crie uma Conta de Serviço**:
    - Vá para **APIs e serviços > Credenciais > CRIAR CREDENCIAIS > Conta de serviço**.
    - Siga os passos e, ao final, gere uma **nova chave do tipo JSON**.
    - Guarde este arquivo `.json` em um local seguro.
4. **Compartilhe sua Agenda do Google**:
    - Nas configurações da sua agenda, encontre o e-mail da conta de serviço criada.
    - Adicione este e-mail à lista de compartilhamento com a permissão **"Fazer alterações nos eventos"**.

### 3. Pushbullet

1. Acesse [Pushbullet.com](https://www.pushbullet.com/).
2. Em **Settings > Account**, crie um **Access Token** e copie o valor.

## Configuração do Projeto

Crie um arquivo `config.json` na raiz do projeto e preencha com suas chaves e preferências.

```json
{
  "api_football": {
    "token": "SUA_CHAVE_DA_API_FOOTBALL_DATA_AQUI"
  },
  "google_calendar": {
    "service_account_file": "caminho/para/o/seu-arquivo-de-credenciais.json",
    "calendar_id": "seu-id-de-calendario@group.calendar.google.com"
  },
  "pushbullet": {
    "access_token": "SEU_TOKEN_DO_PUSHBULLET_AQUI"
  },
  "team_settings": {
    "team_id": 126,
    "team_name": "São Paulo FC",
    "competitions": [
      2013,
      2152
    ]
  },
  "event_settings": {
    "title": "Jogo do SP",
    "duration_hours": 2,
    "reminder_minutes": 30,
    "color_id": "11"
  }
}
````

## Executando

Com tudo configurado, basta executar o script no seu terminal:

```bash
python jogos_sp_agenda.py
```

Você pode automatizar a execução deste script usando `cron` (Linux/macOS) ou Agendador de Tarefas (Windows).

## Contribuição

Contribuições são bem-vindas\! Se você tiver ideias para novas funcionalidades ou encontrar um bug, sinta-se à vontade para:

1. Fazer um **Fork** do projeto.

2. Criar uma nova branch (`git checkout -b feature/sua-feature-incrivel`).

3. Fazer o commit de suas alterações (`git commit -m 'Adiciona sua-feature-incrivel'`).

4. Fazer o push para a branch (`git push origin feature/sua-feature-incrivel`).

5. Abrir um **Pull Request**.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.
