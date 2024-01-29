# quotebot
Discord bot designed to save and recall memorable quotes, with the help of Discord.py and SQLite. Inspired by [Twitch's Streamer.bot](https://wiki.streamer.bot/en/Settings/Quotes).
Designed to be selfhosted, or with the aid of websites such as codesandbox + uptimerobot to keep it online all of the time. Quotes and settings are stored in an SQL database that is created upon first running the bot.

## Dependencies
- [Python3](https://www.python.org/downloads/)
- [reactionmenu](https://github.com/Defxult/reactionmenu/)

## Installation
### Creating A Bot User
1. Head to the [Discord Developer Portal](https://discord.com/developers/applications) and create a new application. Give it whatever name you'd like.
2. Generate and record the value of your bot token somewhere safe. Don't share this, because this is what's used to run the bot!.
3. Go to the Bot settings and turn on the "Server Members Intent" and "Message Content" intent under Privileged Intents.
4. Go to OAuth2 -> URL Generator and generate a URL, selecting the following: Bot (under scopes), and Send Messages, Add Reactions (under bot permissions). Use this URL to add the bot to your server.

### Hosting an Instance of the Bot (Locally)
1. Run `git clone https://github.com/phthallo/quotebotpy`to clone the contents of the repository to your computer. 
2. Edit `example.env` and add your bot token after the `=`.
3. Run main.py! 


# Commands

| Command | Explanation | Example |
| ------- | --------- | ------- | 
| `!guide` | Brings up a help menu containing all commands | - |
| `!add "<quote>" <author>` | `<quote>` is the quote to be added <br>`<author>` is who the quote should be attributed to. | `!add "Lorem ipsum dolor" Me` |
| `!get <search (type: int (quote ID))>` | `<search>` is the integer ID of the quote to be retrieved. | `!get 7`` |
| `!get "<search (type: str (search phrase))>"`| `<search>` is the phrase or word to search existing quotes for. | `!get "ipsum` |
| `!get all` | Returns all existing quotes in an reaction-navigable menu | - |
| `!get random` | Returns a random quote | - | 
| `!settings <setting> <value>` | Changes the setting to the specified value. <br>The only available option is `embedcolour`, which accepts a hex code | `!settings embedcolour #316b82`|