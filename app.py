import hashlib# this password hashes , its a built in function btw
import os# generates a random salt for password hashing, a salt is randomly generated data that is addede to  a password before hashing it
import hmac#safe comparison of hashed passwords to prevent timing attacks,
print("--" * 20)
print("WELCOME TO SOLOME MARKET PLACE")
print("--" * 20)
#this creates a  list of different email signs known to the system and can be used to validate the email input by the user
email_signs = [
    "gmail.com", "yahoo.com", "outlook.com",
    "hotmail.com", "icloud.com", "protonmail.com",
    "aol.com", "zoho.com", "gmx.com", "yandex.com"
]

#Store registered user information 
#if a user registers, their username, email, and password will be stored in these variables for login validation.
registered_username = ""
registered_email = ""
registered_password_hash = ""
registered_password_salt = ""
#in this function,os.urandom(16) generates a random number using the os random secure sources 
def hash_password(password):
    salt=os.urandom(16)  # Generate a random salt
    #encode("utf-8") converts the password string into bytes using UTF-8 encoding, which is necessary for hashing.
    #shas256 is a cryptographic hash function that produces a fixed-size 256-bit (32-byte) hash value from the input data.
    #10000 repeats the calculation 600000 times to make the hashing process slower and more secure against hack attacks.
    #pbkdf2_hmac is a key derivation function that takes the salt and password and applies the hashing algorithm multiple times to produce a derived key (hashed password).
    hashed_password=hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'),salt,600000)
    #salt.hex() converts the salt bytes into a hexadecimal string representation, which is easier to store and retrieve.
    #hashed_password.hex() converts the hashed password bytes into a hexadecimal string representation for storage.
    return salt.hex(),hashed_password.hex()
def verify_password(stored_salt, stored_hash, provided_password):
    salt=bytes.fromhex(stored_salt)
    hashed_provided_password=hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'),salt,600000)
    return hmac.compare_digest(stored_hash,hashed_provided_password.hex())

while True:
    print("\n1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter your choice: ")

    # REGISTRATION
    if choice == "1":
        try:
            username = input("Enter a username: ")
            if username == "":
                raise ValueError("Username cannot be empty.")

            # Email validation
            while True:
                #here we a user is asked to enter their email ,
                #. strip() removes spaces  and 
                #.lower() converts the email to lowercase for consistency. 
                #The email is then validated for format and domain.
                useremail = input("Enter your email: ").strip().lower()
                #.count("@") checks if there is exactly one "@" symbol in the email.
                #If not, it prompts the user to try again.by using continue to restart the loop.

                if useremail.count("@") != 1:
                    print("Invalid email format. Please try again.")
                    continue
                   #checks for a dot and also checks if the domain is in the list of supported email domains.
                   #it also splits the email address entered into two parts using @ and each with index 0 and 1 respectively. 
                   # The first part is the username and the second part is the domain thats why we have useremail.split("@")[1]which checks the domain eg gmail.com.
                   #the not checks if the domain is in the list it will keep fails if its not there it keeps true  so its a viceversa operator
                elif "." not in useremail.split("@")[1]:
                    print("Invalid email format. Please try again.")
                    continue

                elif useremail.split("@")[1] not in email_signs:
                    print("Email domain not supported.")
                    continue
                #breaks the loop if the email is valid and accepted

                else:
                    print("Email accepted!")
                    break

            # Password validation
            while True:
                userpassword = input("Enter your password: ")

                if len(userpassword) < 6:
                    print("Password must be at least 6 characters.")
                    continue
                else:
                    break

            # Store user information
            registered_username = username
            registered_email = useremail
            registered_password_salt, registered_password_hash = hash_password(userpassword)

            print("\nRegistered successfully!")
            print(f"Welcome to Solome Marketplace {username}")
            #this  captures the error with in the try code and prints it so 
            # the prgrammers doesnt bother alot writting all errors even the in the except block
        except ValueError as e:
            print(e)
            continue

    # LOGIN
    elif choice == "2":

        if registered_username == "":
            print("Please register first.")
            continue

        while True:
            print("\nLOGIN OPTIONS")
            print("1. Login with username")
            print("2. Login with email")
            print("3. Back to main menu")

            login_choice = input("Enter your choice: ")

            if login_choice == "1":
                username = input("Enter your username: ")
                userpassword = input("Enter your password: ")

                if (username == registered_username
                    and verify_password(registered_password_salt, registered_password_hash, userpassword)):

                    print("Login successful!")
                    break

                else:
                    print("Incorrect username or password.")

            elif login_choice == "2":
                useremail = input("Enter your email: ").strip().lower()
                userpassword = input("Enter your password: ")

                if (useremail == registered_email
                    and verify_password(registered_password_salt, registered_password_hash, userpassword)):

                    print("Login successful!")
                    break

                else:
                    print("Incorrect email or password.")

            elif login_choice == "3":
                break

            else:
                print("Invalid login option. Try again.")

    # EXIT
    elif choice == "3":
        print("Exiting the application.")
        break

    else:
        print("Invalid choice. Please try again.")
