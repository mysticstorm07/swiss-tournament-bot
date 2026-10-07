# swiss-tournament-bot

I have been an avid player of video games all my life, and over the past few months, I have been participating in online tournaments whenever I find the time, and spectating when I don't. However, the tournaments I play in almost always seem to use external websites to create brackets and matches, which then have to be conveyed over Discord.

That gave me the inspiration to create a Discord bot that could automate the entire matchmaking process within the platform without having to rely on an external tool.
Specifically, I created a bot that creates and hosts tournaments in the Swiss format. I found Swiss to be the most interesting tournament format (compared to single-elimination, double-elimination, and round-robin) and decided to try making this bot as my first attempt at a real project.

## The Rules of Swiss

Swiss is one of the fairer tournament formats. You never have to worry about playing opponents who are too tough—or too easy, for that matter. Swiss ensures that the opponent you play against is close to your skill level. Of course, the more games that are played, the fairer the matchups become.

The rules work as follows:

* **In the case of an odd number of players**, the player unable to be paired up with anyone is given a bye, meaning they are awarded a win. A player can only be given one bye per tournament.
* **The opponent a player is matched with usually shares the same win-loss record across the entire tournament.** If, however, there is no such opponent to match against, the selected opponent is the next highest-ranked player on the leaderboard.
For example, if the leaderboard of a 40-player tournament after 5 rounds looks like:
```text
A - 5 Wins, 0 Losses
B - 4 Wins, 1 Loss
C - 4 Wins, 1 Loss
D - 4 Wins, 1 Loss
E - 4 Wins, 1 Loss
F - 4 Wins, 1 Loss
G - 4 Wins, 1 Loss
...and so on

```


Then player A is paired against one of the players with 4 wins and 1 loss for Round 6. A natural question might be: *How do we decide which 4–1 player to pair A against?* This is resolved by the next rule.
* **A player must *not* be paired against an opponent they have already played.** If matchmaking cannot create a valid matchup for all players, the tournament must either be completed or continued anew (meaning the next set of matchups is made assuming no player has played anyone).

In the example above, if A has not played against B, they may be paired against each other for Round 6. The word "may" is key because all remaining players must also have valid, unplayed opponents. If pairing A with B leaves another player with no valid matchup, the matchmaking system must backtrack to find valid matchups for everyone. So, if A playing B results in another player having no valid opponent, A cannot play B and must be paired with the next best available opponent.
*(This is unlikely to happen in this sample tournament, but this explanation illustrates the rule.)*

* **There are different types of tiebreakers used to refine leaderboard rankings.** The exact tiebreaking methods are completely up to the tournament host to decide.
The method I implemented in my bot is **game differential (win-loss difference)**, assuming each match is played as a best-of-3. If A wins against B with a 2–1 score, in addition to receiving a match win, A gets **+1 tiebreaker point**. Similarly, B receives a match loss and **-1 tiebreaker point**.
I have also included draws as a possible match outcome—a draw awards **0 tiebreaker points**.

## What Has Been Done (and What Remains)

Keeping in mind the above rules, I have built an engine that runs matchmaking, as well as leaderboard fetching and updating functions. Matchmaking is carried out by a simple recursive function—which I found a bit challenging yet fun to derive—while the rest are simple get-and-update functions.

The `tournament.py` file is the Discord interface that tournament hosts, admins, and players interact with on a Discord server. It is currently designed to be minimalistic, as my primary goal when making this project was simply to build something that functions properly.

The `main.py` file has yet to be created, but since the majority of the brainstorming went into the engine and interface, completing the main file isn't something I am too worried about. What I also forgot to handle in the score-deciding algorithm was a completely tied match (e.g., 3 draws, or 1 win, 1 loss, and 1 draw), but that isn't a particularly difficult problem to solve either.

So what really remains is completing the `main.py` file, importing the bot into a Discord server, and testing it out. Hopefully, this can be accomplished over the next two weeks.
