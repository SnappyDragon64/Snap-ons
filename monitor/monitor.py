import discord
import json
from redbot.core import commands
from redbot.core.commands import Cog


class Unicode(Cog):
    """Monitor users."""

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.channels = None
        self.users = None
        

    async def red_delete_data_for_user(self, **kwargs):
        """Nothing to delete"""
        return
        
    def load_files(self):
        channels_path = bundled_data_path(self) / "channels.json"
        with channels_path.open() as json_data:
            self.channels = json.load(json_data)
            
        users_path = bundled_data_path(self) / "users.json"
        with users_path.open() as json_data:
            self.users = json.load(json_data)
            
    def dump_files(self):
        channels_path = bundled_data_path(self) / "channels.json"
        with channels_path.open() as json_data:
            json.dump(self.channels, json_data)
            
        users_path = bundled_data_path(self) / "users.json"
        with users_path.open() as json_data:
            json.dump(self.users, json_data)
            
    @commands.group(name="monitor", pass_context=True)
    async def monitor(self, ctx):
        """Monitor users."""
        if ctx.invoked_subcommand is None:
            pass

    @monitor.command()
    async def set(self, ctx: commands.Context, channel):
        """Enter channel to log data to."""
        channel_dict = self.channels
        channel_dict[ctx.message.guild.id] = channel.id
        self.channels = channel_dict
        
        ti = "Channel successfully set."
        desc = "Log data will now be sent to #{}.".format(channel.name)
        em = discord.Embed(title=ti, description=desc, color=color)
        await ctx.send(embed=em)
    