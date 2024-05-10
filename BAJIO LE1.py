# Dictionary to store game library with their quantities and rental costs
game_library = {
    "Donkey Kong" : { "Quantity" : 3, "Cost" : 2.0},
    "Super Mario Bros" : { "Quantity" : 5, "Cost" : 3.0 },
    "Tetris" : { "Quantity" : 2, "Cost" : 1.0},
    "Tiny Epic Galaxies" : { "Quantity" : 6, "Cost" : 4.0},
    "Moonrakers" : { "Quantity" : 8, "Cost" : 5.0 },
    "Rival Restaurants" : {"Quantity" : 4, "Cost": 5.0}
}
# Dictionary to store user accounts with their balances and points
user_accounts = {}

# Admin account details
admin_username = "admin"
admin_password = "adminpass"

# Function for the User Menu
def user_menu():
    print("\nGame Rental System")
    print("1. Display Available Games")
    print("2. Register User")
    print("3. Log In User")
    print("4. Return")

    while True:
        try: 
            choice = int(input("\nEnter your choice: "))
            if choice == 1:
                display_available_games()
    
                user_menu()
                break
            elif choice == 2:
                register_user()
                break
            elif choice == 3:
                log_in()
                break
            elif choice == 4:
                main()
                break
            else:
                print("Invalid Input. Please try again.")
        except ValueError as e:
            print(f"Value errror: {e}")

# Function to display available games with their numbers and rental costs
def display_available_games():
    print("\nAvailable Games")
    for idx, (game, info) in enumerate (game_library.items(), start=1):
        print(f'{idx}. {game}: Quantity: {info['Quantity']} Cost: ${info['Cost']}')

# Function to register a new user
def register_user():
    print("\nRegistration")
    while True:
        rented_items = {}
        username = input("Enter your username (must be 5 characters or more): ")
        if username in user_accounts:
            print("User already exists.")
        elif len(username) < 5:
            print("Too short.") 
        else:
            while True:
                password = input("Enter your password( It must be 8 characters long): ")
                if len(password) < 8:
                    print("Password should be 8 characters long.")
                else:
                    break

            user_accounts[username] = {"password": password, "balance": 0, "points": 0, "rented_items": rented_items}
            print("\nSign up successful! You can now log in.")
            log_in()
            break

# Function for the user to log in
def log_in():
    print("\nLog In Portal")
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username in user_accounts and user_accounts[username]["password"] == password:
            if user_accounts[username]['balance'] == 0:
                print("\nWelcome to the Game Rental System! Please top up before proceeding.")
                top_up(username)
            rentalmain(username)
            break
        else:
            print("\nInvalid username or password. Please try again.")

# Function for the user menu after logging in
def rentalmain(username):
    print("\nWelcome to the Rental Game System")
    print("1. Rent A Game")
    print("2. Return A Game")
    print("3. Top Up Account")
    print("4. Display Inventory")
    print("5. Check Points")
    print("6. Redeem Free Points")
    print("7. Log Out")

    while True:
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                rent(username)
                break
            elif choice == 2:
                return_game(username)
                break
            elif choice == 3:
                top_up(username)
                rentalmain(username)
                break
            elif choice == 4:
                inventory(username)
                rentalmain(username)
                break
            elif choice == 5:
                check_point(username)
                break
            elif choice == 6:
                redeem_game(username)
                break
            elif choice == 7:
                print("Logged Out.")
                user_menu()
                break
            else:
                print("Invalid input. Please Try again.")
        except ValueError as e:
            print(f"Value errror: {e}")

