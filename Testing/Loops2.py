def count_up(start, end):
    for number in range(start, end + 1):
        print(number)

count_up(5, 10)

done = False

while not done:
    quit = input("Do you want to quit?")
    if quit.lower()== "y":
        done = True
        print("Bye!")
        break

    attack = input("Do you want to attack the dragon?")
    if attack.lower() == "y":
        done = True
        print("Bad choice")