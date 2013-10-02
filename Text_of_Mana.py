import the_map
import sys
import os
import random
import time
from Q2API.util import logging
import traceback
from ast import literal_eval
from operator import itemgetter
import pygame, pygame.mixer

logger = logging.out_file_instance("Secret_of_Texts")
rooms_by_name = dict()
boss_count = 0
player_inventory =[]
player = None
game_map = None
sword_count = 1
mana_sword = 1
wallet = 0
score = 0
party = []
hero_in_party = False
princess_in_party = False
sprite_in_party = False

def main():
    global game_map
    global player_inventory
    global wallet

    games = os.listdir("saved_games")
    pygame.mixer.init()
    pygame.init()
    pygame.mixer.fadeout(500)
    sound = pygame.mixer.Sound('Secret_of_Mana_Opening_Theme.wav')
    sound.play(loops = 5)
    if games:
        for i, file_name in enumerate(games):
            print str(i) + "\t" + file_name.split(".")[0]
        choice = raw_input("choose a game or type 'N' for a new game\n>")
        if choice not in ["N", "n", "new", "NEW"]:
            try:
                game_file = "saved_games\\" + games[int(choice)]
                pygame.mixer.fadeout(500)
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
    player_inventory = game_map.player[0].item[0].attrs['name']
    wallet = game_map.player[0].attrs['wallet']
    wallet = int(wallet)
    #player_inventory = game_map.player[0].inventory[0]
    last_room = None
    starting_room = int(player.attrs["room"])
    current_room = game_map.building[starting_room]

    intro()
    overworld_music(room)
    load_party(room)
    while True:
        party_builder(room)
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
            sound = pygame.mixer.Sound('Secret of Mana - Danger [Boss Theme].wav')
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
            sound = pygame.mixer.Sound('Battle Theme.wav')
            if number == 0:
                sound.play()
                sound.set_volume(.15)
            elif number == 1:
                pygame.mixer.fadeout(500)
                overworld_music(room)
            else:
                pygame.mixer.fadeout(500)
                overworld_music(room)

def party_builder(room):
    global game_map
    global Hero
    global Princess
    global Sprite
    global party
    global hero_in_party
    global princess_in_party
    global sprite_in_party
    Hero = {'Name': game_map.player[0].attrs['name'], 'Player Level': game_map.player[0].attrs['level'], 'Player Exp': game_map.player[0].attrs['playerxp'], 'Next Level': game_map.player[0].attrs['Nextlvl'], 'player_stats' : {'Strength': game_map.player[0].attrs['strength'], 'Dexterity': game_map.player[0].attrs['dexterity'], 'Endurance': game_map.player[0].attrs['endurance'], 'attack' :game_map.player[0].attrs['attack1'], 'baseattack' :game_map.player[0].attrs['attack2'], 'health': 100}}
    Princess = {'Name': game_map.player[1].attrs['name'],'Player Level': game_map.player[1].attrs['level'], 'Player Exp': game_map.player[1].attrs['playerxp'], 'Next Level': game_map.player[1].attrs['Nextlvl'], 'player_stats' : {'Strength': game_map.player[1].attrs['strength'], 'Dexterity': game_map.player[1].attrs['dexterity'], 'Endurance': game_map.player[1].attrs['endurance'], 'attack' :game_map.player[1].attrs['attack1'], 'baseattack' :game_map.player[1].attrs['attack2'], 'health': 100}}
    Sprite = {'Name': game_map.player[2].attrs['name'],'Player Level': game_map.player[2].attrs['level'], 'Player Exp': game_map.player[2].attrs['playerxp'], 'Next Level': game_map.player[2].attrs['Nextlvl'], 'player_stats' : {'Strength': game_map.player[2].attrs['strength'], 'Dexterity': game_map.player[2].attrs['dexterity'], 'Endurance': game_map.player[2].attrs['endurance'], 'attack' :game_map.player[2].attrs['attack1'], 'baseattack' :game_map.player[2].attrs['attack2'], 'health': 100}}
    if room.party:
        if room.party[0].attrs['member'] == '0':
            if hero_in_party == False:
                party.append(Hero)
                print ''
                print '*****************************'
                print game_map.player[0].attrs['name'], 'has joined your party.'
                print '*****************************'
                print ''
                game_map.party[0].attrs['length'] = '1'
                hero_in_party = True
                for member in room.party:
                    room.party.remove(member)

        elif room.party[0].attrs['member'] == '1':
            if sprite_in_party == False:
                party.append(Sprite)
                print ''
                print '*****************************'
                print game_map.player[2].attrs['name'], 'has joined your party.'
                print '*****************************'
                print ''
                sprite_in_party = True
                game_map.party[0].attrs['length'] = '2'
                for member in room.party:
                    room.party.remove(member)

        elif room.party[0].attrs['member'] == '2':
            if princess_in_party == False:
                party.append(Princess)
                print ''
                print '*****************************'
                print game_map.player[1].attrs['name'], 'has joined your party.'
                print '*****************************'
                print ''
                princess_in_party = True
                game_map.party[0].attrs['length'] = '3'
                for member in room.party:
                    room.party.remove(member)
        else:
            pass