# Function for renting a game
def rent(username): 
    display_available_games()
    while True:
        try:
            choice = int(input("Enter the number of the game you want to rent: "))
            game_names = list(game_library.keys())
            if 1 <= choice <= len(game_names):
                game_name = game_names[choice - 1]
                if game_library[game_name]['Quantity'] <= 0:
                    print("Game is not available.")
                else:
                    break
            else:
                print("Invalid choice. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
   
    while True:
        try:
            game_quantity = int(input(f"How many copies of {game_name} would you like to rent: "))
            if game_quantity <= 0:
                print("Invalid input. Please enter a positive integer.")
            elif game_library[game_name]['Quantity'] < game_quantity:
                print("Not enough copies available. Please select a lower quantity.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    total_cost = game_library[game_name]["Cost"] * game_quantity
    print(f"Total cost: ${total_cost}")
    print("Please confirm your order.")
    confirm = input("Enter any character to confirm. Leave it blank to cancel the transaction.")
    if confirm:
        if game_name in user_accounts[username]["rented_items"]:
            user_accounts[username]["rented_items"][game_name] += game_quantity
        else:
            user_accounts[username]["rented_items"][game_name] = game_quantity

        while True:
            if user_accounts[username]['balance'] < total_cost:
                input("Insufficient balance. Click enter to top-up.")
                top_up(username)
            else: 
                break

        user_accounts[username]['balance'] -= total_cost
        game_library[game_name]['Quantity'] -= game_quantity
        user_accounts[username]["points"] += (total_cost / 2)

        print(f"Purchase success! You earned {user_accounts[username]["points"]} point/s!")
        print("\nReceipt:")
        print(f'Game Rented: {game_name} Quantity: {game_quantity} Total Amount: {total_cost}')
        print(f'New balance after purchase: ${user_accounts[username]["balance"]}')
        input("Click enter to return.")
        rentalmain(username)
    else:
        print("Transaction Cancelled")
        rentalmain(username)

# Function for returning a game 
def return_game(username):
    print("\nItems to return")
    rented_items = user_accounts[username]["rented_items"]
    if rented_items:
        for idx, (game, quantity) in enumerate(rented_items.items(), start=1):
            print(f"{idx}. {game}: Quantity: {quantity} ")
    else:
        print("No items currently rented.")
        input("Press enter to return to rental main.")
        rentalmain(username)

    while True:
        try:
            choice = int(input("Enter the number of the game you want to return: "))
            item_to_return = list(rented_items.keys())
            if 1 <= choice <= len(item_to_return):
                item_to_return = item_to_return[choice - 1]
                break
            else:
                print("Invalid choice. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    while True:
        try:
            quantity_of_the_game = int(input("Enter the quantity of the game you want to return: "))
            if quantity_of_the_game <= 0:
                print("Invalid input. Please enter a positive integer.")
            elif quantity_of_the_game > rented_items[item_to_return]:
                print("You cannot return more than copies you rented.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    game_library[item_to_return]["Quantity"] += quantity_of_the_game
    user_accounts[username]["rented_items"][item_to_return] -= quantity_of_the_game

    if user_accounts[username]["rented_items"][item_to_return] == 0:
        del user_accounts[username]["rented_items"][item_to_return] 

    print(f"Successfully returned {quantity_of_the_game} copies of {item_to_return}.")
    rentalmain(username)

# Function for top up 
def top_up(username):
    print("\nTop Up")
    print(f"Username: {username}")
    
    while True:
        try:
            top_up_amount = float(input("Enter amount: "))
            if top_up_amount <= 0:
                print("Invalid input. Please enter a positive amount.")
            else:
                user_accounts[username]['balance'] += top_up_amount
                print("Top up successful")
                print(f"Username: {username}, New balance: ${user_accounts[username]['balance']}")
                break
        except ValueError as e:
            print(f"Value errror: {e}")

# Function for checking user inventory
def inventory(username):
    rented_games = user_accounts[username].get('rented_items', {})
    print("\nYour Inventory:")
    if rented_games:
        print("Rented Games:")
        for game_name, quantity in rented_games.items():
            print(f"{game_name}: {quantity} copies")
    else:
        print("You have not rented any games.")

    balance = user_accounts[username]['balance']
    print(f"Account Balance: ${balance:.2f}")

# Function for redeeming points
def redeem_game(username):
    print("\nRedeem Game")
    available_points = user_accounts[username]["points"]
    
    if available_points >= 3:
        user_accounts[username]['points'] -= 3
        print("Redeemed a free game rental! 3 points deducted.")
        display_available_games()
        while True:
            try:
                choice = int(input("Enter the number of the game you want to rent: "))
                game_names = list(game_library.keys())
                if 1 <= choice <= len(game_names):
                    game_name = game_names[choice - 1]
                    break
                else:
                    print("Invalid choice. Please enter a number within the range.")
            except ValueError as e:
                print(f"Value errror: {e}")

        if game_library[game_name]['Quantity'] <= 0:
            print("Game is not available.")
        else:
            game_library[game_name]['Quantity'] -= 1
            if game_name in user_accounts[username]["rented_items"]:
                user_accounts[username]["rented_items"][game_name] += 1
            else:
                user_accounts[username]["rented_items"][game_name] = 1
            print("Game rented successfully")
            input("Click enter to return. ")
            rentalmain(username)
    else:
        print(f"You only have {available_points} point/s. You need at least 3 points.")
        rentalmain(username)

# Function for checking earned points
def check_point(username):
    print("\nPoint System Mechanics")
    print("good news! You can use points to rent a game for free.") 
    print("Every purchase of 2$ will grant you 1 point.\nThree (3) points is equivalent to a free game!")
    print("Purchase more to earn free points!")

    points = user_accounts[username]['points']
    print(f"\nYou have {points} point/s.")
    input("Click enter to return. ")
    rentalmain(username)

# Function for admin log in
def admin_login():
    print("\nAdmin Log In")
    while True: 
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if username == admin_username and password == admin_password:
            admin_menu()
            break
        else:
            print("Invalid username or password. ")

# Function for admin menu
def admin_menu():
    print("\nAdmin Menu")
    print("1. Update Game Details")
    print("2. Add New Game")
    print("3. Display Game Inventory")
    print("4. Log Out")
    while True:
        try: 
            choice = int(input("Enter your choice: "))
            if choice == 1:
                update_menu()
                break
            elif choice == 2:
                add_new_game()
                break
            elif choice == 3:
                display_game_inventory()
                break
            elif choice == 4:
                print("Logging out...Goodbye!")
                main()
                break
            else:
                print("Please input a valid option")
        except ValueError as e:
            print(f"Value errror: {e}")

#Function for displaying game inventory
def display_game_inventory():
    print("\nGame Inventory")
    print("Available Games:")
    for idx, (game, info) in enumerate(game_library.items(), start=1):
        print(f'{idx}. {game}: Quantity: {info["Quantity"]}, Cost: ${info["Cost"]}')

    print("\nRented Items:")
    for username, user_info in user_accounts.items():
        rented_items = user_info.get('rented_items', {})
        if rented_items:
            print(f"User: {username}")
            for game_name, quantity in rented_items.items():
                print(f"\t{game_name}: Quantity: {quantity}")
        else:
            print(f"No items rented by {username}.")

    input("Press enter to return to admin menu.")
    admin_menu()

# Function for Update Menu
def update_menu():
    print("\nUpdate Game Menu")
    print("1. Display Available Games")
    print("2. Update Game Copies Available")
    print("3. Update Game Cost")
    print("4. Exit")
    while True:
        try: 
            choice = int(input("Enter your choice: "))
            if choice == 1:
                display_available_games()
                update_menu()
                break
            if choice == 2:
                update_game_quantity()
                break
            elif choice == 3:
                update_game_cost()
                break
            elif choice == 4:
                admin_menu()
                break
            else:
                print("Please input a valid option")
        except ValueError as e:
            print(f"Value errror: {e}")

#Function for Updating Game Quantity
def update_game_quantity():
    print("\nUpdate Game Quantity")
    display_available_games()
    while True: 
        try:
            game_choice = int(input("Enter the number of the game you want to update: "))
            game_names = list(game_library.keys())
            if 1 <= game_choice <= len(game_names):
                game_name = game_names[game_choice - 1]
                while True:
                    try: 
                        new_quantity = int(input(f"Enter the new number of copies for {game_name}: "))
                        if new_quantity >= 0:
                            game_library[game_name]['Quantity'] = new_quantity
                            print(f"Updated Quantity available for {game_name}: {new_quantity}")
                            update_menu()
                            break
                        else: 
                            print("Please enter a positive number.")
                    except ValueError:
                        print("Please enter an integer.")
                break
            else:
                print("Invalid game choice.")
        except ValueError as e:
            print(f"Value errror: {e}")

# Function for Updating Game Cost
def update_game_cost():
    print("\nUpdate Game Cost")
    display_available_games()
    while True: 
        try:
            game_choice = int(input("Enter the number of the game you want to update: "))
            game_names = list(game_library.keys())
            if 1 <= game_choice <= len(game_names):
                game_name = game_names[game_choice - 1]
                while True:
                    try: 
                        new_cost = float(input(f"Enter the new cost for {game_name}: "))
                        if new_cost >= 0:
                            game_library[game_name]['Cost'] = new_cost
                            print(f"Updated cost for {game_name}: ${new_cost}")
                            update_menu()
                            break
                        else:
                            print("Please enter a positive number.")
                    except ValueError:
                        print("please enter a valid digit.")
                break
            else:
                print("Invalid game choice.")
        except ValueError as e:
            print(f"Value errror: {e}")

# Function for Addng New Game
def add_new_game():
    print("\nAdd New Game")
    while True:
        new_game_name = input("Enter the name of the new game: ")
        if new_game_name in game_library:
            print("Game already exists in the library.")
        else:
            break

    while True:
        try:
            new_quantity = int(input("Enter the quantity of copies for the new game: "))
            new_cost = float(input("Enter the cost for the new game: "))
            if new_quantity >= 0 and new_cost >= 0:
                game_library[new_game_name] = {'Quantity': new_quantity, 'Cost': new_cost}
                print(f"New game '{new_game_name}' added to the library.")
                admin_menu()
                break
            else: 
                print("Invalid values. Please Try again.")
        except ValueError as e:
            print(f"Value errror: {e}")

# Main function to run the program
def main():
    print("Game Rental System")
    print("1. User")
    print("2. Admin")
    print("3. Exit")
    while True:
        try:
            choice = int(input("Choose your role: "))
            if choice == 1:
                user_menu()
                break
            elif choice == 2:
                admin_login()
                break
            elif choice == 3:
                print("Exiting...")
                break
            else: 
                print("Invalid input. Please try again.")
        except ValueError as e:
            print(f'Value error: {e}')

if __name__ == "__main__":
    main()
