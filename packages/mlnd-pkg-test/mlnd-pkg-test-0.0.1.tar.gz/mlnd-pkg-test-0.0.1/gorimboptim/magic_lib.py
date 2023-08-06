import time

def magic_function():
    number = input("\nPlease enter a number between 0-100.\nCtrl-c to cancel.\n")
    
    try:
        number = int(number)
    except ValueError:
        print("\nYou are very farofinha.\nSelecting random number...\n")
        number = 3
        for _ in range(4):
            print(".")
            time.sleep(1)
        print("Selected number ", 3)
        time.sleep(2)

    for _ in range(int(1e3*number)):
        print(f"Gorimbo farofimbo #{number}")
    print("Thank you for participating.")
    exit()