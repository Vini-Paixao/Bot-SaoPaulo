# Bot de Agenda de Jogos do São Paulo <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Brasao_do_Sao_Paulo_Futebol_Clube.svg/2054px-Brasao_do_Sao_Paulo_Futebol_Clube.svg.png" width="25px"> - <img align="center" alt="Vini-Python" width="30px" src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Este é um bot em Python que verifica automaticamente os próximos jogos do São Paulo Futebol Clube nas competições: **Libertadores** e **Brasileirão** e cria eventos no seu Google Calendar. Nunca mais perca um jogo!

*Caso queira é possível alterar o Time em questão alterando no arquivo `config.json` o ID do Time que pode ser recuperado da API Football-data ([IDs dos Times](https://dashboard.api-football.com/soccer/ids/teams))*

## Sumário

- [Funcionalidades](https://www.google.com/search?q=%23funcionalidades)
- [Tecnologias Utilizadas](https://www.google.com/search?q=%23tecnologias-utilizadas)
- [Pré-requisitos](https://www.google.com/search?q=%23pr%C3%A9-requisitos)
- [Instalação](https://www.google.com/search?q=%23instala%C3%A7%C3%A3o)
- [Obtenção das Chaves de API](https://www.google.com/search?q=%23obten%C3%A7%C3%A3o-das-chaves-de-api)
  - [1. API-Football (football-data.org)](https://www.google.com/search?q=%231-api-football-football-dataorg)
  - [2. Google Calendar API](https://www.google.com/search?q=%232-google-calendar-api)
  - [3. Pushbullet](https://www.google.com/search?q=%233-pushbullet)
- [Configuração do Projeto](https://www.google.com/search?q=%23configura%C3%A7%C3%A3o-do-projeto)
- [Executando o Bot](https://www.google.com/search?q=%23executando-o-bot)
- [Contribuição](https://www.google.com/search?q=%23contribui%C3%A7%C3%A3o)
- [Licença](https://www.google.com/search?q=%23licen%C3%A7a)

## Funcionalidades

- **Busca de Jogos**: Conecta-se à API da [football-data.org](https://www.football-data.org/) para encontrar jogos agendados.

- **Agenda Inteligente**: Cria eventos no Google Calendar para cada jogo, evitando a criação de eventos duplicados se o jogo já estiver na agenda.

- **Notificações**: Envia notificações via [Pushbullet](https://www.pushbullet.com/) quando um novo jogo é adicionado à agenda (opcional).

- **Altamente Configurável**: Todas as chaves de API, IDs e preferências são gerenciadas em um único arquivo `config.json`, facilitando a personalização.

## Tecnologias Utilizadas

- **Linguagem**: Python 3.7+

- **APIs Externas**:
  - [API-Football (football-data.org)](https://www.football-data.org/)
  - [Google Calendar API](https://developers.google.com/calendar/api/guides/overview)
  - [Pushbullet API](https://www.google.com/search?q=https://docs.pushbullet.com/)

- **Bibliotecas Python**: `requests`, `google-api-python-client`, `google-auth-oauthlib`, `pytz`.

## Pré-requisitos

- [Python 3.7](https://www.python.org/downloads/) ou superior instalado.

- Uma conta no Google para usar a Agenda.

- Conta no [football-data.org](https://www.football-data.org/) (o plano gratuito é suficiente).

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

3. **Instale as dependências a partir do arquivo `requirements.txt`:**

    ```bash
    pip install -r requirements.txt
    ```

    *Se o arquivo `requirements.txt` não existir, crie-o com o seguinte conteúdo:*

    ```text
    google-api-python-client
    google-auth-httplib2
    google-auth-oauthlib
    requests
    pytz
    ```

## Obtenção das Chaves de API

Para que o bot funcione, você precisa obter chaves de API para os serviços que ele utiliza.

### 1\. API-Football (football-data.org)

Esta API fornece os dados sobre os jogos de futebol.

1. Acesse [football-data.org](https://www.football-data.org/client/register) e registre-se para obter uma conta. O nível gratuito ("Tier One") é suficiente para este projeto.
2. Após o login, vá para a sua página de **Perfil (Profile)**.
3. Sua chave de API estará visível na seção "API Key".
4. Copie esta chave. Você a usará no arquivo `config.json`.

### 2\. Google Calendar API

Esta é a parte mais complexa. Vamos criar uma "Conta de Serviço" que dará ao nosso script permissão para gerenciar seus eventos da agenda.

1. **Acesse o Google Cloud Console**: Vá para [https://console.cloud.google.com/](https://console.cloud.google.com/).

2. **Crie um Novo Projeto**: Se você não tiver um, clique em "Selecionar um projeto" na barra superior e depois em "NOVO PROJETO". Dê um nome a ele (ex: "Bot Agenda de Jogos") e clique em "CRIAR".

3. **Ative a API do Google Calendar**:
      - No menu de navegação à esquerda, vá para **APIs e serviços \> Biblioteca**.
      - Procure por "Google Calendar API" e clique nela.
      - Clique no botão **ATIVAR**.

4. **Crie as Credenciais (Conta de Serviço)**:
      - No menu de navegação, vá para **APIs e serviços \> Credenciais**.
      - Clique em **+ CRIAR CREDENCIAIS** e selecione **Conta de serviço**.
      - Dê um nome à sua conta de serviço (ex: `bot-calendario`) e uma descrição. Clique em **CRIAR E CONTINUAR**.
      - Na seção de permissões (Passo 2), não é necessário adicionar um papel. Apenas clique em **CONTINUAR**.
      - Na seção "Conceder aos usuários acesso a esta conta de serviço" (Passo 3), clique em **CONCLUÍDO**.

5. **Gere a Chave da Conta de Serviço**:
      - Na tela de "Credenciais", você verá a conta de serviço que acabou de criar. Clique nela.
      - Vá para a aba **CHAVES**.
      - Clique em **ADICIONAR CHAVE \> Criar nova chave**.
      - Selecione o tipo **JSON** e clique em **CRIAR**.
      - Um arquivo `.json` será baixado para o seu computador. **Guarde este arquivo em um local seguro\!** Este arquivo contém as credenciais que seu script usará.

6. **Compartilhe sua Agenda do Google**:
      - Abra sua [Agenda do Google](https://calendar.google.com/).
      - Encontre o e-mail da sua conta de serviço. Ele está nos detalhes da conta de serviço no Google Cloud Console e se parece com `nome-da-conta@seu-projeto.iam.gserviceaccount.com`.
      - Na sua agenda, encontre o calendário que deseja usar, clique nos três pontos (Opções) e vá para **Configurações e compartilhamento**.
      - Role para baixo até "Compartilhar com pessoas específicas" e clique em **+ Adicionar pessoas**.
      - Cole o e-mail da conta de serviço e, em "Permissões", selecione **Fazer alterações nos eventos**.
      - Clique em **Enviar**.

### 3\. Pushbullet

Serviço opcional para receber notificações no seu celular ou desktop.

1. Acesse [Pushbullet.com](https://www.pushbullet.com/) e faça login com sua conta do Google.

2. Vá para **Settings \> Account**.

3. Role para baixo até a seção **Access Tokens** e clique em **Create Access Token**.

4. Copie o token gerado.

## Configuração do Projeto

Agora que você tem todas as chaves, é hora de configurar o bot.

1. No diretório do projeto, crie um arquivo chamado `config.json`.

2. Copie e cole a estrutura abaixo no seu `config.json` e preencha com as informações que você coletou.

<!-- end list -->

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
```

- **`api_football.token`**: A chave que você obteve do football-data.org.

- **`google_calendar.service_account_file`**: O caminho relativo ou absoluto para o arquivo `.json` que você baixou do Google Cloud.

- **`google_calendar.calendar_id`**: O ID do seu calendário. Para o calendário principal, é seu endereço de e-mail. Para outros, encontre em "Configurações e compartilhamento \> Integrar agenda".

- **`pushbullet.access_token`**: O token que você gerou no Pushbullet. Deixe em branco (`""`) se não quiser usar notificações.

- **`team_settings`**: Personalize com o nome do seu time e os IDs das competições que deseja acompanhar.

- **`event_settings`**: Personalize o título, duração, lembretes e cor dos eventos na agenda.

## Executando o Bot

Com tudo configurado, basta executar o script no seu terminal:

```bash
python jogos_sp_agenda.py
```

Você pode automatizar a execução deste script usando `cron` (Linux/macOS) ou Agendador de Tarefas (Windows) para que ele verifique por novos jogos periodicamente.

## Contribuição

Contribuições são bem-vindas\! Se você tiver ideias para novas funcionalidades ou encontrar um bug, sinta-se à vontade para:

1. Fazer um **Fork** do projeto.

2. Criar uma nova branch (`git checkout -b feature/sua-feature-incrivel`).

3. Fazer o commit de suas alterações (`git commit -m 'Adiciona sua-feature-incrivel'`).

4. Fazer o push para a branch (`git push origin feature/sua-feature-incrivel`).

5. Abrir um **Pull Request**.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE.md](LICENSE.md) para mais detalhes.
