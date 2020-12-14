import discord
import json
from redbot.core import commands, checks
from redbot.core.commands import Cog
from redbot.core.data_manager import bundled_data_path


class Monitor(Cog):
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
        with open(channels_path, 'w') as json_data:
            json.dump(self.channels, json_data)
            
        users_path = bundled_data_path(self) / "users.json"
        with open(users_path, 'w') as json_data:
            json.dump(self.users, json_data)
            
    @commands.group(name="monitor", pass_context=True)
    @checks.mod_or_permissions(administrator=True)
    async def monitor(self, ctx):
        """Monitor users."""
        if ctx.invoked_subcommand is None:
            pass

    @monitor.command()
    async def set(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """Enter channel to log data to."""
        if channel is not None:
            if self.channels is None:
                self.load_files()
            
            channel_dict = self.channels
            channel_dict[ctx.message.guild.id] = channel.id
            self.channels = channel_dict
        
            self.dump_files()
        
            ti = "Channel successfully set."
            desc = "Log data will now be sent to #{}.".format(channel.name)
            em = discord.Embed(title=ti, description=desc, color=discord.Color.green())
            await ctx.send(embed=em)
        else:
            ti = "No channel entered."
            desc = "Please mention a channel to send log data to."
            em = discord.Embed(title=ti, description=desc, color=discord.Color.red())
            await ctx.send(embed=em)
            
    @monitor.command()
    async def add(self, ctx: commands.Context, user: discord.User = None):
        """Enter channel to log data to."""
        if user is not None:
            if self.users is None:
                self.load_files()
            
            users_dict = self.users
            if users_dict[ctx.message.guild.id] is none:
                users_dict[ctx.message.guild.id] = []
            list = users_dict[ctx.message.guild.id]
            
            if list.count(user.id) > 0:
                ti = "User already being monitored."
                desc = "Please mention another user to monitor."
                em = discord.Embed(title=ti, description=desc, color=discord.Color.green())
                await ctx.send(embed=em)
            else:
                list.append(user.id)
                users_dict[ctx.message.guild.id] = list
                self.users = users_dict
                self.dump_files()
        
                ti = "User successfully set."
                desc = "{} will now be monitored.".format(user.name)
                em = discord.Embed(title=ti, description=desc, color=discord.Color.green())
                await ctx.send(embed=em)
        else:
            ti = "No user entered."
            desc = "Please mention a user to monitor."
            em = discord.Embed(title=ti, description=desc, color=discord.Color.red())
            await ctx.send(embed=em)
        
    