def load_party(room):
    global Hero
    global Princess
    global Sprite
    global hero_in_party
    global sprite_in_party
    global princess_in_party
    Hero = {'Name': game_map.player[0].attrs['name'], 'Player Level': game_map.player[0].attrs['level'], 'Player Exp': game_map.player[0].attrs['playerxp'], 'Next Level': game_map.player[0].attrs['Nextlvl'], 'player_stats' : {'Strength': game_map.player[0].attrs['strength'], 'Dexterity': game_map.player[0].attrs['dexterity'], 'Endurance': game_map.player[0].attrs['endurance'], 'attack' :game_map.player[0].attrs['attack1'], 'health': 100}}
    Princess = {'Name': game_map.player[1].attrs['name'],'Player Level': game_map.player[1].attrs['level'], 'Player Exp': game_map.player[1].attrs['playerxp'], 'Next Level': game_map.player[1].attrs['Nextlvl'], 'player_stats' : {'Strength': game_map.player[1].attrs['strength'], 'Dexterity': game_map.player[1].attrs['dexterity'], 'Endurance': game_map.player[1].attrs['endurance'], 'attack' :game_map.player[1].attrs['attack1'], 'health': 100}}
    Sprite = {'Name': game_map.player[2].attrs['name'],'Player Level': game_map.player[2].attrs['level'], 'Player Exp': game_map.player[2].attrs['playerxp'], 'Next Level': game_map.player[2].attrs['Nextlvl'], 'player_stats' : {'Strength': game_map.player[2].attrs['strength'], 'Dexterity': game_map.player[2].attrs['dexterity'], 'Endurance': game_map.player[2].attrs['endurance'], 'attack' :game_map.player[2].attrs['attack1'], 'health': 100}}
    if game_map.party[0].attrs['length'] == '1':

        party.append(Hero)

        game_map.party[0].attrs['length'] = '1'
        hero_in_party = True

    elif  game_map.party[0].attrs['length'] == '2':
        party.append(Hero)

        party.append(Sprite)

        hero_in_party = True
        sprite_in_party = True

    elif game_map.party[0].attrs['length'] == '3':
        party.append(Hero)

        party.append(Sprite)

        party.append(Princess)

        hero_in_party = True
        sprite_in_party = True
        princess_in_party = True

def overworld_music(room):
    global boss_count
    #put in random to have more than one fucking song
    if boss_count < 3:
        pygame.mixer.init()
        pygame.init()
        sound = pygame.mixer.Sound('Into_the_Thick_of_it_Secret_of_Mana_Music.wav')
        sound.set_volume(.15)
        sound.play(loops = 2)
    if boss_count > 3:
        if boss_count <= 6:
            pygame.mixer.init()
            pygame.init()
            sound = pygame.mixer.Sound('What the Forest Taught Me- Secret of Mana Music.wav')
            sound.set_volume(.15)
            sound.play(loops = 2)
    if boss_count > 6:
        if boss_count <= 9:
            pygame.mixer.init()
            pygame.init()
            sound = pygame.mixer.Sound('Secret Of Mana Soundtrack- Eternal Recurrence (1080p).wav')
            sound.set_volume(.15)
            sound.play(loops = 2)
    if boss_count > 9:
        pygame.mixer.init()
        pygame.init()
        sound = pygame.mixer.Sound('Still_Of_The_Night_1080p.wav')
        sound.set_volume(.15)
        sound.play(loops = 2)

