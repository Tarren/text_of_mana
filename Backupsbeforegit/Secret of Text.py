import the_map
import sys
import os
import random
import time
from Q2API.util import logging
import traceback
import pygame, pygame.mixer

logger = logging.out_file_instance("Secret_of_Texts")
rooms_by_name = dict()
player_inventory =[]
game_map = None
sword_count = 1
wallet = 0
score = 0

character = {'Player Level': 1, 'Player Exp': 0, 'Next Level': 25, 'player_stats' : {'Strength': 1, 'Dexterity': 1, 'Endurance': 1, 'attack' :[5, 12], 'health': 100}}

def main():
    global game_map
    games = os.listdir("saved_games")
    pygame.mixer.init()
    pygame.init()
    sound = pygame.mixer.Sound('Secret_of_Mana_Opening_Theme.wav')
    sound.play()
    if games:
        for i, file_name in enumerate(games):
            print str(i) + "\t" + file_name.split(".")[0]
        choice = raw_input("choose a game or type 'N' for a new game\n>")
        if choice not in ["N", "n", "new", "NEW"]:
            try:
                game_file = "saved_games\\" + games[int(choice)]
            except:
                print "you failed to type a number. HOW?!?"
                exit()
        else:
            game_file = 'the_map.xml'
    else:
        game_file = 'the_map.xml'

    with open(game_file, 'r') as fin:
        xml_file = fin.read()

    success, game_map = the_map.obj_wrapper(xml_file)

    # build a dictionary that maps room names to room objects
    global rooms_by_name
    for room in game_map.building:
        room_name = room.attrs["room"]
        rooms_by_name[room_name] = room
    # initialize the starting room
    global player
    player = game_map.player[0]
    last_room = None
    starting_room = int(player.attrs["room"])
    current_room = game_map.building[starting_room]
    intro()
    overworld_music(room)
    while True:
        if current_room is not last_room:
            describe(current_room)
        last_room = current_room
        command = raw_input(">")
        verb, noun = parse_command(command)
        os.system('CLS')
        current_room = run_command(current_room, verb, noun)

def battle_music(number, room):
    pygame.mixer.fadeout(500)
    if room.monster[0].attrs['name'] == 'Dark Lich':
        pygame.mixer.init()
        pygame.init()
        sound = pygame.mixer.Sound('The_Oracle_Dark_Lich_Secret_of_Mana.wav')
        sound.set_volume(.35)
        if number == 0:
            sound.play()
        elif number == 1:
            pygame.mixer.fadeout(500)
            overworld_music(room)
        else:
            pygame.mixer.fadeout(500)
            overworld_music(room)

    elif room.monster[0].attrs['name'] == 'Mana Beast':
        pygame.mixer.init()
        pygame.init()
        sound = pygame.mixer.Sound('Secret_of_Mana_Meridian_Dance_sound_remastered_.wav')
        if number == 0:
            sound.play()
        elif number == 1:
            pygame.mixer.fadeout(500)
            overworld_music(room)
        else:
            pygame.mixer.fadeout(500)
            overworld_music(room)

    else:
        if room.monster[0].attrs['boss'] == 'True':
            pygame.mixer.init()
            pygame.init()
            sound = pygame.mixer.Sound('Secret_of_Mana_Dangers.wav')
            if number == 0:
                sound.play()
            elif number == 1:
                pygame.mixer.fadeout(500)
                overworld_music(room)
            else:
                pygame.mixer.fadeout(500)
                overworld_music(room)
        else:
            pygame.mixer.init()
            pygame.init()
            sound = pygame.mixer.Sound('battlemusic.wav')
            if number == 0:
                sound.play()
                sound.set_volume(.15)
            elif number == 1:
                pygame.mixer.fadeout(500)
                overworld_music(room)
            else:
                pygame.mixer.fadeout(500)
                overworld_music(room)

def overworld_music(room):
    pygame.mixer.init()
    pygame.init()
    sound = pygame.mixer.Sound('Into_the_Thick_of_it_Secret_of_Mana_Music.wav')
    sound.set_volume(.15)
    sound.play()

def intro():
    global game_map
    intro_text = game_map.intro[0].text[0].value
    things = intro_text.split('.')
    for words in things:
        print words
        time.sleep(.1)
    time.sleep(1)
    pygame.mixer.fadeout(2000)

