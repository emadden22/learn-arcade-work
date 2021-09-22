# 'for Loops' - WHEn you know how many times to loop
# while loop - unknown number of loops

def print_about_class(repetitions):
    for i in range (repetitions):
        print("I will not chew gum in class")

repetitions = int(input("How many times?"))
print("But I can drink water.")

for i in range(10, -1, -1):
    print(i)
