import discord
from discord.ext import commands
from engine import Player, Tournament, Match


class TournamentCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_tournaments = {}  

    @commands.command()
    async def create_tournament(self, ctx, name: str, rounds: int):
        name=ctx.guild.name + "_" + name
        if ctx.guild.id in self.active_tournaments:
            await ctx.send(f"A tournament already exists.")
            return
        
        tournament = Tournament(name, rounds)
        self.active_tournaments[ctx.guild.id] = tournament
        await ctx.send(f"Tournament '{name}' created with {rounds} rounds.")

    @commands.command()
    async def add_self(self, ctx):
        if ctx.guild.id not in self.active_tournaments:
            await ctx.send("No active tournament in this server. Please create one first.")
            return

        tournament = self.active_tournaments[ctx.guild.id]

        if tournament.current_round!=0:
            await ctx.send("Tournament has begun.")
            return
        
        if any(player.discord_id == ctx.author.id for player in tournament.competition):
            await ctx.send(f"{ctx.author.name} is already in the tournament.")
            return
        else:
            p=Player(ctx.author.id,ctx.author.name)
            tournament.add_player(p)
            await ctx.send(f"{ctx.author.name} has been added to the tournament.")
        return

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def start_round(self, ctx):
        if ctx.guild.id not in self.active_tournaments:
            await ctx.send("No active tournaments.")
            return
        tournament = self.active_tournaments[ctx.guild.id]
        if 2**(tournament.current_round - 1) >= len(tournament.competition):
            await ctx.send("Not enough players to start the round.")
            return
        round_schedule = tournament.round_start()
        if round_schedule:
            text = f"**Round {tournament.current_round} has started. Here are the matchups:**\n"
            for match in round_schedule:
                text+=f"<@{match.player1.discord_id}> vs <@{match.player2.discord_id}>\n"
            await ctx.send(text)
        else:
            await ctx.send("Failed to create pairings for the round.")

    @commands.command()
    async def report_match(self, ctx, player1_id: int, player2_id: int, p1_wins: int, p2_wins: int, draws: int):
        if ctx.guild.id not in self.active_tournaments:
            await ctx.send("No active tournaments.")
            return
        is_player = (ctx.author.id==player1_id) or (ctx.author.id==player2_id)
        is_admin = ctx.author.guild_permissions.manage_messages
        if not is_player and not is_admin:
            await ctx.send("Unauthorized.")
            return
        tournament = self.active_tournaments[ctx.guild.id]
        result=tournament.report_match(player1_id, player2_id, p1_wins, p2_wins, draws)

        if result="Success":
            await ctx.send(f"Match result reported for {player1_id} vs {player2_id}.")
            tournament.update_leaderboard()
            #self.save_tournament()
        else:
            await ctx.send(f"Score rejected: {result}")
        return

    @commands.command()
    async def remaining_match(self, ctx):
        if ctx.guild.id not in self.active_tournaments:
            await ctx.send("No active tournaments.")
            return
        tournament=self.active_tournaments[ctx.guild.id]
        matches_text=''
        for m in tournament.match_history[tournament.current_round]:
            if m.status!='Completed':
                matches_text+=f"Match between {m.player1.discord_id} and {m.player2.discord_id} in {m.status} status.\n"
        if matches_text=='':
            await ctx.send("All matches complete!")
        else:
            await ctx.send(matches_text)
        return

    @commands.command()
    async def show_leaderboard(self, ctx):
        if ctx.guild.id not in self.active_tournaments:
            await ctx.send("No active tournaments.")
            return
        tournament = self.active_tournaments[ctx.guild.id]
        leaderboard_text=''
        for i in range(len(tournament.competition)):
            leaderboard_text+=f"{i+1}: {tournament.competition[i].name}, Matches Played:' {tournament.competition[i].matches_played}, Points:' {tournament.competition[i].points}, Tiebreaker points: {tournament.competition[i].tiebreaker_points}\n"
        await ctx.send(leaderboard_text)
        return

async def setup(bot):
    await bot.add_cog(TournamentCog(bot))