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
        
    def load_channels(self):
        channels_path = bundled_data_path(self) / "channels.json"
        with channels_path.open() as json_data:
            self.channels = json.load(json_data)
            
    def dump_channels(self):
        channels_path = bundled_data_path(self) / "channels.json"
        with open(channels_path, 'w') as json_data:
            json.dump(self.channels, json_data)
            
    def load_users(self):
        users_path = bundled_data_path(self) / "users.json"
        with users_path.open() as json_data:
            self.users = json.load(json_data)
            
    def dump_users(self):
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
    async def add(self, ctx: commands.Context, user: discord.User = None, channel: discord.TextChannel = None):
        """Add a user to the watchlist."""
        if user is not None and channel is not None:
            if self.users is None:
                self.load_users()
            if self.channels is None:
                self.load_channels()
            
            channels_dict = self.channels
            channels_dict[user.id] = channel.id
            self.channels = channels_dict
        
            self.dump_channels()
            
            users_dict = self.users
            try:
                null_list = users_dict[ctx.message.guild.id]
            except:
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
                self.dump_users()
        
                ti = "User successfully set."
                desc = "**{0}** will now be monitored. Logs will be sent to #{1}.".format(user.name, channel.name)
                em = discord.Embed(title=ti, description=desc, color=discord.Color.green())
                await ctx.send(embed=em)
        else:
            ti = "Invalid operands entered."
            desc = "Please enter the user and channel correctly."
            em = discord.Embed(title=ti, description=desc, color=discord.Color.red())
            await ctx.send(embed=em)
            
    @monitor.command()
    async def remove(self, ctx: commands.Context, user: discord.User = None):
        """Remove a user from the watchlist."""
        if user is not None:
            if self.users is None:
                self.load_users()
            f self.channels is None:
                self.load_channels()
                
            users_dict = self.users
            try:
                null_list = users_dict[ctx.message.guild.id]
            except:
                users_dict[ctx.message.guild.id] = []
            list = users_dict[ctx.message.guild.id]
            
            if list.count(user.id) == 0:
                ti = "User is not being monitored."
                desc = "Please mention another user to remove."
                em = discord.Embed(title=ti, description=desc, color=discord.Color.green())
                await ctx.send(embed=em)
            else:
                channels_dict = self.channels
                del channels_dict[user.id]
                self.channels = channels_dict
        
                self.dump_channels()
            
                list.remove(user.id)
                users_dict[ctx.message.guild.id] = list
                self.users = users_dict
                self.dump_users()
        
                ti = "User successfully removed."
                desc = "**{}** will no longer be monitored.".format(user.name)
                em = discord.Embed(title=ti, description=desc, color=discord.Color.green())
                await ctx.send(embed=em)
        else:
            ti = "No user entered."
            desc = "Please mention a user to remove."
            em = discord.Embed(title=ti, description=desc, color=discord.Color.red())
            await ctx.send(embed=em)
        
    @monitor.command()
    async def watchlist(self, ctx: commands.Context):
        """Check the watchlist. WARNING: Updating this cog will reset the watchlist."""
        if self.users is None:
            self.load_users()
        
        users_dict = self.users
        try:
            null_list = users_dict[ctx.message.guild.id]
        except:
            users_dict[ctx.message.guild.id] = []
        list = users_dict[ctx.message.guild.id]
        if len(list) < 1:
            ti = "Watchlist is empty."
        else:
            ti = "Watchlist for {}.".format(ctx.message.guild.name)
        desc = ""
        
        for userid in list:
            username = ctx.message.guild.get_member(userid).name
            desc += "\n**{}**".format(username)
        
        em = discord.Embed(title=ti, description=desc, color=discord.Color.blue())
        await ctx.send(embed=em)
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if self.users is None:
            self.load_users()
        
        users_dict = self.users
        
        try:
            null_list = users_dict[message.guild.id]
        except:
            users_dict[message.guild.id] = []
        list = users_dict[message.guild.id]
        
        if list.count(message.author.id) > 0:
            if self.channels is None:
                self.load_channels()
            
            channels_dict = self.channels
            try:
                null_list = channels_dict[message.author.id]
            except:
                channels_dict[message.author.id] = None
            
            if channels_dict[message.author.id] is not None:
                em = discord.Embed(title="Message sent", description=message.content, color=discord.Color.green())
                em.set_author(name=message.author, icon_url=message.author.avatar_url)
                em.set_footer(text="Original message sent by user with ID {0} in #{1} at time {2}.".format(message.author.id, message.channel, message.created_at))
                await message.guild.get_channel(channels_dict[message.author.id]).send(embed=em)
                
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if self.users is None:
            self.load_users()
        
        users_dict = self.users
        
        try:
            null_list = users_dict[message.guild.id]
        except:
            users_dict[message.guild.id] = []
        list = users_dict[message.guild.id]
        
        if list.count(message.author.id) > 0:
            if self.channels is None:
                self.load_channels()
            
            channels_dict = self.channels
            try:
                null_list = channels_dict[message.author.id]
            except:
                channels_dict[message.author.id] = None
            
            if channels_dict[message.author.id] is not None:
                em = discord.Embed(title="Message deleted", description=message.content, color=discord.Color.red())
                em.set_author(name=message.author, icon_url=message.author.avatar_url)
                em.set_footer(text="Original message sent by user with ID {0} in #{1} at time {2}.".format(message.author.id, message.channel, message.created_at))
                await message.guild.get_channel(channels_dict[message.author.id]).send(embed=em)
                
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if self.users is None:
            self.load_users()
        
        users_dict = self.users
        
        try:
            null_list = users_dict[before.guild.id]
        except:
            users_dict[before.guild.id] = []
        list = users_dict[before.guild.id]
        
        if list.count(before.author.id) > 0:
            if self.channels is None:
                self.load_channels()
            
            channels_dict = self.channels
            try:
                null_list = channels_dict[before.author.id]
            except:
                channels_dict[before.author.id] = None
            
            if channels_dict[before.author.id] is not None:
                em = discord.Embed(title="Message edited", color=discord.Color.blue())
                em.set_author(name=before.author, icon_url=before.author.avatar_url)
                em.add_field(name="**Before**", value=before.content)
                em.add_field(name="**After**", value=after.content)
                em.set_footer(text="Original message sent by user with ID {0} in #{1} at time {2}.".format(before.author.id, before.channel, before.created_at))
                await before.guild.get_channel(channels_dict[before.author.id]).send(embed=em)