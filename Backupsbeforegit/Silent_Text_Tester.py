__author__ = 'THubbard'
import the_map
import sys
import os
import random
player_health = 100
rooms_by_name = dict()
player_inventory =[]
player_damage = 5
game_map = None
player_experience = 0
player_level = 1
next_level = 25
character = {'Player Level': 1, 'Player Exp': 0, 'Next Level': 25}
player_stats = {'Strength': 1, 'Dexterity': 1, 'Intelligence': 1}



def main():
    global game_map
    games = os.listdir("saved_games")
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
    while True:
        if current_room is not last_room:
            describe(current_room)
        last_room = current_room
        command = raw_input(">")
        verb, noun = parse_command(command)
        os.system('CLS')
        current_room = run_command(current_room, verb, noun)

def intro():
    global game_map
    intro_text = game_map.intro[0].text[0].value
    print intro_text

def battle_system(room, monsters):
    global player_health
    global player_inventory
    global player_damage
    monster = room.monster[0]
    monster_name = monster.attrs["name"]
    monster_damage = 5
    monster_health = room.monster[0].attrs["health"]
    if "shovel" in player_inventory:
        player_damage = 15
    if "shotgun" in player_inventory and "shotgun ammo" in player_inventory:
            player_damage = 1000
    print 'You have encountered a ', monster_name
    while player_health >0 and monster_health >0:
        print 'Player Health:', player_health
        print 'Enemy Health', monster_health
        command = raw_input('What would you like to do>>>')
        if command == "attack":
            monster_health = int(monster_health) - player_damage
            print ''
            print 'You do', player_damage, 'damage to the', monster_name
            print ''
            if monster_health >= 0:
                player_health = player_health - monster_damage
        elif command == 'run':
            print 'Cannot escape'
        else:
            print 'What are you thinking?!?'
            print monster_name, "attacks you for ", monster_damage, "while you are fumbling around."
            player_health = player_health - monster_damage

        if player_health <=0:
            print 'You have been eaten by a ', monster_name
            print "Game Over"
            raw_input('...')
            break

        if monster_health <= 0:
            print 'You have beaten a', monster_name
            print ''
            print 'You have', player_health, 'health remaining'
            print ''
            room.monster.remove(monster)
            return

def experience_system(room):
    global character

    nstr, ndex, nint = 0, 0, 0

    while character['Player Exp'] >= character['Next Level']:
        character["Player Level"] += 1
        character["Player Exp"] = character["Player Exp"] - character["Next Level"]
        character["Next Level"] = round(character["Next Level"] * 1.5)
        nstr = random.randint(1 , 5)
        ndex = random.randint(1 , 5)
        nint = random.randint(1 , 5)
        #Prints stat gain
        player_stats['Strength'] += nstr
        player_stats['Dexterity'] += ndex
        player_stats['Intelligence'] += nint
        print character["Player Level"]
        print 'Strength:', nstr
        print "Dexterity:", ndex
        print "Intelligence:", nint




def describe(room):
    print room.text[0].value
    if room.item:
        item_text = "You see"
        for item in room.item:
            item_text += " a " + item.attrs["name"]
        print item_text
        print ''
    if room.exit:
        for exit in room.exit:
            room_text = 'You see a '
            room_text += exit.attrs["name"] + ' to your ' + exit.attrs["dir"]
            print room_text




def parse_command(command):
    words = command.split()
    if len(words) < 1:
        words = ["BAD_COMMAND"]
    verb = words[0]
    noun = " ".join(words[1:])
    return verb, noun

def run_command(room, verb, noun):
    global player
    global player_inventory

    exits, items, locked, reqs, monsters = get_room_data(room)
    #hopefully one day will check to see if doors are locked, and if so, let me pass through them if I have the key.
    if monsters:
        battle_system(room, monsters)

    if verb in ["go", "g", "walk", "run", "sprint", "w", "r", "s"]:
        room_exit = exits.get(noun, None)
        if room_exit:
            lock = locked.get(room_exit.attrs["name"])
            if lock == 'True':
                req = reqs[room_exit.attrs["name"]]
                if req == "None" or req in player_inventory:
                    print 'You unlocked the', room_exit.attrs["name"]
                    return rooms_by_name[room_exit.attrs["link"]]
                else:
                    print 'The', room_exit.attrs["name"], 'is locked'
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


        #brief help guide
    elif verb in ["help", "Help", "HELP", "HElp"]:
        print "The game is fairly simple to play."
        print "Commands generally break down to: look, go, or, take"
        print "Also, if you would like to view your inventory, enter a capital 'I'"
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
    main()