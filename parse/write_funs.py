carh_list = [
    'Ah',
    '2h',
    '3h',
    '4h',
    '5h',
    '6h',
    '7h',
    '8h',
    '9h',
    '10h',
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
    '10c',
    'Jc',
    'Qc',
    'Kc',
    'Ah',
    '2h',
    '3h',
    '4h',
    '5h',
    '6h',
    '7h',
    '8h',
    '9h',
    '10h',
    'Jh',
    'Qh',
    'Kh',
    'As',
    '2s',
    '3s',
    '4s',
    '5s',
    '6s',
    '7s',
    '8s',
    '9s',
    '10s',
    'Js',
    'Qs',
    'Ks'
]

action_list = [
    'check',
    'fold',
    'post'
    'raise'
]

def write_card(w_card, file):
    with open(file) as current_file:
        for r_card in card_list:
            if w_card == r_card:
                current_file.write("1")
            else:
                current_file.write("0")
            if r_card != 'Ks':
                current_file.write(", ")
            else:
                current_file.write("\n")

def write_action(w_action, file):
    with open(file) as current_file:
        for r_action in action_list:
            if w_card == r_card:
                current_file.write("1")
            else:
                current_file.write("0")
            if r_card != 'raise':
                current_file.write(", ")
            else:
                current_file.write("\n")

def write_bet(w_bet, file):
    with open(file) as current_file:
        for r_action in action_list:
            current_file.write(str(w_bet))
            current_file.write("\n")
