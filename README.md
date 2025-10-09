# 🎮 Discord Bot - Valorant Stats & LFG

Bot de Discord em Python com funcionalidades para consultar estatísticas de Valorant, procurar jogadores para ranked e verificar a rotação de mapas competitivos.

## 📋 Funcionalidades

- **📊 Estatísticas de Valorant**: 
  - `/stats` - Consulta stats detalhadas (Competitive/Premier) com histórico de partidas
- **🎯 Sistema LFG (Looking For Group)**: 
  - `/ranked` - Procura jogadores para jogar ranked (sistema de votação com botões)
  - `/ranked-cancel` - Cancela a sessão LFG ativa
- **🗺️ Rotação de Mapas**: 
  - `/maps` - Mostra os 7 mapas atualmente em rotação no competitivo
- **🎮 VLR.gg Matches**: 
  - `/vlr` - Mostra jogos profissionais de Valorant (finalizados, ao vivo e próximos)
- **❓ Ajuda**: 
  - `/help` - Lista todos os comandos disponíveis
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
cd EspalhaBrasas
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
Obtém as estatísticas de Valorant de um jogador com informações detalhadas.

**Parâmetros:**
- `game_mode`: Escolha entre `competitive` ou `premier`
- `player`: Nome do jogador no formato `nome#TAG`

**Exemplos:**
```
/stats competitive Player#1234
/stats premier TenZ#NA1
```

**Informações mostradas:**
- Rank atual com emoji customizado
- Nível da conta
- K/D ratio (calculado dos últimos 20 jogos)
- Headshot % médio
- Win rate (%) com recorde W-L
- Dano médio por round
- Agente mais jogado (com ícone)
- Histórico das últimas 5 partidas com:
  - Resultado (✅/❌)
  - Mapa jogado
  - Agente usado
  - Placar final
  - KDA (Kills/Deaths/Assists)
  - K/D ratio da partida
- Card do jogador (banner grande)
- Logo do Valorant no rodapé
- Link para tracker.gg

---

### `/ranked [game_name] [horario]`
Cria uma sessão para procurar jogadores para jogar ranked com sistema de votação interativo.

**Parâmetros:**
- `game_name`: Nome do jogo (ex: Valorant, CS2, League of Legends)
- `horario`: *(Opcional)* Hora do jogo no formato `HH:MM`

**Exemplos:**
```
/ranked Valorant 20:30
/ranked CS2
```

**Funcionalidades:**
- Sistema de votação com botões "Juntar-me"
- Máximo de 5 jogadores
- Auto-finalização quando atingir 5 jogadores
- Countdown automático (atualiza a cada 60s)
- Mostra avatares dos participantes
- Se não especificar hora: votação dura 1 hora
- Com hora especificada: votação termina 5 min antes do horário

---

### `/ranked-cancel`
Cancela a sua sessão de procura de jogadores ativa.

**Exemplo:**
```
/ranked-cancel
```

**Funcionalidades:**
- Remove a mensagem de procura
- Liberta o slot para nova sessão
- Confirmação de cancelamento

---

### `/maps`
Mostra os mapas atualmente em rotação no Valorant competitivo com visual melhorado.

**Exemplo:**
```
/maps
```

**Informações mostradas:**
- **Logo do Valorant** (thumbnail no canto superior direito)
- **Patch atual** do jogo
- **Lista dos 7 mapas em rotação** com emojis temáticos:
  - 🏛️ **Ascent** - Itália
  - 🏜️ **Bind** - Marrocos
  - 🏯 **Haven** - Butão
  - ❄️ **Icebox** - Rússia
  - 🏝️ **Breeze** - Caribe
  - ⚡ **Fracture** - Novo México
  - 🌊 **Pearl** - Lisboa
  - 🪷 **Lotus** - Índia
  - 🌅 **Sunset** - Los Angeles
  - 🕳️ **Abyss** - Desconhecido
