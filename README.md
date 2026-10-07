# swiss-tournament-bot

I have been an avid player of video games all my life, and over the past months I have been participating in online tournaments whenever I find the time, and spectate when I don't. However, the tournaments I play in almost always seem to use an external website to create brackets and matches which then have to be conveyed over Discord.

That gave me the inspiration to create a bot on the same that could automate the entire matchmaking process within the platform without having to rely on a different tool.
Specifically, I created a bot that creates and hosts tournaments in the Swiss format. I found Swiss to be the most interesting tournament format (others being single-elimination (knockouts), double-elimination, and Round Robin) and decided to try making this bot as my first attempt at a real project.

## The Rules of Swiss 

Swiss is one of the fairer tournament formats. You never have to worry about playing too tough opponents, or easy for that matter. Swiss ensures that the opponent you play against is of your skill level. Of course, the more games that are played, the fairer the matchups become.

The rules work as follows:

- In case of an odd number of players, the player unable to be paired up against anyone is given a bye, meaning he is awarded a win. A player can only be given one bye per tournament.

- __The opponent a player is matched up with usually shares the number of wins and losses they have both incurred across the entire tournament.__ If, however, there is no such opponent to be matched up against, the opponent is decided to be the next highest ranked opponent in the leaderboard.

So for example, if the leaderboard of a tournament of 40 players after 5 rounds looks like: 
A - 5 Wins 0 Losses 
B - 4 Wins 1 Loss
C - 4 Wins 1 Loss
D - 4 Wins 1 Loss
E - 4 Wins 1 Loss
F - 4 Wins 1 Loss
G - 4 Wins 1 Loss
....and so on and so on, then A is paired up against the one of the players with 4 wins and 1 loss for round 6. A natural question may be, how do we decide which opponent to pair A against? This is resolved by the next rule.

- __A player must _not_ be paired up against an opponent they have already played.__ If there is no way for matchmaking to be done that creates a valid matchup for all players, the tournament must be completed, or should be continued anew, meaning the next matchup should be made assuming no player has played anyone.

So in the above example, if A has not played with B, they may be the round 6 matchups for each other. The 'may' is because the rest of the players should also have valid opponents to play, i.e. opponents they haven't played before. In case a player doesn't have a valid remaining matchup, the matchmaking has to be traced back to a point where valid matchups _may_ be made. So if A playing B implies that there is always a player with no valid matchup, then A cannot play B and he must find the next best opponent.
(This is most likely never going to happen in this sample tournament, but I hope the explanation clears the rule up.)

- There are different types of tiebreakers to refine the rankings in leaderboards. There are different tie breaking means which are completely up to the tournament host to decide.

The means I have used in my bot is a win-loss difference, since I have also assumed that each round will be a best of 3. If A wins in the match against B with a 2-1 score, apart from the awarded win, A also receives 1 tie breaking point. Similarly, B receives a loss as well as a -1 tie breaking point.

I have also included draws in my round outcome - a draw rewards 0 tie breaking points. 

