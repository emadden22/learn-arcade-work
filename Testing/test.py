while True: # Loop forever
    quit = input("Do you want to quit? ")
    if quit == "y":
        break

    attack = input("Does your elf attack the dragon? ")
    if attack == "y":
        print("Bad choice, you died.")
        break

    attack = input("Does your elf attempt to steal the gold? ")
    if attack == "y":
        print("Bad choice, you died.")
        break

done = True
    while done:
        sick = input("Would you like to un-alive?")
        if sick == "y" or "yes":
            done = False

    done = False
    while not done:
        run = input("Nice. Lets go")
        if run == "y" or "yes":
            print("The border is" 'total' "miles away. Do you want to:")
            print("a. Sprint")
            print("b. Hide")
            print("c. Check health")
            print("d. Walk without concern")
            done = False
        sprint = input("You have made it" "miles")
        if sprint == "a":
            print("You made it")
            done = False
            continue