import discord
from discord.ext import commands
from engine import Tournament, Player, Match
import os

bot = commands.Bot(command_prefix='!')

a=0
active_tournaments = {}



