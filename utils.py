import discord
import datetime
from dateutil import tz
from datetime import datetime
from_zone = tz.tzutc()
to_zone = tz.tzlocal()


def qformat(quote, colour = None):
    embed_resp = discord.Embed(
        title = quote[1],
        colour=colour
    )
    embed_resp.set_author(name = quote[2])
    embed_resp.set_footer(text = f"Quote #{quote[0]}")
    curr_time = datetime.strptime(quote[3], '%Y-%m-%d %H:%M:%S')
    curr_time = curr_time.replace(tzinfo=from_zone)
    embed_resp.timestamp = curr_time.astimezone(to_zone)
    return embed_resp