def intro():
    global game_map
    try:
        item = game_map.intro[0]
        intro_text = game_map.intro[0].text[0].value
        things = intro_text.split('.')
        for words in things:
            print words
            time.sleep(2.0)
        choice = raw_input('Press Enter to continue>>>')
        game_map.intro.remove(item)
        game_map.children.remove(item)
        pygame.mixer.fadeout(2000)
    except:
        pass

def battle_system(room, monsters):
    global player_inventory
    global sword_count
    global mana_sword
    global wallet
    global boss_count
    monster = room.monster[0]
    monster_name = monster.attrs["name"]
    monster_damage = int(room.monster[0].attrs['damage'])
    monster_health = room.monster[0].attrs["health"]
    experience = room.monster[0].attrs['exp']
    battle_music(0, room)
    score = int(room.monster[0].attrs['score'])
    for character in party:
        if len(party) == 1:
            character1 = party[0]
        if len(party) == 2:
            character1 = party[0]
            character2 = party[1]
        if len(party) == 3:
                character1 = party[0]
                character2 = party[1]
                character3 = party[2]
        else:
            pass
    for character in party:
        character["player_stats"]['attack'] = int(character["player_stats"]['attack'])
        print '****************Battle******************'
        print 'You have encountered a ', monster_name
        while character['player_stats']['health'] and monster_health >0:
            for inv in game_map.player[0].item:
                if "rusty sword" in inv.attrs['name']:
                    if sword_count == 1:
                        character["player_stats"]['attack'] = (character["player_stats"]['attack'] + 18)
                        sword_count = sword_count + 1
                if "Mana Sword" in inv.attrs['name']:
                    if mana_sword == 1:
                        character["player_stats"]['attack'] = character["player_stats"]['attack'] + 1100
                        mana_sword = 2
            for character in party:
                print '****************************************'
                print character['Name'], 'has', character['player_stats']['health'], 'health remaining'
            print '****************************************'
            print ''
            print 'Enemy Health', monster_health
            command = raw_input('What would you like to do>>>')
            verb, noun = parse_command(command)
            attack_number = 0
            for character in party:
                if verb in ["attack", "fight", "a", "f", 'poop',]:
                    monster_health = damage(character, int(monster_health))
                    if monster_health >= 0:
                        character['player_stats']['Dexterity'] = int(character['player_stats']['Dexterity'])
                        dodge_chance = random.randint( 0, (100 / character['player_stats']['Dexterity']))
                        if dodge_chance == 25:
                            print monster_name, 'misses you'
                        else:
                            if attack_number == 0:
                                if len(party) == 1:
                                    character1['player_stats']['health'] = character1['player_stats']['health'] - monster_damage
                                    attack_number = attack_number + 1
                                if len(party) == 2:
                                    choice = random.randint(1,2)
                                    if choice == 1:
                                        character1['player_stats']['health'] = character1['player_stats']['health'] - monster_damage
                                        attack_number = attack_number + 1
                                    if choice ==2:
                                        character2['player_stats']['health'] = character2['player_stats']['health'] - monster_damage
                                        attack_number = attack_number + 1
                                if len(party) == 3:
                                    choice = random.randint(1,3)
                                    if choice == 1:
                                        character1['player_stats']['health'] = character1['player_stats']['health'] - monster_damage
                                        attack_number = attack_number + 1
                                    if choice == 1:
                                        character2['player_stats']['health'] = character2['player_stats']['health'] - monster_damage
                                        attack_number = attack_number + 1
                                    if choice == 1:
                                        character3['player_stats']['health'] = character3['player_stats']['health'] - monster_damage
                                        attack_number = attack_number + 1
                                    else:
                                        print monster_name, 'misses you'

                elif verb == 'run':
                    print 'Cannot escape'

                elif verb == 'go':
                    if noun == 'super saiyin':
                        print 'not fair... you win...'
                        sys.exit()

                elif verb in ['use', 'Use']:
                    if noun == 'candy' and 'candy' in player.item:
                        candy_system(room, noun)
                    else:
                        print "You cannot use that item"
                else:
                    print 'What are you thinking?!?'
                    print monster_name, "attacks you for ", monster_damage, "while you are fumbling around."
                    character['player_stats']['health'] = character['player_stats']['health'] - monster_damage

            if character['player_stats']['health'] <=0:
                pygame.mixer.fadeout(2000)
                print 'You have been eaten by a ', monster_name
                print "Game Over"
                pygame.mixer.init()
                pygame.init()
                sound = pygame.mixer.Sound('Close_Your_Eyelids_Secret_of_Mana_Music.wav')
                sound.play()
                high_score()
                raw_input('...')
                sys.exit()

            elif monster_health <= 0:
                print 'You have beaten a', monster_name
                print ''
                print 'You have', character['player_stats']['health'], 'health remaining'
                print ''
                experience_system(int(experience))
                gold = room.monster[0].attrs['gold']
                wallet_system(gold)
                battle_music(69, room)
                score_system(room, score)
                end_the_game(room)
                    # end_the_game(room)
                if room.monster[0].attrs['boss'] == 'True':
                    room.monster.remove(monster)
                    room.children.remove(monster)
                    boss_count = boss_count + 1
                else:
                    pass
                return