def battle_system(room, monsters):
    global player_health
    global player_inventory
    global player_damage
    global character
    global sword_count
    global wallet
    monster = room.monster[0]
    monster_name = monster.attrs["name"]
    monster_damage = int(room.monster[0].attrs['damage'])
    monster_health = room.monster[0].attrs["health"]
    experience = room.monster[0].attrs['exp']
    battle_music(0, room)
    score = int(room.monster[0].attrs['score'])

    print 'You have encountered a ', monster_name
    while character['player_stats']['health'] and monster_health >0:
        if "Rusty Sword" in player_inventory:
            if sword_count == 1:
                character["player_stats"]['attack'] = (character["player_stats"]['attack'][0] + 12) , (character["player_stats"]['attack'][1] + 18)
                sword_count = sword_count + 1
        if "Mana Sword" in player_inventory:
            character["player_stats"]['attack'] = 1000, 1100
        print 'Player Health:', character['player_stats']['health']
        print 'Enemy Health', monster_health
        command = raw_input('What would you like to do>>>')
        verb, noun = parse_command(command)
        if verb == "attack":
            monster_health = damage(character, int(monster_health))
            print 'You attack the ', monster_name
            if monster_health >= 0:
                dodge_chance = random.randint( 0, (100 / character['player_stats']['Dexterity']))
                if dodge_chance == 25:
                    print monster_name, 'misses you'
                else:
                    character['player_stats']['health'] = character['player_stats']['health'] - monster_damage
        elif verb == 'run':
            print 'Cannot escape'

        elif verb in ['use', 'Use']:
            if noun == 'Candy' and 'Candy' in player_inventory:
                candy_system(room, noun)
            else:
                print "You cannot use that item"
        else:
            print 'What are you thinking?!?'
            print monster_name, "attacks you for ", monster_damage, "while you are fumbling around."
            character['player_stats']['health'] = character['player_stats']['health'] - monster_damage

        if character['player_stats']['health'] <=0:
            print 'You have been eaten by a ', monster_name
            print "Game Over"
            raw_input('...')
            break

        if monster_health <= 0:
            print 'You have beaten a', monster_name
            print ''
            print 'You have', character['player_stats']['health'], 'health remaining'
            print ''
            experience_system(int(experience))
            gold = room.monster[0].attrs['gold']
            wallet_system(gold)
            battle_music(69, room)
            score_system(room, score)
            # end_the_game(room)
            if room.monster[0].attrs['boss'] == 'True':
                room.monster.remove(monster)
            else:
                pass
            return

def experience_system(gained_exp):
    global character
    base_health = 100
    print "You gained,", gained_exp, "experience."
    nstr, ndex, nint = 0, 0, 0
    character["Player Exp"]+= gained_exp
    while character['Player Exp'] >= character['Next Level']:
        character["Player Level"] += 1
        character["Player Exp"] = character["Player Exp"] - character["Next Level"]
        character["Next Level"] = round(character["Next Level"] * 1.5)
        nstr = random.randint(1 , 5)
        ndex = random.randint(1 , 5)
        nint = random.randint(1 , 20)
        #Prints stat gain
        character['player_stats']['Strength'] += nstr
        character['player_stats']['Dexterity'] += ndex
        character['player_stats']['Endurance'] += nint
        character['player_stats']['attack'] = (character['player_stats']['attack'][0] + (character['player_stats']['Strength']), (character['player_stats']['attack'][1] + character['player_stats']['Strength'] * 2))
        character["player_stats"]['health'] = base_health + (character['player_stats']['Endurance'] * 2)
        print "Player Level:", character["Player Level"]
        print 'Experience Needed To Next Level:', int(character['Next Level']) - int(character["Player Exp"])
        print ''
        print 'Strength Gain:', nstr
        print "Dexterity Gain:", ndex
        print "Endurance Gain:", nint
        print "Characters New Max Health:", character["player_stats"]['health']
        print ''


        ###MAKE INTERLLIGINCE HEALTH
        ### enemy is based of off nested enemy script. It it exists great, if not, it wont print, thats how the plot will work.
        ### for example, <enemy>
        ###                 <text>

def inn_system(room):
    global character
    global wallet
    base_health = 100
    print "It cost ten gold to stay at the inn, would you like to stay?"
    choice = raw_input('>')
    if choice in ["yeah", "Yes", "yes", "Yeah", "Y"]:
        if wallet >= 10:
            pygame.mixer.init()
            pygame.init()
            sound = pygame.mixer.Sound('Close_Your_Eyelids_Secret_of_Mana_Music.wav')
            sound.play()
            wallet = wallet - 10
            character['player_stats']['health'] = character["player_stats"]['health'] = base_health + (character['player_stats']['Endurance'] * 2)
            print 'You stay at the inn and feel well rested.'
            print 'Hp fully recovered.'
            save_game(room)
            time.sleep(5)
            pygame.mixer.fadeout(2000)
            return room
        else:
            print 'You do not have enough money'
            return room
    else:
        return room

