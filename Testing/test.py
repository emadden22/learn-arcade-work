elif user_input.upper() == "east" or user_input.upper() == "e":
next_room = room_list[current_room].east
if user_input.upper() == None:
    print("You can't go that way!")
else:
    next_room = current_room
elif user_input.upper() == "south" or user_input.upper() == "s":
next_room = room_list[current_room].south
if user_input.upper() == None:
    print("You can't go that way!")
else:
    next_room = current_room
elif user_input.upper() == "west" or user_input.upper() == "w":
next_room = room_list[current_room].west
if user_input.upper() == None:
    print("You can't go that way!")
else:
    next_room = current_room