def experience_system(gained_exp):
    global party
    base_health = 100
    print "You gained,", gained_exp, "experience."
    nstr, ndex, nint = 0, 0, 0
    for characters in party:
        characters["Player Exp"] = int(characters["Player Exp"]) + gained_exp
        characters["Next Level"] = int(characters["Next Level"])
        base_attack = int(characters['player_stats']['baseattack'])
        while characters['Player Exp'] >= characters['Next Level']:
            print '***********************************'
            print 'Character Name:',characters["Name"]
            characters["Player Level"] = int(characters["Player Level"]) + 1
            characters["Player Exp"] = characters["Player Exp"] - characters["Next Level"]
            characters["Next Level"] = round(characters["Next Level"] * 1.4)
            nstr = random.randint(1 , 5)
            ndex = random.randint(1 , 5)
            nint = random.randint(1 , 15)
            #Prints stat gain
            characters['player_stats']['Strength'] = int(characters['player_stats']['Strength']) + nstr
            characters['player_stats']['Dexterity'] = int(characters['player_stats']['Dexterity']) + ndex
            characters['player_stats']['Endurance'] = int(characters['player_stats']['Endurance']) +nint
            characters['player_stats']['attack'] = int(characters['player_stats']['attack'])
            characters['player_stats']['attack'] = base_attack + (characters['player_stats']['Strength'])
            characters["player_stats"]['health'] = base_health + (characters['player_stats']['Endurance'] * 2)
            print "Player Level:", characters["Player Level"]
            print 'Experience Needed To Next Level:', int(characters['Next Level']) - int(characters["Player Exp"])
            print 'Strength Gain:', nstr
            print "Dexterity Gain:", ndex
            print "Endurance Gain:", nint
            print "Characters New Max Health:", characters["player_stats"]['health']
            print ''

            if characters["Name"] == 'Hero':
                level= str(characters["Player Level"])
                strength = str(characters['player_stats']['Strength'])
                endurance = str(characters['player_stats']['Endurance'])
                dexterity = str(characters['player_stats']['Dexterity'])

                game_map.player[0].attrs['level'] = level
                game_map.player[0].attrs['strength'] = strength
                game_map.player[0].attrs['endurance'] = endurance
                game_map.player[0].attrs['dexterity'] = dexterity


            elif characters["Name"] == 'Princess':
                level= str(characters["Player Level"])
                strength = str(characters['player_stats']['Strength'])
                endurance = str(characters['player_stats']['Endurance'])
                dexterity = str(characters['player_stats']['Dexterity'])

                game_map.player[1].attrs['level'] = level
                game_map.player[1].attrs['strength'] = strength
                game_map.player[1].attrs['endurance'] = endurance
                game_map.player[1].attrs['dexterity'] = dexterity

            elif characters["Name"] == 'Sprite':
                level= str(characters["Player Level"])
                strength = str(characters['player_stats']['Strength'])
                endurance = str(characters['player_stats']['Endurance'])
                dexterity = str(characters['player_stats']['Dexterity'])

                game_map.player[2].attrs['level'] = level
                game_map.player[2].attrs['strength'] = strength
                game_map.player[2].attrs['endurance'] = endurance
                game_map.player[2].attrs['dexterity'] = dexterity
            else:
                pass