- Fonte dos dados: [thespike.gg](https://www.thespike.gg/valorant/maps/map-pool)
- Cor temática do Valorant (vermelho #FF4655)

---

### `/vlr`
Mostra os jogos de Valorant profissionais de hoje do VLR.gg com categorização por status e informações detalhadas.

**Exemplo:**
```
/vlr
```

**Informações mostradas:**

**🔴 Jogos Finalizados** (até 5 mais recentes):
- Placar final completo
- Times com bandeiras das regiões (emojis 🇧🇷🇺🇸🇪🇺🇰🇷🇯🇵 etc.)
- Nome do evento/torneio
- Fase da competição (Playoffs, Finals, etc.)
- Link direto para página do jogo no VLR.gg

**🟠 Jogos Ao Vivo** (todos os jogos em andamento):
- Placar atual em tempo real
- Status "LIVE" destacado
- Times participantes com bandeiras
- Informações do torneio
- Link para acompanhar ao vivo

**🟢 Jogos Próximos** (até 5 próximos):
- Tempo até o início (ex: "11h 51m", "2h 30m")
- Times confirmados com bandeiras
- Horário previsto
- Detalhes do evento
- Link para mais informações

**Características:**
- Atualização em tempo real via web scraping
- Emojis de bandeiras automáticos para identificar regiões
- Contador de jogos por categoria no título
- Cores temáticas do Valorant (#FF4655)
- Layout organizado com separação visual (espaçamento) entre jogos
- Sem informações redundantes ou labels repetitivos

**Fontes de dados:**
- [vlr.gg/matches](https://www.vlr.gg/matches) - Jogos ao vivo e próximos
- [vlr.gg/matches/results](https://www.vlr.gg/matches/results) - Jogos finalizados hoje

---

### `/help`
Mostra a lista de todos os comandos disponíveis com descrições.

**Exemplo:**
```
/help
```

**Informações mostradas:**
- Lista completa de comandos
- Breve descrição de cada comando
- Emoji representativo
- Cor temática do Valorant

---

## 🗂️ Estrutura do Projeto

```
EspalhaBrasas/
├── commands/
│   ├── help.py          # Comando /help - Lista todos os comandos
│   ├── stats.py         # Comando /stats - Estatísticas Valorant (Competitive/Premier)
│   ├── valorant.py      # Comando /ranked - Estatísticas competitivas de Valorant
│   ├── lfg.py           # Comandos /ranked e /ranked-cancel - Sistema LFG
│   ├── maps.py          # Comando /maps - Rotação de mapas competitivos
│   └── vlr.py           # Comando /vlr - Jogos profissionais do VLR.gg
├── events/
│   └── error.py         # Tratamento global de erros
├── utils/
│   └── valorant_stats.py # Funções auxiliares para estatísticas
├── main.py              # Ponto de entrada do bot
├── requirements.txt     # Dependências Python
├── .env                 # Variáveis de ambiente (não incluído no git)
├── .env.example         # Exemplo de configuração
├── .gitignore           # Ficheiros ignorados pelo git
├── README.md            # Este ficheiro
├── PRIVACY_POLICY.md    # Política de privacidade
└── TERMS_OF_SERVICE.md  # Termos de serviço
```

### Descrição dos Módulos

#### `commands/`
Contém todos os comandos slash do bot organizados por funcionalidade:

- **`help.py`**: Sistema de ajuda que lista todos os comandos disponíveis
- **`stats.py`**: Integração com Henrik API para estatísticas detalhadas de jogadores
- **`valorant.py`**: Comandos relacionados com estatísticas competitivas
- **`lfg.py`**: Sistema Looking For Group com votações interativas
- **`maps.py`**: Web scraping de thespike.gg para rotação de mapas
- **`vlr.py`**: Web scraping de vlr.gg para jogos profissionais

#### `events/`
Handlers de eventos do Discord:

- **`error.py`**: Tratamento centralizado de erros com mensagens user-friendly

#### `utils/`
Funções auxiliares reutilizáveis:

- **`valorant_stats.py`**: Lógica de busca e formatação de estatísticas

---

## 🔧 Configuração Avançada

### Permissões do Bot

No Discord Developer Portal, em "Bot" > "Privileged Gateway Intents", ative:
- ✅ **Message Content Intent** (necessário para ler conteúdo de mensagens)
- ✅ **Server Members Intent** (opcional, para funcionalidades futuras)

### Convite do Bot

URL de convite (substitua `YOUR_CLIENT_ID` pelo ID da sua aplicação):
```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&integration_type=0&scope=bot+applications.commands
```

Ou use o link específico para este bot:
```
https://discord.com/oauth2/authorize?client_id=1425209969971695638&permissions=8&integration_type=0&scope=bot+applications.commands
```

**Permissões necessárias:**
- ✅ Send Messages
- ✅ Embed Links
- ✅ Read Message History
- ✅ Use Slash Commands
- ✅ Add Reactions
- ✅ Attach Files (para futuros recursos)

---

## 🐛 Resolução de Problemas

### "Module not found"
**Causa:** Dependências não instaladas

**Solução:**
```bash
pip install -r requirements.txt
```

Se persistir, tente:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

### "Invalid token"
**Causa:** Token do Discord incorreto ou ausente

**Solução:**
1. Verifique se o ficheiro `.env` existe na raiz do projeto
2. Confirme que `DISCORD_TOKEN=` está preenchido
3. Regenere o token no Discord Developer Portal se necessário

---

### "Player not found" (comando /stats)
**Causas possíveis:**
- Formato incorreto do nome
- Jogador não existe
- TAG inválida

**Soluções:**
- Use o formato exato: `nome#TAG` (ex: `Player#1234`)
- A TAG tem entre 1-6 caracteres
- Verifique o nome no jogo Valorant
- Certifique-se que o jogador já jogou partidas ranked

---

### "/stats não funciona"
**Causas possíveis:**
- API Henrik indisponível
- Chave API inválida
- Rate limit excedido

**Soluções:**
1. Verifique se `HENRIK_API_KEY` está configurada no `.env`
2. Teste a API: [Henrik API Status](https://discord.gg/X3GaVkX2YN)
3. Aguarde alguns minutos se atingiu o rate limit
4. Verifique logs no terminal para erros específicos

---

### "/maps não mostra mapas"
**Causas possíveis:**
- Site thespike.gg indisponível
- Mudança na estrutura HTML do site
- Problema de conexão

**Soluções:**
1. Acesse [thespike.gg](https://www.thespike.gg/valorant/maps/map-pool) no navegador
2. Verifique conexão à internet
3. Se o site mudou, pode ser necessário atualizar os selectores CSS em `maps.py`

---

### "/vlr não mostra jogos"
**Causas possíveis:**
- Site vlr.gg indisponível
- Mudança na estrutura HTML
- Não há jogos agendados para hoje

**Soluções:**
1. Verifique se há jogos em [vlr.gg/matches](https://www.vlr.gg/matches)
2. Aguarde alguns minutos e tente novamente
3. Se persistir, a estrutura HTML pode ter mudado (atualizar selectores em `vlr.py`)

---

### Bandeiras não aparecem (comando /vlr)
**Causa:** Discord não reconhece o código do país

**Informação:** As bandeiras são emojis padrão do Discord (🇧🇷🇺🇸🇪🇺). Se não aparecem, pode ser:
- Código de país inválido no HTML do VLR.gg
- Problema de renderização do Discord

---

### Bot não responde a comandos
**Soluções:**
1. Verifique se o bot está online (status verde no Discord)
2. Confirme que os comandos foram sincronizados (mensagem no terminal ao iniciar)
3. Verifique permissões do bot no servidor
4. Tente `/help` para testar

---

## 📝 Notas Importantes

### API Henrik
- **Gratuita** com rate limits (60 requests/minuto)
- Para uso intensivo, considere upgrade para plano pago
- Dados atualizados automaticamente pela Riot Games API
- Suporta todas as regiões (EU, NA, ASIA, BR, LATAM, KR)

### Web Scraping
- Os comandos `/maps` e `/vlr` dependem da estrutura HTML dos sites
- Se os sites mudarem, pode ser necessário atualizar os selectores CSS
- Use com moderação para não sobrecarregar os servidores

### Emojis Customizados
- Os emojis de rank (`<:radiant:123>`) são específicos de um servidor
- Para usar noutro servidor, atualize os IDs em `utils/valorant_stats.py`
- Linha 32-64 do ficheiro `valorant_stats.py`

### Performance
- Comandos de web scraping (`/maps`, `/vlr`) podem demorar 2-5 segundos
- Use `defer()` para evitar timeout do Discord
- Cache pode ser implementado para melhorar performance

---

## 🤝 Contribuições

Contribuições são muito bem-vindas! Aqui está como você pode ajudar:

### Como Contribuir

1. **Fork** o repositório
2. Crie uma **branch** para sua feature (`git checkout -b feature/MinhaFeature`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. **Push** para a branch (`git push origin feature/MinhaFeature`)
5. Abra um **Pull Request**

### Ideias para Contribuir

- 🐛 Reportar bugs
- ✨ Sugerir novas funcionalidades
- 📝 Melhorar documentação
- 🎨 Melhorar interface dos embeds
- ⚡ Otimizar performance
- 🌍 Adicionar suporte para mais idiomas

### Diretrizes

- Siga o estilo de código existente
- Comente código complexo
- Teste suas mudanças antes de submeter
- Atualize o README se necessário

---

## 📄 Licença

Este projeto é **open-source** e está disponível sob a [Licença MIT](LICENSE).

Você é livre para:
- ✅ Usar comercialmente
- ✅ Modificar
- ✅ Distribuir
- ✅ Uso privado

**Condições:**
- Incluir a licença original
- Dar crédito ao autor original

---

## 🔗 Links Úteis

### Documentação
- [Discord.py Documentação Oficial](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Guia Discord.py 2.0](https://discordpy.readthedocs.io/en/stable/migrating.html)

### APIs e Serviços
- [Henrik Valorant API](https://discord.gg/X3GaVkX2YN) - Discord para obter chave
- [Valorant API (Unofficial)](https://valorant-api.com/) - Assets e dados do jogo
- [TheSpike.gg](https://www.thespike.gg/valorant/maps/map-pool) - Rotação de mapas
- [VLR.gg](https://www.vlr.gg/matches) - Esports e torneios

### Ferramentas
- [BeautifulSoup4 Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [aiohttp Docs](https://docs.aiohttp.org/)
- [Python dotenv](https://pypi.org/project/python-dotenv/)

---

## ✨ Autor

Desenvolvido com ❤️ por **[YangSafe](https://github.com/a79300)**

- GitHub: [@a79300](https://github.com/a79300)
- Repositório: [EspalhaBrasas](https://github.com/a79300/EspalhaBrasas)

---

## 🙏 Agradecimentos

- **Riot Games** - Por criar Valorant
- **Henrik-3** - Por disponibilizar a API gratuita
- **Discord.py** - Pela excelente biblioteca
- **Comunidade** - Por todo o feedback e suporte

---

## 📊 Status do Projeto

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Última atualização:** Janeiro 2025

---

## ⚠️ Aviso Legal

Este bot **não é afiliado, associado, autorizado ou endossado** pela Riot Games, Inc.

**Valorant** é uma marca registada da **Riot Games, Inc.**

Todos os assets, imagens e dados do jogo pertencem aos seus respectivos proprietários.

Este projeto é para fins **educacionais e de entretenimento** apenas.

---

<div align="center">

### 🎮 Feito para a comunidade de Valorant 🎮

**Se este projeto te ajudou, considere dar uma ⭐ no repositório!**

</div>