def score_system(room, enemy_score):
    global score
    score = score + enemy_score
    print 'Score:', score


def save_game(room):
    print 'Would you like to save your game?'
    choice = raw_input('>>>')
    if choice in ['yes', 'Yes', 'yeah', 'Yeah', 'y', 'Y']:
        room_idx = game_map.building.index(room)
        player.attrs["room"] = str(room_idx)
        save_file = raw_input("enter a name for the save file>")
        game_data = game_map.flatten_self()
        with open("saved_games\\" + save_file + ".xml", "w") as f:
            f.write(game_data)
            print "game saved!"
            return room
    else:
        pass
        return room

def wallet_system(gold):
    global wallet
    wallet = int(wallet) + int(gold)

def damage(attacker, defender):

    if random.randint(0, 100) > 95:
        damage = random.randint(attacker['player_stats']['attack'][0], attacker['player_stats']['attack'][1]) *2
        print 'You scored a critical hit'
    else:
        damage = random.randint(attacker['player_stats']['attack'][0], attacker['player_stats']['attack'][1]) * 1.1
    print 'You have done', damage, 'damage'
    defender = defender - damage

    return defender

def describe(room):
    print room.text[0].value
    if room.item:
        print '***************Items***************'
        item_text = "You see"
        for item in room.item:
            item_text += " a " + item.attrs["name"]
        print item_text
    if room.exit:
        print '***************Exits***************'
        for exit in room.exit:
            room_text = 'You see the '
            room_text += exit.attrs["name"] + ' to your ' + exit.attrs["dir"]
            print room_text
    print '***********************************'

def town_text(room):
    words = room.town_text[0].value
    things = words.split('.')
    for word in things:
        print word
        time.sleep(2)
    room.town_text.remove(room.town_text[0])
def parse_command(command):
    words = command.split()
    if len(words) < 1:
        words = ["BAD_COMMAND"]
    verb = words[0]
    noun = " ".join(words[1:])
    return verb, noun

def candy_system(room, noun):
    global character
    global player_inventory
    base_health = 100
    if noun in player_inventory:
        if noun == 'Candy':
            character['player_stats']['health'] = character["player_stats"]['health'] = base_health + (character['player_stats']['Endurance'] * 2)
            print 'Hp Restored To:', character['player_stats']['health']
            player_inventory.remove('Candy')
        if noun == 'Health Boost':
            character['player_stats']['Endurance'] = character['player_stats']['Endurance'] + 5
            player_inventory.remove('Health Boost')
        if noun == 'Strength Boost':
            character['player_stats']['Strength'] = character['player_stats']['Strength'] + 5
            player_inventory.remove('Strength Boost')
        if noun == 'Agility Boost':
            character['player_stats']['Dexterity'] = character['player_stats']['Dexterity'] + 5
            player_inventory.remove('Agility Boost')

        print character


def store_system():
    global wallet
    global player_inventory

    print 'You have', wallet, 'gold'
    print 'This is what we have in stock:'
    print '1. Candy'
    print 'Cost: 10 Gold'
    print '****************'
    print '2. Health Boost'
    print 'Cost: 500 Gold'
    print '****************'
    print '3. Strength Boost'
    print 'Cost: 500 Gold'
    print '****************'
    print '4. Agility Boost'
    print 'Cost: 500 Gold'
    choice = raw_input('>>>')
    if choice in ['1', 'candy', 'Candy']:
        if wallet >= 10:
            player_inventory.append('Candy')
            wallet = wallet - 10
        else:
            print 'Sorry, you do not have enough gold.'
    if choice in ['2', 'health boost', 'health Boost', 'Health boost', 'Health', 'Health Boost', 'health']:
        if wallet >= 10:
            player.inventory.append('Health Boost')
            wallet = wallet - 500
        else:
            print 'Sorry, you do not have enough gold.'
    if choice in ['3', 'Strength Boost', 'Strength boost', 'strength Boost', 'Strength', 'strength']:
        if wallet >= 10:
            player_inventory.append('Strength Boost')
            wallet = wallet - 500
        else:
            print 'Sorry, you do not have enough gold.'
    if choice in ['4', 'Agility Boost', 'Agility boost', 'agility Boost', 'Agility', 'agility']:
        if wallet >= 10:
            player_inventory.append('Agility Boost')
            wallet = wallet - 500
        else:
            print 'Sorry, you do not have enough gold.'