def inn_system(room):
    global wallet
    base_health = 100
    pygame.mixer.fadeout(500)
    print "It cost ten gold to stay at the inn, would you like to stay?"
    choice = raw_input('>')
    if choice in ["yeah", "Yes", "yes", "Yeah", "Y"]:
        if wallet >= 10:
            pygame.mixer.init()
            pygame.init()
            sound = pygame.mixer.Sound('Close_Your_Eyelids_Secret_of_Mana_Music.wav')
            sound.play()
            wallet = wallet - 10
            for character in party:
                character["player_stats"]['health'] = base_health + int((character['player_stats']['Endurance'] * 2))
            print 'You stay at the inn and feel well rested.'
            print 'Hp fully recovered.'
            save_game(room)
            time.sleep(5)
            pygame.mixer.fadeout(2000)
            overworld_music(room)
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
    game_map.player[0].attrs['wallet'] = str(wallet)

def damage(attacker, defender):
    global party
    attacker['player_stats']['attack'] = int(attacker['player_stats']['attack'])
    if random.randint(0, 100) > 95:
        damage = random.randint(attacker['player_stats']['attack']-5, attacker['player_stats']['attack'] + 15) * 2
        print 'You scored a critical hit'
        print 'You have done', damage, 'damage'
        pygame.mixer.init()
        pygame.init()
        sound = pygame.mixer.Sound('rage_of_blades-Blaga_Saun-1763516257.wav')
        sound.set_volume(.45)
        sound.play()
    else:
        damage = round(random.randint(attacker['player_stats']['attack'] + 5, attacker['player_stats']['attack'] + 10) * 1.4)
        print attacker['Name'], 'has done', damage, 'damage'
        pygame.mixer.init()
        pygame.init()
        sound = pygame.mixer.Sound('Swoosh 3-SoundBible.com-1573211927.wav')
        sound.set_volume(.45)
        sound.play()
    defender = defender - damage

    return defender

def describe(room):
    global player_inventory
    print room.text[0].value
    if room.item:
        print '***************Items***************'
        print ''
        item_text = "You see"
        for item in room.item:
            item_text += " a " + item.attrs["name"]
        print item_text
    if room.exit:
        print ''
        print '***************Exits***************'
        print ''
        for exit in room.exit:
            room_text = 'You see the '
            room_text += exit.attrs["name"] + ' to your ' + exit.attrs["dir"]
            print room_text
    print ''
    print '***********************************'
    print ''

def town_text(room):
    words = room.town_text[0].value
    things = words.split('.')
    for word in things:
        print word
        time.sleep(1.5)
    choice = raw_input('Press Enter to continue>>>')
    room.children.remove(room.town_text[0])
    room.town_text.remove(room.town_text[0])

def parse_command(command):
    words = command.split()
    if len(words) < 1:
        words = ["BAD_COMMAND"]
    verb = words[0]
    noun = " ".join(words[1:])
    return verb, noun

def candy_system(room, noun):
    base_health = 100
    for inv in game_map.player[0].item:
        name = inv.attrs['name']
        for character in party:
            if noun == 'candy' and noun in name:
                character['player_stats']['health'] = base_health + int((character['player_stats']['Endurance'] * 2))
                print 'Hp Restored To:', character['player_stats']['health']
                game_map.player[0].item.remove(inv)
    else:
        pass

