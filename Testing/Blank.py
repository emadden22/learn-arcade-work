def average(x, y, z):
    result = (x + y + z) / 3
    return result


result = average(x=10, y=20, z=30)
print(result)

# If statements

a = 4
b = 5
if a < b:
    print("a is smaller than b")

if b < a:
    print("b is smaller than a")

print("done")

temperature = input("What is the temperature in Fehrenheit? ")
temperature = int(temperature)

if temperature > 90:
    print("It is hot.")
else:
    print("Man, its cold")

print("Done")
