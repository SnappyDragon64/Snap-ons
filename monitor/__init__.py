from .monitor import Monitor


def setup(bot):
    bot.add_cog(Monitor(bot))