def store_system():
    global wallet
    global player_inventory
    pass
    # print 'You have', wallet, 'gold'
    # print 'This is what we have in stock:'
    # print '****************'
    # print '1. Candy'
    # print 'Cost: 10 Gold'
    # print '****************'
    # print '2. Health Boost'
    # print 'Cost: 500 Gold'
    # print '****************'
    # print '3. Strength Boost'
    # print 'Cost: 500 Gold'
    # print '****************'
    # print '4. Agility Boost'
    # print 'Cost: 500 Gold'
    # choice = raw_input('>>>')
    # if choice in ['1', 'candy', 'Candy']:
    #     if wallet >= 10:
    #         player.item.append('candy')
    #         player.children.append('candy')
    #         wallet = wallet - 10
    #     else:
    #         print 'Sorry, you do not have enough gold.'
    # if choice in ['2', 'health boost', 'health Boost', 'Health boost', 'Health', 'Health Boost', 'health']:
    #     if wallet >= 10:
    #         player.inventory.append('Health Boost')
    #         wallet = wallet - 500
    #     else:
    #         print 'Sorry, you do not have enough gold.'
    # if choice in ['3', 'Strength Boost', 'Strength boost', 'strength Boost', 'Strength', 'strength']:
    #     if wallet >= 10:
    #         player_inventory.append('Strength Boost')
    #         wallet = wallet - 500
    #     else:
    #         print 'Sorry, you do not have enough gold.'
    # if choice in ['4', 'Agility Boost', 'Agility boost', 'agility Boost', 'Agility', 'agility']:
    #     if wallet >= 10:
    #         player_inventory.append('Agility Boost')
    #         wallet = wallet - 500
    #     else:
    #         print 'Sorry, you do not have enough gold.'

def end_the_game(room):
    global score
    if room.monster[0].attrs['name'] == 'Mana Beast':
        pygame.mixer.fadeout(500)
        print 'The game is over!!!'
        pygame.mixer.init()
        pygame.init()
        sound = pygame.mixer.Sound('The Second Truth From The Left (1080p).wav')
        sound.play()
        high_score()
        time.sleep(6)
        print ''
        print 'Thanks to the developers at Square for creating one of the greatest games of all time.'
        print ''
        time.sleep(8)
        print 'Thanks to the members of Project R and Abe for helping the game come together and actually being playable... '
        print ''
        time.sleep(8)
        print 'Hope the music and battle system wasnt too annoying.'
        time.sleep(8)
        print ''
        print score
        choice = raw_input('>>>')
        sys.exit()
    else:
        pass

