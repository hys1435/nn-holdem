import re
import os

card_list = [
    'Ah',
    '2h',
    '3h',
    '4h',
    '5h',
    '6h',
    '7h',
    '8h',
    '9h',
    'Th',
    'Jh',
    'Qh',
    'Kh',
    'Ac',
    '2c',
    '3c',
    '4c',
    '5c',
    '6c',
    '7c',
    '8c',
    '9c',
    'Tc',
    'Jc',
    'Qc',
    'Kc',
    'Ad',
    '2d',
    '3d',
    '4d',
    '5d',
    '6d',
    '7d',
    '8d',
    '9d',
    'Td',
    'Jd',
    'Qd',
    'Kd',
    'As',
    '2s',
    '3s',
    '4s',
    '5s',
    '6s',
    '7s',
    '8s',
    '9s',
    'Ts',
    'Js',
    'Qs',
    'Ks'
]

action_list = [
    'calls',
    'checks',
    'folds',
    'posts',
    'raises',
    'bets'
]

def write_card(w_card, file):
    with open(file, 'a') as current_file:
        for r_card in card_list:
            if w_card == r_card:
                current_file.write("1")
            else:
                current_file.write("0")
            current_file.write(", ") 
        current_file.write("\n")

def write_action(w_action, file):
    with open(file, 'a') as current_file:
        for r_action in action_list:
            if w_action == r_action:
                current_file.write("1")
            else:
                current_file.write("0")
            current_file.write(", ")
        current_file.write("\n")

def write_bet(w_bet, file):
    with open(file, 'a') as current_file:
        current_file.write(str(w_bet) + ',')
        current_file.write("\n")

"""This class holds all the games for a given parse"""
class matches:
    def __init__(self, game_type, bet_type, blind):
        self.game_type = game_type
        self.bet_type = bet_type
        self.blind = blind
        self.games = []

    def add_game(self, game):
        self.games.append(game)

    def get_current_game(self):
        return self.games[-1]

    def set_current_game(self, game):
        self.games[-1] = game

    """Exports game data to a csv readable format and deletes all games
    in the object"""
    def export_games_to_csv(self):
        current_actions = os.listdir('./actions')
        filename = './actions/'+ 'action' + '.txt'
        mod_games = self.games[:-1]
        for g in mod_games:
            hasCards = True
            for p in g.players:
                if p.private_cards == []:
                    hasCards = False
                    break
            if hasCards:
                for p in g.players:
                    for c in p.private_cards:
                        write_card(c, filename)
                    write_bet(p.money, filename)
                t_index = 0
                for t in g.turns:
                    if t_index != 0:
                        p_c = list(set(t.public_cards) - set(g.turns[t_index - 1].public_cards))
                    else:
                        p_c = t.public_cards
                    t_index = t_index + 1
                    for c in p_c:
                        write_card(c, filename)
                    for m in t.moves:
                        a = m[1]
                        if m[2] == None:
                            b = 0
                        else:
                            b = m[2]
                        write_action(a, filename)
                        write_bet(b, filename)
                with open(filename, 'a') as f:
                    f.write('-1,\n')
        self.games = [self.games[-1]]
"""This class holds all the data for a given game"""
class game:
    def __init__(self, game_num, time):
        self.game_num = game_num
        self.players = []
        self.button = None
        self.time = time
        self.turns = []
        self.winner = None
        self.rake = 0
        self.pot = 0

    def add_player(self, player):
        self.players.append(player)

    def set_button(self, button):
        self.button = button

    def set_rake(self, rake):
        self.result = result

    def add_turn(self, turn):
        self.turns.append(turn)

    def set_winner(self, winner):
        self.winner = winner

    """Determines when scanning whether this is the first player to
    be entered into the game object. Used for determining who is the
    button"""
    def first_player(self):
        if len(self.players) == 1:
            return True
        else:
            return False

    def recent_turn(self):
        return self.turns[-1]

    def set_current_turn(self, turn):
        self.turns[-1] = turn

"""A turn is an object that encompasses all the actions associated
with a phase of a game. The river card and all betting would be
considered a turn"""
class turn:
    def __init__(self):
        self.moves = []
        self.public_cards = []

    def add_move(self, player, action, bet):
        self.moves.append([player, action, bet])

    def add_public_cards(self, cards):
        for card in cards:
            self.public_cards.append(card)

