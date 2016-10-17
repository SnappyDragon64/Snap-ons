from discord.ext import commands
import random
import discord

class Kill:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def kill(self, context, member : discord.Member):
        """Wanna kill someone? Wanna be the troll kind? You've got the perfect cog for the lulz! 21 unique and funny kill commands!"""
        killer = context.message.author.mention
        victim = member.mention
        method = {}
        method['1'] = '{0} shoots  in {1}\'s mouth with rainbow laser, causing {1}\'s head to explode with rainbows and {1} is reborn as unicorn. :unicorn:'.format(killer, victim)
        method['3'] = '{0} is stuffed into a suit by Freddy on their night guard duty. Oh, not those animatronics again! :bear:'.format(victim)
        method['4'] = '{0} grabs {1} and shoves them into an auto-freeze machine with some juice and sets the temperature to 100 Kelvin, creating human ice pops.'.format(killer, victim)
        method['5'] = '{0} drowns {1} in a tub of hot chocolate. *"How was your last drink?"*'.format(killer, victim)
        method['6'] = '{0} screams in terror as they accidentally spawn in the cthulhu while uttering random latin words. Cthulhu grabs {0} by the right leg and takes them to his dimension yelling,"Honey, Dinner\'s ready!"'.format(victim)
        method['7'] = '{0} feeds toothpaste-filled oreos to {1}, who were apparently allergic to fluorine. GGWP.'.format(killer, victim)
        method['8'] = '{0} forgot to zombie-proof {1}\'s lawn... Looks like zombies had a feast last night.'.format(killer, victim)
        method['9'] = '{0} cranks up the music system only to realize the volume was at max and the song playing was Baby by Justin Beiber...'.format(victim)
        method['10'] = '{0} presses a random button and is teleported to the height of 100m, allowing them to fall to their inevitable death. Moral of the story: Don\'t go around pressing random buttons.'.format(victim)
        method['11'] = '{0} is injected with chocolate syrup, which mutates them into a person made out of chocolate. While doing a part-time job at the Daycare, they are devoured by the hungry babies. :chocolate_bar:'.format(victim)
        method['12'] = '{0} is sucked into Minecraft. {0}, being a noob at the so called "Real-Life Minecraft" faces the Game Over screen.'.format(victim)
        method['13'] = '{0} turns on Goosebumps (2015 film) on the TV. {1} being a scaredy-cat, dies of an heart attack.'.format(killer, victim)
        method['14'] = '{0} after a long day, plops down on the couch with {1} and turns on The Big Bang Theory. After a Sheldon Cooper joke, {1} laughs uncontrollably as they die.'.format(killer, victim)
        method['15'] = '{0} was given a chance to synthesize element 119 (Ununennium) and have it named after them, but they messed up. R.I.P.'.format(victim)
        method['16'] = '{0} gets {1} to watch anime with them. {1} couldn\'t handle it.'.format(killer, victim)
        method['17'] = '{0} tries to get crafty, but they accidentally cut themselves with the scissors.:scissors:'.format(victim)
        method['18'] = '{0} goes genoicide and Sans totally dunks {0}!'.format(victim)
        method['19'] = '{0} was so swag that {1} died due to it. #Swag'.format(killer, victim)
        method['20'] = '{0} has been found guilty, time for their execution!'.format(victim)
        method['21'] = '{0} fell down a cliff while playing Pokemon Go. Good job on keeping your nose in that puny phone. :iphone:'.format(victim)

       await self.bot.say('**{0}**'.format(random.choice([method[i] for i in method])))

def setup(bot):
    n = Kill(bot)
    bot.add_cog(n)