def run_command(room, verb, noun):
    global player
    global player_inventory
    global wallet
    global party
    global game_map

    exits, items, locked, reqs, monsters = get_room_data(room)
    #hopefully one day will check to see if doors are locked, and if so, let me pass through them if I have the key.
    if room.town_text:
        town_text(room)

    if monsters:
        chance = random.randint(1,5)
        if room.monster[0].attrs['boss'] == 'True':
            print 'boss batter'
            battle_system(room, monsters)

        elif chance in [1,2,3]:
            print 'normal battle'
            battle_system(room, monsters)

        else:
            print 'skipped battle'
            pass

    if room.party:
        party_builder(room)

    if verb in ["go", "g", "walk", "run", "sprint", "w", "r", "s"]:
        room_exit = exits.get(noun, None)
        if room_exit:
            lock = locked.get(room_exit.attrs["dir"])
            if lock == 'True':
                req = reqs[room_exit.attrs["name"]]
                for inv in game_map.player[0].item:
                    name = inv.attrs['name']
                    if req == "None" or req in name:
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
    elif verb in ["look", "Look", "LOOK", "inspect", "Inspect", "INSPECT"]:
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
                item = items[noun]
                player.item.append(item)
                player.children.append(item)
                room.item.remove(item)
                room.children.remove(item)
                print "You "+verb+" the "+item.attrs["name"]+"."
                describe(room)

                return room

        else:
            print "you can't "+verb+" that."
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
        for character in party:
            print character['Name']
            print '*************************'
            print "Level:", character['Player Level']
            print "Strength:", character['player_stats']['Strength']
            print "Dexterity:", character['player_stats']['Dexterity']
            print "Endurance:", character['player_stats']['Endurance']
            print ''

        print "*******************"
        print "You have", wallet, "gold"
        return room

        #brief help guide
    elif verb in ["help", "Help", "HELP", "HElp"]:
        print "The game is fairly simple to play."
        print ''
        print "Commands generally break down to: look, go, or, take"
        print ''
        print "For example, if you see a rusty sword on the ground, try typing, 'take rusty sword' "
        print ''
        print "Navigation works similarly, try typing, 'go north, go east, go west, or go south'"
        print ''
        print "If you ever find yourself lost, try typing in, 'look'"
        print ''
        print "Try sleeping or shopping in hotels, and you can save your game anytime by typing in 'save'"
        print ''
        print "Also, if you would like to view your inventory, enter a capital 'I'"
        print ''
        print 'Try sleeping in or staying in inns'
        print ''
        return room

    elif verb in ['use', 'Use']:
        if noun == 'flammie drum':
            for inv in game_map.player[0].item:
                name = inv.attrs['name']
                if 'flammie drum' in name:
                    return rooms_by_name[game_map.building[1].attrs['room']]
            else:
                return room
        else:
            candy_system(room, noun)
            return room

    elif verb in ["i", "I", "inv", "INV", "inventory"]:
        print "Your inventory contains:   "
        for inv in game_map.player[0].item:
            print inv.attrs['name']
        return room
    elif verb == 'play':
        if noun == 'music':
            print 'which song?'
            choice = raw_input('>>>')
            if choice == '1':
                pygame.mixer.fadeout(500)
                pygame.mixer.init()
                pygame.init()
                sound = pygame.mixer.Sound('The_Oracle_Dark_Lich_Secret_of_Mana.wav')
                sound.set_volume(.35)
                sound.play()
                time.sleep(60)
                pygame.mixer.fadeout(500)
                overworld_music(room)
                return room
            elif choice == '2':
                pygame.mixer.fadeout(500)
                pygame.mixer.init()
                pygame.init()
                sound = pygame.mixer.Sound('Battle Theme.wav')
                sound.play()
                sound.set_volume(.15)
                time.sleep(60)
                pygame.mixer.fadeout(500)
                overworld_music(room)
                return room
            elif choice == '3':
                pygame.mixer.fadeout(500)
                pygame.mixer.init()
                pygame.init()
                sound = pygame.mixer.Sound('Secret_of_Mana_Meridian_Dance_sound_remastered_.wav')
                sound.play()
                sound.set_volume(.50)
                time.sleep(60)
                pygame.mixer.fadeout(500)
                overworld_music(room)
                return room
            elif choice == '4':
                pygame.mixer.fadeout(500)
                pygame.mixer.init()
                pygame.init()
                sound = pygame.mixer.Sound('Close_Your_Eyelids_Secret_of_Mana_Music.wav')
                sound.play()
                sound.set_volume(.15)
                time.sleep(30)
                pygame.mixer.fadeout(500)
                overworld_music(room)
                return room
            else:
                pygame.mixer.fadeout(500)
                overworld_music(room)
                return room
    elif verb == 'party':
        print party
        return room

    elif verb == 'talk':
        print 'Even though you are the Mana Knight of legend, no one seems to have anything to say.'
        return room

    else:
        print "unrecognized command"
        describe(room)
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

def high_score():
    global score
#********************************Writing*************************************************
    name = raw_input('\n\n\nEnter you name to record your score:')
    display = (score, name.capitalize())
    with open('score_board.txt', 'a+b') as fout:
        fout.write(str(display) + '\n')
    print '\n\nYou can see your score by pressing score anytime in the game on the home screen.'.center(100)

    #********************************Reading*************************************************
    scores = []
    with open('score_board.txt', 'r') as fin:
        fileOpen = fin.read()
    for line in fileOpen[:-1].split('\n'):
        if line:
            score = literal_eval(line)
            scores.append(score)
    sortScore = sorted(scores, key=itemgetter(0), reverse=True)
    for points, name in sortScore:
        print (name + ' ' * 5 + str(points)).center(50)
    print 'Would you like to play again?'
    choice = raw_input('>>>')
    if choice in ['yes', 'Yes', 'yeah', 'y', 'Y']:
        pygame.mixer.fadeout(500)
        main()
    else:
        print 'Thanks for playing!!!'
        sys.exit()

if __name__ =="__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        exception_string = traceback.format_exc()
        logger.write_line([exception_string])
