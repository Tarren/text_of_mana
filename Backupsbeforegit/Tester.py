__author__ = 'THubbard'
import the_map
import sys

player = None
rooms_by_name = dict()
player_inventory =[]

def main():
    with open('the_map.xml', 'r') as fin:
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
    current_room = game_map.building[0]
    while True:
        print current_room.text[0].value
        command = raw_input(">")
        verb, nouns = parse_command(command)
        current_room = run_command(current_room, verb, nouns)

def parse_command(command):
    words = command.split()
    verb = words[0]
    nouns = words[1:]
    return verb, nouns

def run_command(room, verb, nouns):
    global player
    global player_inventory
    exits, items, npcs, locked = get_room_data(room)

    #hopefully one day will check to see if doors are locked, and if so, let me pass through them if I have the key.
    if verb == "go":
        noun = ' '.join(nouns)
        room_exit = exits.get(noun, None)
        if room_exit:
            lock = locked.get(room_exit.attrs["name"], False)
            if lock == 'True':
                print 'The door is locked'
                return room
            else:
                return rooms_by_name[room_exit.attrs["link"]]
        else:
            print "You can't go there."
            return room
    #look to see if there are items in the room, and add them to inventory
    elif verb == "look":
        item = items.get('name')
        if item:
            player_inventory.append(item)
            return room
        else:
            print 'You look around and see nothing of value'
            return room
    #quit if you get stuck in a loop
    elif verb == "quit":
        print 'Sorry to see you go, goodbye'
        sys.exit()
    #brief help guide
    elif verb == "help":
        print "The game is fairly simple to play."
        print "Commands generally break down to: look, go, or, take"
        return room

    else:
        print "unrecognized command"
        return room

def get_room_data(room):
    exits = dict()
    for room_exit in room.exit:
        exits[room_exit.attrs["name"]] = room_exit
        exits[room_exit.attrs["dir"]] = room_exit

    items = dict()
    for item in room.item:
        items[item.attrs["name"]] = item

    locked = dict()
    for room_exit in room.exit:
        exits[room_exit.attrs["locked"]] = room_exit
        locked[room_exit.attrs["name"]] = "True"

    npcs = dict()
    for npc in room.npc:
        npcs[npc.attrs["name"]] = npc

    return exits, items, npcs , locked

if __name__ =="__main__":
    main()

# roomname = game_map.building[0].room_name[0].value

# room_dict = game_map.__dict__
#
# exits = game_map.building[0].exits[0].value
# name = game_map.building[0].text[0].value
# event_number = game_map.building[1].event[0].value
# locked_doors = game_map.building[0].locked_door[0].desc[0].value
#
#
# print 'Room Name:' ,roomname
# print 'Exits:' ,exits
# print 'Desc:', name
# print 'Event Numbers: ', event_number
# print 'Locked Doors:' , locked_doors