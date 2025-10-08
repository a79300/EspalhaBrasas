# 🎮 Discord Bot - Valorant Stats & LFG

Bot de Discord em Python com funcionalidades para consultar estatísticas de Valorant, procurar jogadores para ranked e verificar a rotação de mapas competitivos.

## 📋 Funcionalidades

- **📊 Estatísticas de Valorant**: Consulta stats detalhadas de jogadores (Competitive/Premier)
- **🎯 Sistema LFG (Looking For Group)**: Procura jogadores para jogar ranked
- **🗺️ Rotação de Mapas**: Mostra os mapas atualmente em rotação no competitivo
- **🤖 Comandos Slash**: Interface moderna com comandos `/`

## 🛠️ Tecnologias

- **Python 3.8+**
- **discord.py** - Biblioteca para Discord
- **aiohttp** - Requisições HTTP assíncronas
- **BeautifulSoup4** - Web scraping
- **python-dotenv** - Gestão de variáveis de ambiente

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/a79300/EspalhaBrasas.git
cd discord-bot
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Crie um ficheiro `.env` na raiz do projeto:

```env
DISCORD_TOKEN=seu_token_do_discord_aqui
HENRIK_API_KEY=sua_chave_api_henrik_aqui
```

#### Como obter as chaves:

**Discord Token:**
1. Aceda ao [Discord Developer Portal](https://discord.com/developers/applications)
2. Crie uma nova aplicação
3. Vá em "Bot" e clique em "Add Bot"
4. Copie o token em "Token"

**Henrik API Key:**
1. Entre no servidor Discord: [discord.gg/X3GaVkX2YN](https://discord.gg/X3GaVkX2YN)
2. Siga as instruções para obter a chave gratuita da API

### 4. Execute o bot

```bash
python main.py
```

Se tudo correr bem, verá a mensagem:
```
[Nome do Bot] está online!
Sincronizados X comandos slash
```

## 📖 Comandos

### `/stats [game_mode] [player]`
Obtém as estatísticas de Valorant de um jogador.

**Parâmetros:**
- `game_mode`: Escolha entre `competitive` ou `premier`
- `player`: Nome do jogador no formato `nome#TAG`

**Exemplos:**
```
/stats competitive Player#1234
/stats premier TenZ#NA1
```

**Informações mostradas:**
- Rank atual com emoji
- K/D ratio (últimos 20 jogos)
- Headshot % médio
- Win rate
- Dano médio por round
- Histórico das últimas 5 partidas

---

### `/ranked [game_name] [horario]`
Cria uma sessão para procurar jogadores para jogar ranked.

**Parâmetros:**
- `game_name`: Nome do jogo (ex: Valorant, CS2, League of Legends)
- `horario`: *(Opcional)* Hora do jogo no formato `HH:MM`

**Exemplos:**
```
/ranked Valorant 20:30
/ranked CS2
```

**Funcionalidades:**
- Sistema de votação com botões
- Máximo de 5 jogadores
- Auto-finalização quando atingir 5 jogadores
- Countdown automático (atualiza a cada 60s)
- Mostra avatares dos participantes
- Se não especificar hora: votação dura 1 hora
- Com hora especificada: votação termina 5 min antes

---

### `/ranked-cancel`
Cancela a sua sessão de procura de jogadores ativa.

**Exemplo:**
```
/ranked-cancel
```

---

### `/maps`
Mostra os mapas atualmente em rotação no Valorant competitivo.

**Exemplo:**
```
/maps
```

**Informações mostradas:**
- Número do patch atual
- Lista dos 7 mapas em rotação
- Fonte dos dados (thespike.gg)

---

### `/help`
Mostra a lista de todos os comandos disponíveis.

**Exemplo:**
```
/help
```

## 🗂️ Estrutura do Projeto

```
discord-bot/
├── commands/
│   ├── help.py          # Comando /help
│   ├── stats.py         # Comando /stats (Valorant)
│   ├── lfg.py           # Comandos /ranked e /ranked-cancel
│   └── maps.py          # Comando /maps
├── events/
│   └── error.py         # Tratamento de erros
├── utils/
│   └── valorant_stats.py # Funções auxiliares para stats
├── main.py              # Ponto de entrada do bot
├── requirements.txt     # Dependências Python
├── .env                 # Variáveis de ambiente (não incluído no git)
├── .gitignore          # Ficheiros ignorados pelo git
└── README.md           # Este ficheiro
```

## 🔧 Configuração Avançada

### Permissões do Bot

No Discord Developer Portal, em "Bot" > "Privileged Gateway Intents", ative:
- ✅ Message Content Intent
- ✅ Server Members Intent (opcional)

### Convite do Bot

URL de convite (substitua `YOUR_CLIENT_ID`):
```
https://discord.com/oauth2/authorize?client_id=1425209969971695638&permissions=8&integration_type=0&scope=bot+applications.commands
```

Permissões necessárias:
- Send Messages
- Embed Links
- Read Message History
- Use Slash Commands
- Add Reactions

## 🐛 Resolução de Problemas

### "Module not found"
Certifique-se de que instalou todas as dependências:
```bash
pip install -r requirements.txt
```

### "Invalid token"
Verifique se o `DISCORD_TOKEN` no ficheiro `.env` está correto.

### "Player not found"
- Certifique-se de usar o formato correto: `nome#TAG`
- A TAG tem 1-6 caracteres
- Verifique se o jogador existe no Valorant

### "/stats não funciona"
- Verifique se a `HENRIK_API_KEY` está configurada corretamente
- A API pode estar temporariamente indisponível

### "/maps não mostra mapas"
- O site thespike.gg pode estar temporariamente indisponível
- Verifique a conexão à internet

## 📝 Notas

- **API Henrik**: Gratuita com rate limits. Para uso intensivo, considere upgrade.
- **Web Scraping**: O comando `/maps` depende da estrutura do site thespike.gg. Se mudarem o site, pode ser necessário atualizar o código.
- **Emojis de Rank**: Os emojis customizados estão configurados para um servidor específico. Para usar noutro servidor, atualize os IDs em `valorant_stats.py`.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Submeter pull requests

## 📄 Licença

Este projeto é open-source e está disponível sob a licença MIT.

## 🔗 Links Úteis

- [Discord.py Documentação](https://discordpy.readthedocs.io/)
- [Henrik Valorant API](https://discord.gg/X3GaVkX2YN)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [TheSpike.gg](https://www.thespike.gg/valorant/maps/map-pool)

## ✨ Autor

Desenvolvido por [YangSafe](https://github.com/a79300)

---

**⚠️ Aviso Legal**: Este bot não é afiliado com a Riot Games. Valorant é uma marca registada da Riot Games, Inc.
