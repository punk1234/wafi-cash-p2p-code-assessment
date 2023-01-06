################################################
# USER MODEL
################################################

from datetime import datetime

class User:

    def __init__(self, username):
        self.username = username
        self.account_balance = 0
        self.created_at = datetime.now()

################################################
# DATA-STORE
################################################

class DataStore:

    content: dict = {}

    @staticmethod
    def add_record(key: str, value: User) -> None:
        DataStore.content[key] = value

    @staticmethod
    def get_record(key: str) -> User:
        return DataStore.content.get(key)
    
    @staticmethod
    def exist(key: str) -> bool:
        return (key in DataStore.content)

    @staticmethod
    def clear(key: str) -> None:
        DataStore.content = {}

################################################
# USER-SERVICE
################################################

INVALID_AMOUNT_ERROR = "Amount must be greater than ZERO!"

INVALID_SEND_OPERATION_WITH_SAME_USER = "Invalid operation - cannot send money to one's self!"

class UserService:

    def __init__(self):
        pass

    def create_user(self, username: str) -> User:
        """ Creates a new User

        Args:
          username: str, username of the new user

        Returns:
          The newly created User
        """
        
        self.__check_that_username_is_valid(username)
        self.__check_that_username_does_not_exist(username)

        new_user = User(username)
        DataStore.add_record(username, new_user)
        
        print(f"User {new_user.username} is added to the app")
        return new_user


    def credit_account(self, username: str, amount: float) -> User:
        """ Credits account of user with username

        Args:
          username: str, username of the user to credit
          amount: float, amount or value to credit the user

        Returns:
          The User object that was credited
        """

        self.__check_that_username_is_valid(username)

        if amount <= 0:
            raise Exception(INVALID_AMOUNT_ERROR)

        user = self.__check_that_username_exist(username)
        user.account_balance += amount

        print(f"User {user.username} deposits {amount} dollars")
        return user


    def send(self, sender_username: str, recipient_username: str, amount: float) -> list:
        """ Sends money from a user-account to another user-account

        Args:
          sender_username: str, username of the sender
          recipient_username: str, username of the recipient
          amount: float, amount or value to send

        Returns:
          A list containing both the sender & recipient user objects
        """

        self.__check_that_username_is_valid(sender_username)
        self.__check_that_username_is_valid(recipient_username)

        if sender_username == recipient_username:
            raise Exception(INVALID_SEND_OPERATION_WITH_SAME_USER)

        if amount <= 0:
            raise Exception(INVALID_AMOUNT_ERROR)

        sender = self.__check_that_username_exist(sender_username)
        recipient = self.__check_that_username_exist(recipient_username)
            
        self.__check_that_user_has_sufficient_funds(sender, amount)

        sender.account_balance -= amount
        recipient.account_balance += amount

        print(f"User {sender.username} sends {amount} dollars to User {recipient.username}")
        return [sender, recipient]


    def transfer(self, username: str, amount: float) -> None:
        """ Transfers money out of a user's account

        Args:
          username: str, username of user to debit for transfer
          amount: float, amount or value to debit the user

        Returns:
          The User object that was debited
        """

        self.__check_that_username_is_valid(username)

        if amount <= 0:
            raise Exception("Amount must be greater than ZERO!")

        user = self.__check_that_username_exist(username)
        self.__check_that_user_has_sufficient_funds(user, amount)

        user.account_balance -= amount

        print(f"User {user.username} transfers {amount} dollars from their account")
        return user
        

    def check_account_balance(self, username: str) -> float:
        """ Checks user's account balance

        Args:
          username: str, username of user to get account-balance

        Returns:
          The account-balance of specified user with username
        """

        self.__check_that_username_is_valid(username)
        user = self.__check_that_username_exist(username)

        print(f"User {user.username} checks their balance and has {user.account_balance} dollars")
        return user.account_balance
        

    def __check_that_username_is_valid(self, username: str) -> None:
        username = username.strip()

        if len(username) == 0:
            raise Exception("Invalid user!")


    def __check_that_username_does_not_exist(self, username: str) -> None:
        if DataStore.exist(username):
            raise Exception("User already exist!")


    def __check_that_username_exist(self, username: str) -> User:
        found_user = DataStore.get_record(username)

        if found_user:
            return found_user

        raise Exception("User not found!")


    def __check_that_user_has_sufficient_funds(self, sender: User, amount_to_deduct: float) -> None:
        if sender.account_balance < amount_to_deduct:
            raise Exception("Insufficient account balance!")

################################################
# APP
################################################

class App:

    def __init__(self):
        self.user_service = UserService()

    def run(self):
        """Sample run of the app"""

        try:
            A = self.user_service.create_user("A")
            self.user_service.credit_account(A.username, 10)

            B = self.user_service.create_user("B")
            self.user_service.credit_account(B.username, 20)

            self.user_service.send(B.username, A.username, 15)

            self.user_service.check_account_balance(A.username)
            self.user_service.check_account_balance(B.username)

            self.user_service.transfer(A.username, 25)
            self.user_service.check_account_balance(A.username)
        except Exception as ex:
            print(ex)

################################################
# MAIN EXECUTOR!!!
################################################

if __name__ == "__main__":
    print("Welcome to `WIFI.CASH` peer-to-peer app!!!")

    app = App()
    app.run()