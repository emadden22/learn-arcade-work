import random


def main():
    print("You have woken up super far from the border of some super hostile place.")
    print("Hostile people are coming to do hostile things to you. Hostile-y.")
    print("The closest border is 200 miles away.")
    print("Make it to the border or suffer the hostiles.")

    done = False
    miles_traveled = 0
    hostiles = 0
    tired = 0
    thirst = 0
    water = 4
    waterfill = -1

    while not done:
        print("A. Drink")
        print("B. Hide")
        print("C. Walk Fast Fast")
        print("D. Walk Less Fast")
        print("E. Status check")
        print("Q. Quit")

        user_input = input("How will you proceed?")

        if user_input.upper() == "Q":
            done = True
        elif user_unput.upper() == "E":
            print("Traveled:", miles_traveled)
            print("Drinks:"
            water)
            print("Hostiles are:"
            hostiles, "miles behind you")
            elif user_input.upper() == "B":
            print("You hide, the hostiles do not")
            tired = 0
            hostiles += random.range(5, 20)
        elif user_input.upper() == "C":
            miles = randon.randrange(10, 30)
            miles_traveled += miles
            thirst += 1
            tired += random.randrange(1, 5)
            hostiles += random.randrange(5, 16)
            water_get = random.randrange(20)
            if water_get == 12:
                thirst = 0
                tired = 0
                water = 4
                print("You found some water!!")
                print("That is as the hostiles say,")
                print("Hype")
                print("Hostiles continue to come for you")
            else:
                print("Life continues to be hard")
                print("Thoughts and prayers")
        elif user_input.upper() == "D":
            miles = random.randrange(4, 10)
            miles_traveled += miles
            thirst += 1
            tired += 1
            hostiles += random.randrange(5, 16)
            if water_get == 12:
                thirst = 0
                tired = 0
                water = 4
                print("You found some water!!")
                print("That is as the hostiles say,")
                print("Hype")
                print("Hostiles continue to come for you")
            else:
                print("Life continues to be hard")
                print("Thoughts and prayers")
        elif user_input.upper() == "A":
            if water > 0:
                water - + 1
                thirst = 0
                print("Hydrated once again")
            else:
                print("No water, find some or die soon")
        if thirst > 5:
            print("Yikes. Dehydration killed you")
            print("Pretty lame way to die")
            print("Bye Bye")
            done = True
        if miles_traveled >= 200:
            print("You escaped!")
            print("No hostile things being done to you!!")
            print("Bye Bye! Enjoy not being mutilated! :)")
            done = True
        if tired > 7:
            print("Team no sleep..")
            print("Dead")
            print("Bye Bye!")
            done = True
        elif tired > 5:
            print("Sleep or suffer, my dude")
        elif miles_traveled - hostiles <= 0:
            print("The hostiles got you, my dude")
            print("Very hostile things done to you")
            print("Enjoy being dead :)")
            print("Bye Bye!")
            done = True
        elif miles_traveled - hostiles < 20:
            print("You're so close!")
            print("But so are the hostiles!")
            print("Good luck!")
    print("Game Over. Bye Bye!")
    input("")


main()



