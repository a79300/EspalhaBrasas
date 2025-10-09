# 🎮 Discord Bot - Valorant Stats & LFG

Discord bot in Python with features to check Valorant statistics, find ranked players, and view competitive map rotation.

## 📋 Features

- **📊 Valorant Statistics**: 
  - `/stats` - Query detailed stats (Competitive/Premier) with match history
- **🎯 LFG System (Looking For Group)**: 
  - `/ranked` - Find players for ranked games (voting system with buttons)
  - `/ranked-cancel` - Cancel active LFG session
- **🗺️ Map Rotation**: 
  - `/maps` - Shows the 7 maps currently in competitive rotation
- **🎮 VLR.gg Matches**: 
  - `/vlr` - Shows professional Valorant matches (finished, live and upcoming)
- **❓ Help**: 
  - `/help` - Lists all available commands
- **🤖 Slash Commands**: Modern interface with `/` commands

## 🛠️ Technologies

- **Python 3.8+**
- **discord.py** - Discord library
- **aiohttp** - Asynchronous HTTP requests
- **BeautifulSoup4** - Web scraping
- **python-dotenv** - Environment variables management

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/a79300/EspalhaBrasas.git
cd EspalhaBrasas
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
DISCORD_TOKEN=your_discord_token_here
HENRIK_API_KEY=your_henrik_api_key_here
```

#### How to get the keys:

**Discord Token:**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" and click "Add Bot"
4. Copy the token under "Token"

**Henrik API Key:**
1. Join the Discord server: [discord.gg/X3GaVkX2YN](https://discord.gg/X3GaVkX2YN)
2. Follow the instructions to get a free API key

### 4. Run the bot

```bash
python main.py
```

If everything works fine, you'll see the message:
```
[Bot Name] is online!
Synced X slash commands
```

## 📖 Commands

### `/stats [game_mode] [player]`
Get Valorant player statistics with detailed information.

**Parameters:**
- `game_mode`: Choose between `competitive` or `premier`
- `player`: Player name in `name#TAG` format

**Examples:**
```
/stats competitive Player#1234
/stats premier TenZ#NA1
```

**Information shown:**
- Current rank with custom emoji
- Account level
- K/D ratio (calculated from last 20 games)
- Average Headshot %
- Win rate (%) with W-L record
- Average damage per round
- Most played agent (with icon)
- Last 5 match history with:
  - Result (✅/❌)
  - Map played
  - Agent used
  - Final score
  - KDA (Kills/Deaths/Assists)
  - Match K/D ratio
- Player card (large banner)
- Valorant logo in footer
- Link to tracker.gg

---

### `/ranked [game_name] [time]`
Create a session to find players for ranked games with interactive voting system.

**Parameters:**
- `game_name`: Game name (e.g.: Valorant, CS2, League of Legends)
- `time`: *(Optional)* Game time in `HH:MM` format

**Examples:**
```
/ranked Valorant 20:30
/ranked CS2
```

**Features:**
- Voting system with "Join" and "Leave" buttons
- Maximum of 5 players
- Auto-complete when reaching 5 players
- Automatic countdown (updates every 60s)
- Shows participants' avatars
- Without specified time: voting lasts 1 hour
- With specified time: voting ends 5 min before the time

---

### `/ranked-cancel`
Cancel your active player search session.

**Example:**
```
/ranked-cancel
```

**Features:**
- Removes the search message
- Frees the slot for a new session
- Cancellation confirmation

---

### `/maps`
Shows maps currently in Valorant competitive rotation with improved visuals.

**Example:**
```
/maps
```

**Information shown:**
- **Valorant logo** (thumbnail in top right corner)
- **Current patch** of the game
- **List of 7 maps in rotation** with themed emojis:
  - 🏛️ **Ascent** - Italy
  - 🏜️ **Bind** - Morocco
  - 🏯 **Haven** - Bhutan
  - ❄️ **Icebox** - Russia
  - 🏝️ **Breeze** - Caribbean
  - ⚡ **Fracture** - New Mexico
  - 🌊 **Pearl** - Lisbon
  - 🪷 **Lotus** - India
  - 🌅 **Sunset** - Los Angeles
  - 🕳️ **Abyss** - Unknown
