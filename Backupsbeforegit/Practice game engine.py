stat= init_stat
player = init_player

while 1:
	print get_text(state)
	in = raw_input)get_prompt)(state))
	in = parse(in)
	transitions = get_transitions(state, in, player)
	print transitions
	state = get_next_state(state, in, player)
	
def get_text()
	return game_map.area[state].desc[0].value
	
	
	
	
area[0].desc[0].value
	