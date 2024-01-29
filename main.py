import discord
import sqlite3
from utils import qformat
from dateutil import tz
import re 
import os
import random
from discord.ext import commands
from reactionmenu import ReactionMenu, ReactionButton
from dotenv import load_dotenv
load_dotenv("variables.env")
intents = discord.Intents.default()
intents.messages=True 
intents.guilds=True 
intents.reactions=True
intents.members=True
intents.message_content = True
activity=discord.Game(name="use !guide to get started!")
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)    

# DATABASES
# Quotes
qconnection = sqlite3.connect("quotes.db")
qcursor = qconnection.cursor()
qcursor.execute("CREATE TABLE IF NOT EXISTS quote(id INTEGER PRIMARY KEY AUTOINCREMENT, content, author, date)")
# Settings
sconnection = sqlite3.connect("settings.db")
scursor = sconnection.cursor()
scursor.execute("CREATE TABLE IF NOT EXISTS settings(id INTEGER PRIMARY KEY AUTOINCREMENT, setting, value, UNIQUE(setting, value))")

scursor.execute(f"""
        INSERT OR REPLACE INTO settings 
                VALUES(1, 
                "embedcolour", 
                COALESCE((SELECT value from settings WHERE id == 1), '0x5d66f6'))
        """)
sconnection.commit()
buttons = [ReactionButton.go_to_first_page(), ReactionButton.back(), ReactionButton.end_session(), ReactionButton.next(), ReactionButton.go_to_last_page()]

# Timezones
from_zone = tz.tzutc()
to_zone = tz.tzlocal()

#Commands
@bot.command()
async def settings(ctx, setting, value):
    if setting in ["embedcolour"]:
        if setting == "embedcolour" and re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value): 
            scursor.execute(f"""UPDATE settings 
                            SET value=? 
                            WHERE setting = ?""", (value, setting))
            sconnection.commit()
            await ctx.send(f'{setting} updated to {value}')

@bot.command()
async def guide(ctx):
    em_co = (scursor.execute(f"""SELECT value FROM settings WHERE setting == ?""", ("embedcolour",)).fetchone()[0]).replace("#", "0x")
    pages = [discord.Embed(title="Help Menu", 
                           description="*Quotes*", 
                           color=int(em_co,16)).add_field(
                               name='!add `"<quote>" <author>`', 
                               value='*!add "Lorem ipsum dolor sit amet" Person*\nAdds the quote "Lorem ipsum dolor sit amet", authored by Person, timestamped to when the command was sent.',
                               inline=False).add_field(
                               name='!get "`<search (type: int (quote ID))>`"', 
                               value="*!get 7*\nReturns the quote with the specified ID 7 (or a null quote if none exists)",
                               inline=False).add_field(
                               name='!get "`<search (type: str (search phrase))>`"',
                               value="*!get ipsum*\nReturns all instances of quotes mentioning the specified phrase 'ipsum'",
                               inline=False).add_field(
                               name='!get "`<special: all or random)>`"',
                               value="*!get all*\nReturns all instances of quotes.\n*!get random*\nReturns a random quote.",
                               inline=False),

            discord.Embed(title="Help Menu", 
                          description="*General*", 
                          color=int(em_co,16)).add_field(
                            name='!guide', 
                            value='Brings up this menu.',
                            inline=False).add_field(
                            name='!settings `<setting> <value>`', 
                            value='*!settings embedcolour #316b82*\nChanges the embed colour to the specified hexcode. Note: only accepts hexcodes.',
                            inline=False
                          )
    ]
    menu = ReactionMenu(ctx, 
                        menu_type=ReactionMenu.TypeEmbed, 
                        clear_reactions_after=False)
    for page in pages: 
        menu.add_page(page)
    for button in buttons:
        menu.add_button(button)

    await menu.start()


@bot.command()
async def add(ctx, message, author):
    data = (
        {"content": message, 
         "author": author,
         "date": str((ctx.message.created_at).strftime('%Y-%m-%d %H:%M:%S'))}
    )
    qcursor.execute(f"""
    INSERT INTO quote VALUES
        (NULL, :content, :author, :date)
    """, data)
    id = qcursor.execute(f"""
    SELECT id FROM quote ORDER BY id DESC LIMIT 1""").fetchone()
    qconnection.commit()
    await ctx.send(f'Quote "{message}" added (Quote #{id[0]})')
    
@bot.command()
async def get(ctx, *search):
    search = ' '.join(search)
    em_co = (scursor.execute(f"""SELECT value FROM settings WHERE setting == ?""", ("embedcolour",)).fetchone()[0]).replace("#", "0x")
    gconnection = sqlite3.connect("quotes.db")
    gcursor = gconnection.cursor()
    if search.isdigit(): 
        num_quote = gcursor.execute(f"""
                       SELECT id, content, author, date FROM quote WHERE id == ?
                       """,  (search,)).fetchone()
    elif search == "all":
        num_quote = gcursor.execute(f"""
                       SELECT id, content, author, date FROM quote
                       """).fetchall()
    elif search == "random": 
        max_id = random.randint(1,int(qcursor.execute(f"""
    SELECT id FROM quote ORDER BY id DESC LIMIT 1""").fetchone()[0]))
        num_quote = gcursor.execute(f"""
                       SELECT id, content, author, date FROM quote WHERE id == ?
                       """,  (max_id,)).fetchone()
    else:
        num_quote = gcursor.execute(f"""
                       SELECT id, content, author, date FROM quote WHERE content LIKE ?
                       """,  ('%'+search+'%',)).fetchall()
    if num_quote == []: 
        num_quote = (0, "Invalid quote", "Null", "2000-01-01 12:00:00")
    if isinstance(num_quote, list): 
        quote_results = [qformat(quote, colour= int(em_co,16)) for quote in num_quote]
        menu = ReactionMenu(ctx, 
                            menu_type=ReactionMenu.TypeEmbed, 
                            clear_reactions_after=False)
        for quote in quote_results:
            menu.add_page(quote)
        for button in buttons:
            menu.add_button(button)
        await menu.start()

    else:
        embed_resp = qformat(num_quote, colour=int(em_co,16))
        await ctx.send(embed = embed_resp)

@bot.command()
async def edit(ctx, id, replacement):
    qcursor.execute(f"""
    UPDATE quote 
    SET content=?
    WHERE id=?
    """, (replacement, int(id)))
    qconnection.commit()
    await ctx.send(f"Quote {id} updated!")

bot.run(os.environ.get("TOKEN"))