class player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.private_cards = []

    def add_private_cards(self, cards):
        if self.private_cards == []:
            for card in cards:
                self.private_cards.append(card)

# Lets functions search for particular information in a given line and
# extract it, given a line type
queries = {
    'game number': re.compile(r'#(\d*):'),
    'game type': re.compile(r'(\S*)\s(\S*)\s*\(\$(\d*)/\$([\d\.]*)\sUSD'),
    'game time': re.compile(r'(\d*/\d*/\d*\s\d*:\d*:\d*\s\w*)'),
    'player': re.compile(r'Seat\s\d*:\s(.*)\s\(\$([\d\.]*)\sin\schips'),
    'action': re.compile(r'(.*):\s(\w*)'),
    'bet': re.compile(r'\w*\s\$(\d*)'),
    'flop': re.compile(r'\[(\S*)\s(\S*)\s(\S*)\]'),
    'turn and river': re.compile(r'\[.*\]\s\[(\S*)\]'),
    'result': re.compile(r'Total\spot\s\$([\d\.]*).*Rake\s\$([\d\.]*)'),
    'winner': re.compile(r'(.*)\scollected'),
    'player hand': re.compile(r'(.*):\sshows\s\[(\S*)\s(\S*)\]'),
}

# Determines the flow of the scanning. If I know I am on this line,
# what lines can I expect next
next_line_type = {
    'game': ['player'],
    'player': ['player', 'post action'],
    'post action': ['post action', 'hole'],
    'hole': ['hole action', 'flop'],
    'hole action': ['hole action', 'flop'],
    'flop': ['flop action', 'turn'],
    'flop action': ['flop action', 'turn'],
    'turn': ['turn action', 'river'],
    'turn action': ['turn action', 'river'],
    'river': ['river action', 'hand reveal', 'winner'],
    'river action': ['river action', 'hand reveal', 'winner'],
    'hand reveal': ['hand reveal', 'winner'],
    'winner': ['result'],
    'result': ['game']
}

find_action = re.compile(r'.*:\s\w*')

# Dictionary to check whether a line is of a certain type
line_types = {
    'game': re.compile('PokerStars Hand'),
    'player': re.compile(r'in\schips'),
    'post action': re.compile(r'\S*: posts \w* blind'),
    'hole': re.compile(r'\*{3}\sHOLE CARDS\s\*{3}'),
    'hole action': find_action,
    'flop': re.compile(r'\*{3}\sFLOP\s\*{3}'),
    'flop action': find_action,
    'turn': re.compile(r'\*{3}\sTURN\s\*{3}'),
    'turn action': find_action,
    'river': re.compile(r'\*{3}\sRIVER\s\*{3}'),
    'river action': find_action,
    'hand reveal': re.compile(r'\S*:\sshows'),
    'winner': re.compile(r'\scollected\s'),
    'result': re.compile(r'Total\spot.*Rake')
}

"""Creates a new game based on line information and creates a new
match if none have been created"""
def get_game(m, line_type, line):
    if not m:
        q = queries['game type']
        match = q.search(line)
        game_type = match.group(1)
        betting_type = match.group(2)
        blind = [float(match.group(3)), float(match.group(4))]
        m = matches(game_type, betting_type, blind)
    q = queries['game number']
    match = q.search(line)
    game_num = match.group(1)
    q = queries['game time']
    match = q.search(line)
    if match:
        game_time = match.group(1)
        g = game(game_num, game_time)
        m.add_game(g)
    else:
        print(line)
    return m, line_type

"""Creates a new player based on line information. If the player is
the first to be scanned in, then the button is set to that player's
name"""
def get_player(m, line_type, line):
    g = m.get_current_game()
    q = queries['player']
    match = q.search(line)
    if match:
        name = match.group(1)
        money = float(match.group(2))
        p = player(name, money)
        g.add_player(p)
        if g.first_player():
            g.set_button(p.name)
        m.set_current_game(g)
    else:
        print(line)
    return m, line_type

