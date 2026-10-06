#initial tournamenet setup
#player addition
#after creating round schedule, displaying round schedule
#updating reporting disputing results

class Tournament:
    def __init__(self,name,n):
        self.name=name
        self.competition=[]
        self.rounds=n
        self.match_history={}
        self.current_round=0

    def to_dict(self):
        return {
            "name": self.name,
            "rounds": self.rounds,
            "current_round": self.current_round,
            "competition": [player.to_dict() for player in self.competition],
            "match_history": {
                str(round_num): [match.to_dict() for match in matches] for round_num, matches in self.match_history.items()
            }
        }

    @classmethod
    def from_dict(cls,data:dict):
        name=data["name"]
        rounds=data["rounds"]
        tournament=cls(name,rounds)
        tournament.current_round=data.get("current_round",0)
        tournament.competition=[Player.from_dict(p_data) for p_data in data["competition"]]

        player_map = {p.discord_id: p for p in tournament.competition}

        tournament.match_history = {}
        for round_num_str, matches_data in data["match_history"].items():
            round_num = int(round_num_str)
            round_matches = []
            
            for m_data in matches_data:
                # 3. Grab the REAL players from the map instead of creating ghost players
                p1 = player_map[m_data["player1"]["discord_id"]]
                p2 = player_map[m_data["player2"]["discord_id"]]
                
                # Rebuild the match using real players
                match = Match(p1, p2, m_data["status"])
                match.p1_wins = m_data.get("p1_wins", 0)
                match.p2_wins = m_data.get("p2_wins", 0)
                match.draws = m_data.get("draws", 0)
                round_matches.append(match)
                
            # FIX: Syntax error corrected here
            tournament.match_history[round_num] = round_matches
        return tournament

    def add_player(self,player):
        self.competition.append(player)

    def pair_player(self, waiting_room, round_schedule):
        if len(waiting_room)==0:
            return True
        else:
            player1=waiting_room.pop(0)
            for k in range(len(waiting_room)):
                if waiting_room[k].discord_id not in player1.played:
                    player2=waiting_room.pop(k)
                    round_schedule.append(Match(player1,player2))
                    if self.pair_player(waiting_room, round_schedule)==True:
                        return True
                    else:
                        waiting_room.insert(k,player2)
                        round_schedule.pop()
            waiting_room.insert(0,player1)
            return False

    def update_leaderboard(self):
        self.competition.sort(key=lambda x: (x.points,x.tiebreaker_points),reverse=True)
        
    def round_start(self): #start of each round
        self.current_round+=1
        round_schedule=[]
        self.update_leaderboard()
        waiting_room=self.competition.copy()
        if len(waiting_room)%2==1: #accounting for bye
            for j in range(len(waiting_room)-1,-1,-1):
                if waiting_room[j].bye==False:
                    waiting_room[j].bye=True
                    bye_player=waiting_room.pop(j)
                    break
            bye_player.points+=2
            bye_player.tiebreaker_points+=3
    #creating the pairings for the round
        if self.pair_player(waiting_room,round_schedule):
            self.match_history[len(self.match_history)+1]=round_schedule
            return round_schedule
        else:
            self.current_round-=1
            return False
        
    def report_match(self, player1_id, player2_id, p1_wins, p2_wins, draws):
        current_matches = self.match_history.get(self.current_round, [])
        
        for match in current_matches:
            has_p1 = match.player1.discord_id in (player1_id, player2_id)
            has_p2 = match.player2.discord_id in (player1_id, player2_id)
            
            if has_p1 and has_p2:
                if match.status == "Completed":
                    return "Error: Match already reported."
                if match.player1.discord_id == player1_id:
                    return match.resolve(p1_wins, p2_wins, draws)
                else:
                    return match.resolve(p2_wins, p1_wins, draws)
                
        return "Error: Match not found in current round."
    
class Player:
    def __init__(self,discord_id,name,points=0,tiebreaker_points=0,matches_played=0,played=None,bye=False):
        self.discord_id = discord_id
        self.name=name
        self.points = points
        self.tiebreaker_points = tiebreaker_points
        self.matches_played = matches_played
        self.played = played if played is not None else []
        self.bye=bye

    def to_dict(self):
        return {
            "discord_id": self.discord_id,
            "name":self.name,
            "points":self.points,
            "tiebreaker_points":self.tiebreaker_points,
            "matches_played":self.matches_played,
            "played":self.played,
            "bye":self.bye
        }

    @classmethod
    def from_dict(cls,data:dict):
        return cls(
            discord_id=data['discord_id'],
            name=data['name'],
            points=data.get('points',0),
            tiebreaker_points=data.get('tiebreaker_points',0),
            matches_played=data.get('matches_played',0),
            played=data.get('played',[]),
            bye=data.get('bye',False)
        )

class Match:
    def __init__(self,player1 : Player,player2 : Player, status="Pending"):
        self.player1 = player1
        self.player2 = player2
        self.p1_wins=0
        self.p2_wins=0
        self.draws=0
        self.status=status #pending, completed, disputed, reported
        self.winner=None

    def to_dict(self):
        return {
            "player1": self.player1.to_dict(),
            "player2": self.player2.to_dict(),
            "status":self.status,
            "p1_wins":self.p1_wins,
            "p2_wins":self.p2_wins,
            "draws":self.draws
        }

    @classmethod
    def from_dict(cls,data:dict):
        p1=Player.from_dict(data["player1"])
        p2=Player.from_dict(data["player2"])
        match=cls(p1,p2,data["status"])
        match.p1_wins=data.get("p1_wins",0)
        match.p2_wins=data.get("p2_wins",0)
        match.draws=data.get("draws",0)
        return match

    def resolve(self,p1_wins,p2_wins,draws): #updates points, matches played, played and not played lists
        #result=input("W/L/D:")
        if p1_wins>2 or p2_wins>2 or (p1_wins+p2_wins+draws>3):
            return "Invalid game count"
        
        self.status="Completed"

        self.player1.points+=p1_wins*2+draws*1+p2_wins*0
        self.player1.tiebreaker_points+=p1_wins+p2_wins*(-1)
        self.player2.points+=p2_wins*2+draws*1+p1_wins*0
        self.player2.tiebreaker_points+=p2_wins+p1_wins*(-1)

        self.p1_wins = p1_wins
        self.p2_wins = p2_wins
        self.draws = draws

        if p1_wins>p2_wins:
            self.winner=self.player1.discord_id
        elif p2_wins>p1_wins:
            self.winner=self.player2.discord_id
        else:
            self.winner="Draw"
        
        self.player1.matches_played+=1
        self.player2.matches_played+=1
        self.player1.played.append(self.player2.discord_id)
        self.player2.played.append(self.player1.discord_id)

        return "Success"

