class Room:
    def __init__(self, name, north, east, south, west):
        self.name = name
        self.north = north
        self.east = east
        self.south = south
        self.west = west


def main():
    room_list = []
    room_dr = Room("Dining Room. There is a table and one door to the living room to the east. \n"
                   "", None, 1, None, None)
    room_list.append(room_dr)
    room_lr = Room("Living Room. There are bad pictures on the wall. \n "
                   "You are west of the entry way and south of the atrium", 3, 2, None, 0)
    room_list.append(room_lr)
    room_er1 = Room("Entry Room 1. There is a gross rug. \n "
                    "You are east of the living room. You may only go back.", None, None, 1, None)
    room_list.append(room_er1)
    room_ar = Room("Atrium. You are basically outside, but not. \n "
                   "You are south of an entry room, and north of the living room.", 5, None, 1, None)
    room_list.append(room_ar)
    room_br = Room("Bedroom. There is a bed. It looks cozy. \n "
                   "There is only the door you came from.", None, 5, None, None)
    room_list.append(room_br)
    room_er2 = Room("Entry Room 2. Another gross rug? Gross. \n "
                    "You are north of the atrium, east of the bedroom, and west of the kitchen.", None, 6, 3, 4)
    room_list.append(room_er2)
    room_kt = Room("Kitchen. There is no food. You are now sad. \n "
                   "There is only the door you came from.", None, None, None, 5)
    room_list.append(room_kt)
    current_room = 0
    done = False
    while not done:
        print()
        print(room_list[current_room].name)
        user_input = input("Where do you go? ")
        if user_input.lower() == "east" or user_input.lower() == "e":
            next_room = room_list[current_room].east
            if next_room is None:
                print("You can't go that way!")
            else:
                current_room = next_room

        elif user_input.lower() == "north" or user_input.lower() == "n":
            next_room = room_list[current_room].north
            if next_room is None:
                print("You can't go that way!")
            else:
                current_room = next_room

        elif user_input.lower() == "south" or user_input.lower() == "s":
            next_room = room_list[current_room].south
            if next_room is None:
                print("You can't go that way!")
            else:
                current_room = next_room

        elif user_input.lower() == "west" or user_input.lower() == "w":
            next_room = room_list[current_room].west
            if next_room is None:
                print("You can't go that way!")
            else:
                current_room = next_room

        elif user_input.lower() == "quit" or user_input.lower() == "q":
            done = True
            print("Game Over. Have a nice day!")


main()