"""Adds a new move to an action using the player name, action and
bet amount. If the action is fold, jump to the hand reveal line type.
If the action is check with no bet amount, bet is set to 0. If posts
is in the action and there are no turns yet, then create a new
turn and append this action to it. """
def get_action(m, line_type, line):
    g = m.get_current_game()
    q = queries['action']
    match = q.search(line)
    a = True
    if match:
        player = match.group(1)
        action = match.group(2)
    else:
        print(line)
    q = queries['bet']
    match = q.search(line)
    if match:
        bet = float(match.group(1))
    elif 'check' in line:
            bet = 0
    elif 'fold' in line:
        bet = None
        line_type = 'hand reveal'
    else:
        a = False
    if action == 'posts' and not g.turns:
        t = turn()
        g.add_turn(t)
    if a:
        t = g.recent_turn()
        t.add_move(player, action, bet)
        g.set_current_turn(t)
        m.set_current_game(g)
    return m, line_type

"""Creates a new turn and adds cards to that turn when applicable"""
def new_phase(m, line_type, line):
    g = m.get_current_game()
    p_t = g.recent_turn()
    t = turn()
    t.add_public_cards(p_t.public_cards)
    if line_type == 'flop':
        q = queries['flop']
        match = q.search(line)
        if match:
            c1 = match.group(1)
            c2 = match.group(2)
            c3 = match.group(3)
            cards = [c1, c2, c3]
            t.add_public_cards(cards)
        else:
            print(line)
    if line_type == 'turn' or line_type == 'river':
        q = queries['turn and river']
        match = q.search(line)
        if match:
            c1 = match.group(1)
            cards = [c1]
            t.add_public_cards(cards)
        else:
            print(line)
    g.add_turn(t)
    m.set_current_game(g)
    return m, line_type

"""Updates a player's hand if they choose to reveal during the game"""
def get_player_hand(m, line_type, line):
    g = m.get_current_game()
    q = queries['player hand']
    match = q.search(line)
    if match:
        pn = match.group(1)
        cards = [match.group(2), match.group(3)]
        for p in g.players:
            if p.name == pn:
                p.add_private_cards(cards)
                m.set_current_game(g)
    else:
        print(line)
    return m, line_type

"""Determines the winner of the game"""
def find_winner(m, line_type, line):
    g = m.get_current_game()
    q = queries['winner']
    match = q.search(line)
    winner = match.group(1)
    g.set_winner(winner)
    m.set_current_game(g)
    return m, line_type

"""Updates the most recent game with it's total pot and rake"""
def get_result(m, line_type, line):
    g = m.get_current_game()
    q = queries['result']
    match = q.search(line)
    if match:
        pot = match.group(1)
        rake = match.group(2)
        g.pot = float(pot)
        g.rake = float(rake)
        m.set_current_game(g)
    else:
        print(line)
    return m, line_type

"""Checks to see if this line one of the types based on the next_line_type
dictionary. If it is, return that line type and true for line_match.
Otherwise, set current_line_type equal to previous line_type and
line_match to false"""
def get_line_type(prev_line_type, line):
    line_match = False
    current_line_type = prev_line_type
    if not prev_line_type:
        current_line_type = 'game'
        line_match = True
    else:
        for line_type in next_line_type[prev_line_type]:
            pattern = line_types[line_type]
            match = pattern.search(line)
            if match:
                if 'action' in line_type and 'collected' in line:
                    pass
                if 'action' in line_type and 'hand' in line:
                    pass
                else:
                    current_line_type = line_type
                    line_match = True
    return (current_line_type, line_match)

# A dictionary of functions to run based on the current line type
line_action = {
    'game': get_game,
    'player': get_player,
    'post action': get_action,
    'hole': new_phase,
    'hole action': get_action,
    'flop': new_phase,
    'flop action': get_action,
    'turn': new_phase,
    'turn action': get_action,
    'river': new_phase,
    'river action': get_action,
    'hand reveal': get_player_hand,
    'winner': find_winner,
    'result': get_result
}

"""Takes in a hand_history_file and output_file_name and parses the
hand_history_file for information related to the games and Exports
it to the output_file in csv form"""
def parse_hand_history(hand_history_file):
    m = None
    prev_line_type = None
    with open(hand_history_file, 'r') as hand_history:
        for line in hand_history:
            line_type, line_match = get_line_type(prev_line_type, line)
            if line_match:
                m, line_type = line_action[line_type](m, line_type, line)
            prev_line_type = line_type
            if len(m.games) > 100:
                m.export_games_to_csv()
    return m

k = parse_hand_history('handHistorySmithy.txt')