- Data source: [thespike.gg](https://www.thespike.gg/valorant/maps/map-pool)
- Valorant themed color (red #FF4655)

---

### `/vlr`
Shows today's professional Valorant matches from VLR.gg with status categorization and detailed information.

**Example:**
```
/vlr
```

**Information shown:**

**🔴 Finished Matches** (up to 5 most recent):
- Complete final score
- Teams with region flags (emojis 🇧🇷🇺🇸🇪🇺🇰🇷🇯🇵 etc.)
- Event/tournament name
- Competition phase (Playoffs, Finals, etc.)
- Direct link to match page on VLR.gg

**🟠 Live Matches** (all ongoing games):
- Current real-time score
- "LIVE" status highlighted
- Participating teams with flags
- Tournament information
- Link to watch live

**🟢 Upcoming Matches** (up to 5 next):
- Time until start (e.g. "11h 51m", "2h 30m")
- Confirmed teams with flags
- Scheduled time
- Event details
- Link for more information

**Features:**
- Real-time updates via web scraping
- Automatic flag emojis to identify regions
- Match counter per category in title
- Valorant themed colors (#FF4655)
- Organized layout with visual separation (spacing) between matches
- No redundant information or repetitive labels

**Data sources:**
- [vlr.gg/matches](https://www.vlr.gg/matches) - Live and upcoming matches
- [vlr.gg/matches/results](https://www.vlr.gg/matches/results) - Matches finished today

---

### `/help`
Shows the list of all available commands with descriptions.

**Example:**
```
/help
```

**Information shown:**
- Complete list of commands
- Brief description of each command
- Representative emoji
- Valorant themed color

---

## 🗂️ Project Structure

```
EspalhaBrasas/
├── commands/
│   ├── help.py          # /help command - Lists all commands
│   ├── stats.py         # /stats command - Valorant stats (Competitive/Premier)
│   ├── valorant.py      # /ranked command - Competitive Valorant stats
│   ├── lfg.py           # /ranked and /ranked-cancel commands - LFG System
│   ├── maps.py          # /maps command - Competitive map rotation
│   └── vlr.py           # /vlr command - Professional matches from VLR.gg
├── events/
│   └── error.py         # Global error handling
├── utils/
│   └── valorant_stats.py # Helper functions for statistics
├── main.py              # Bot entry point
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (not included in git)
├── .env.example         # Configuration example
├── .gitignore           # Files ignored by git
├── README.md            # This file
├── PRIVACY_POLICY.md    # Privacy policy
└── TERMS_OF_SERVICE.md  # Terms of service
```

### Module Descriptions

#### `commands/`
Contains all bot slash commands organized by functionality:

- **`help.py`**: Help system that lists all available commands
- **`stats.py`**: Henrik API integration for detailed player statistics
- **`valorant.py`**: Commands related to competitive statistics
- **`lfg.py`**: Looking For Group system with interactive voting
- **`maps.py`**: Web scraping from thespike.gg for map rotation
- **`vlr.py`**: Web scraping from vlr.gg for professional matches

#### `events/`
Discord event handlers:

- **`error.py`**: Centralized error handling with user-friendly messages

#### `utils/`
Reusable helper functions:

- **`valorant_stats.py`**: Statistics fetching and formatting logic

---

## 🔧 Advanced Configuration

### Bot Permissions

In Discord Developer Portal, under "Bot" > "Privileged Gateway Intents", enable:
- ✅ **Message Content Intent** (required to read message content)
- ✅ **Server Members Intent** (optional, for future features)

### Bot Invite

Invite URL (replace `YOUR_CLIENT_ID` with your application ID):
```
https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=8&integration_type=0&scope=bot+applications.commands
```

Or use the specific link for this bot:
```
https://discord.com/oauth2/authorize?client_id=1425209969971695638&permissions=8&integration_type=0&scope=bot+applications.commands
```

**Required permissions:**
- ✅ Send Messages
- ✅ Embed Links
- ✅ Read Message History
- ✅ Use Slash Commands
- ✅ Add Reactions
- ✅ Attach Files (for future features)

---

## 🐛 Troubleshooting

### "Module not found"
**Cause:** Dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt
```

If it persists, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

### "Invalid token"
**Cause:** Incorrect or missing Discord token

**Solution:**
1. Check if the `.env` file exists in project root
2. Confirm that `DISCORD_TOKEN=` is filled
3. Regenerate token in Discord Developer Portal if necessary

---

### "Player not found" (/stats command)
**Possible causes:**
- Incorrect name format
- Player doesn't exist
- Invalid TAG

**Solutions:**
- Use exact format: `name#TAG` (e.g. `Player#1234`)
- TAG must be between 1-6 characters
- Verify the name in Valorant game
- Make sure player has played ranked matches

---

### "/stats not working"
**Possible causes:**
- Henrik API unavailable
- Invalid API key
- Rate limit exceeded

**Solutions:**
1. Check if `HENRIK_API_KEY` is configured in `.env`
2. Test the API: [Henrik API Status](https://discord.gg/X3GaVkX2YN)
3. Wait a few minutes if you hit the rate limit
4. Check terminal logs for specific errors

---

### "/maps not showing maps"
**Possible causes:**
- thespike.gg site unavailable
- HTML structure change on website
- Connection problem

**Solutions:**
1. Access [thespike.gg](https://www.thespike.gg/valorant/maps/map-pool) in browser
2. Check internet connection
3. If site changed, CSS selectors in `maps.py` may need updating

---

### "/vlr not showing matches"
**Possible causes:**
- vlr.gg site unavailable
- HTML structure change
- No matches scheduled for today

**Solutions:**
1. Check if there are matches at [vlr.gg/matches](https://www.vlr.gg/matches)
2. Wait a few minutes and try again
3. If it persists, HTML structure may have changed (update selectors in `vlr.py`)

---

### Flags not appearing (/vlr command)
**Cause:** Discord doesn't recognize country code

**Information:** Flags are standard Discord emojis (🇧🇷🇺🇸🇪🇺). If they don't appear, it could be:
- Invalid country code in VLR.gg HTML
- Discord rendering issue

---

### Bot not responding to commands
**Solutions:**
1. Check if bot is online (green status in Discord)
2. Confirm commands were synced (message in terminal at startup)
3. Verify bot permissions on server
4. Try `/help` to test

---

## 📝 Important Notes

### Henrik API
- **Free** with rate limits (60 requests/minute)
- For intensive use, consider upgrading to paid plan
- Data automatically updated by Riot Games API
- Supports all regions (EU, NA, ASIA, BR, LATAM, KR)

### Web Scraping
- `/maps` and `/vlr` commands depend on website HTML structure
- If sites change, CSS selectors may need updating
- Use moderately to avoid overloading servers

### Custom Emojis
- Rank emojis (`<:radiant:123>`) are specific to a server
- To use on another server, update IDs in `utils/valorant_stats.py`
- Lines 32-64 of `valorant_stats.py` file

### Performance
- Web scraping commands (`/maps`, `/vlr`) may take 2-5 seconds
- Uses `defer()` to avoid Discord timeout
- Cache can be implemented to improve performance

---

## 🤝 Contributing

Contributions are very welcome! Here's how you can help:

### How to Contribute

1. **Fork** the repository
2. Create a **branch** for your feature (`git checkout -b feature/MyFeature`)
3. **Commit** your changes (`git commit -m 'Add MyFeature'`)
4. **Push** to the branch (`git push origin feature/MyFeature`)
5. Open a **Pull Request**

### Ideas for Contributing

- 🐛 Report bugs
- ✨ Suggest new features
- 📝 Improve documentation
- 🎨 Improve embed interface
- ⚡ Optimize performance
- 🌍 Add support for more languages

### Guidelines

- Follow existing code style
- Comment complex code
- Test your changes before submitting
- Update README if necessary

---

## 📄 License

This project is **open-source** and available under the [MIT License](LICENSE).

You are free to:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Private use

**Conditions:**
- Include original license
- Give credit to original author

---

## 🔗 Useful Links

### Documentation
- [Discord.py Official Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord.py 2.0 Guide](https://discordpy.readthedocs.io/en/stable/migrating.html)

### APIs and Services
- [Henrik Valorant API](https://discord.gg/X3GaVkX2YN) - Discord to get key
- [Valorant API (Unofficial)](https://valorant-api.com/) - Game assets and data
- [TheSpike.gg](https://www.thespike.gg/valorant/maps/map-pool) - Map rotation
- [VLR.gg](https://www.vlr.gg/matches) - Esports and tournaments

### Tools
- [BeautifulSoup4 Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [aiohttp Docs](https://docs.aiohttp.org/)
- [Python dotenv](https://pypi.org/project/python-dotenv/)

---

## ✨ Author

Developed with ❤️ by **[YangSafe](https://github.com/a79300)**

- GitHub: [@a79300](https://github.com/a79300)
- Repository: [EspalhaBrasas](https://github.com/a79300/EspalhaBrasas)

---

## 🙏 Acknowledgements

- **Riot Games** - For creating Valorant
- **Henrik-3** - For providing the free API
- **Discord.py** - For the excellent library
- **Community** - For all the feedback and support

---

## 📊 Project Status

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Last update:** January 2025

---

## ⚠️ Legal Disclaimer

This bot is **not affiliated, associated, authorized or endorsed** by Riot Games, Inc.

**Valorant** is a registered trademark of **Riot Games, Inc.**

All game assets, images and data belong to their respective owners.

This project is for **educational and entertainment** purposes only.

---

<div align="center">

### 🎮 Made for the Valorant community 🎮

**If this project helped you, consider giving a ⭐ to the repository!**

</div>