def end_the_game(room):
    if room.monster[0].attrs['endcode']:
        if room.monster[0].attrs['endcode'] == '1':
            print 'The game is over!!!'
        else:
            pass

def run_command(room, verb, noun):
    global player
    global player_inventory
    global wallet

    exits, items, locked, reqs, monsters = get_room_data(room)
    #hopefully one day will check to see if doors are locked, and if so, let me pass through them if I have the key.
    if room.town_text:
        town_text(room)
        describe(room)
    if monsters:
        battle_system(room, monsters)
    if verb in ["go", "g", "walk", "run", "sprint", "w", "r", "s"]:
        room_exit = exits.get(noun, None)
        if room_exit:
            lock = locked.get(room_exit.attrs["name"])
            if lock == 'True':
                req = reqs[room_exit.attrs["name"]]
                if req == "None" or req in player_inventory:
                    # print 'You unlocked the', room_exit.attrs["name"]
                    return rooms_by_name[room_exit.attrs["link"]]
                else:
                    print room_exit.attrs["name"], 'is blocked, you cannot pass.'
                    return room
            else:
                print 'You pass through the', room_exit.attrs["name"]
                return rooms_by_name[room_exit.attrs["link"]]
        else:
            print "You can't go there."
            return room
        #look to see if there are items in the room, and add them to inventory
    elif verb in ["look", "Look", "LOOK", "inspect", "Inspect", "INSPCET"]:
        if noun:
            if noun in items:
                item = items[noun]
                print item.value
            elif noun in exits:
                exit = exits[noun]
                print exit.attrs.get("name", "you see nothing")
            else:
                print "you see nothing"
        else:
            describe(room)

        return room
    elif verb in ["take", "get", 'grab', 'Take', 'Get', 'Grab', 'obtain', 'Obtain'] :
        if noun in items:
            for name, item in items.iteritems():
                print "You have taken the" , name
                player_inventory.append(name)
                room.item.remove(item)
                return room
        else:
            return room

    elif verb == "save":
        room_idx = game_map.building.index(room)
        player.attrs["room"] = str(room_idx)
        save_file = raw_input("enter a name for the save file>")
        game_data = game_map.flatten_self()
        with open("saved_games\\" + save_file + ".xml", "w") as f:
            f.write(game_data)
        print "game saved!"
        return room

    elif verb == "quit":
        print 'Sorry to see you go, goodbye'
        sys.exit()

    elif verb in ["stay", "Stay", "Sleep", "sleep"]:
            print room.room_name[0].value
            if room.room_name[0].value in ['Potos Inn', 'Pandora Inn', 'Dwarf Village Inn', 'Kakkara Inn', 'Mandala Inn','Gold Island Inn']:
                inn_system(room)
            return room
    elif verb in ["shop", "Shop", "Buy", "buy"]:
        if room.room_name[0].value in ['Potos Inn', 'Pandora Inn', 'Dwarf Village Inn', 'Kakkara Inn', 'Mandala Inn','Gold Island Inn']:
            store_system()
            return room

    elif verb == "stats" or verb == "Stats":
        print character
        print "You have", wallet, "gold"
        return room

        #brief help guide
    elif verb in ["help", "Help", "HELP", "HElp"]:
        print "The game is fairly simple to play."
        print "Commands generally break down to: look, go, or, take"
        print "Also, if you would like to view your inventory, enter a capital 'I'"
        print 'Try sleeping in or staying in inns'
        return room

    elif verb in ['use', 'Use']:
            candy_system(room, noun)
            return room

    elif verb in ["i", "I", "inv", "INV", "inventory"]:
        print "Your inventory contains:   "
        print ", ".join(player_inventory)
        return room

    else:
        print "unrecognized command"
        return room

def get_room_data(room):
    exits = dict()
    for room_exit in room.exit:
        exits[room_exit.attrs["name"]] = room_exit
        exits[room_exit.attrs["dir"]] = room_exit

    monster_dict = dict()
    for monster in room.monster:
        monster_dict[monster.attrs['name']] = monster

    items = dict()
    for item in room.item:
        items[item.attrs["name"]] = item

    pre_req_dict=dict()
    for room_exit in room.exit:
        pre_req_dict[room_exit.attrs["name"]] = room_exit.attrs["req"]

    locked = dict()
    for room_exit in room.exit:
        locked[room_exit.attrs["name"]] = room_exit.attrs["locked"]

    return exits, items , locked, pre_req_dict, monster_dict
if __name__ =="__main__":
    try:
        main()
    except:
        exception_string = traceback.format_exc()
        logger.write_line([exception_string])
        print exception_string
