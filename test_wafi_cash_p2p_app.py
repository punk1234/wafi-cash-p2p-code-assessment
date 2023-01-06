import unittest

from wafi_cash_p2p_app import UserService

class Test_CreateUser(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.user_service = UserService()

    def test_create_user_with_valid_username__success(self):
        """
        Test: test_create_user_with_valid_username__success
        """
        
        valid_username = "abc"
        user = self.user_service.create_user(valid_username)

        self.assertEqual(user.account_balance, 0)
        self.assertEqual(user.username, valid_username)

    def test_create_user_with_invalid_username__error(self):
        """
        Test: test_create_user_with_invalid_username__error
        """
        
        invalid_username = " "

        with self.assertRaises(Exception) as context:
            self.user_service.create_user(invalid_username)
            
        self.assertTrue("Invalid user!" in str(context.exception))

    def test_create_user_that_already_exist__error(self):
        """
        Test: test_create_user_that_already_exist__error
        """
        
        valid_username = "abc-001"
        user = self.user_service.create_user(valid_username)

        self.assertEqual(user.account_balance, 0)
        self.assertEqual(user.username, "abc-001")

        with self.assertRaises(Exception) as context:
            self.user_service.create_user(valid_username)
            
        self.assertTrue("User already exist!" in str(context.exception))


class Test_CreditUserAccount(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.user_service = UserService()

    def test_credit_user_account_with_valid_amount__success(self):
        """
        Test: test_credit_user_account_with_valid_amount__success
        """
        
        user = self.user_service.create_user("valid_username")
        self.user_service.credit_account(user.username, 10)

        self.assertEqual(user.account_balance, 10)
        self.assertEqual(user.username, "valid_username")

    def test_credit_user_account_with_negative_amount__error(self):
        """
        Test: test_credit_user_account_with_negative_amount__error
        """
        
        user = self.user_service.create_user("valid_username_01")

        with self.assertRaises(Exception) as context:
            self.user_service.credit_account(user.username, -3)
            
        self.assertTrue("Amount must be greater than ZERO!" in str(context.exception))

    def test_credit_user_account_with_zero_amount__error(self):
        """
        Test: test_credit_user_account_with_zero_amount__error
        """
        
        user = self.user_service.create_user("valid_username_02")

        with self.assertRaises(Exception) as context:
            self.user_service.credit_account(user.username, 0)
            
        self.assertTrue("Amount must be greater than ZERO!" in str(context.exception))

    def test_credit_user_that_does_not_exist__error(self):
        """
        Test: test_credit_user_that_does_not_exist__error
        """
        
        not_found_username = "@not_found_username_404"

        with self.assertRaises(Exception) as context:
            self.user_service.credit_account(not_found_username, 7)
            
        self.assertTrue("User not found!" in str(context.exception))

    def test_credit_user_that_multiple_credits_gives_correct_balance__success(self):
        """
        Test: test_credit_user_that_multiple_credits_gives_correct_balance__success
        """
        
        valid_username = "@multiple_credit_user"
        user = self.user_service.create_user(valid_username)

        self.user_service.credit_account(valid_username, 7)
        self.user_service.credit_account(valid_username, 2500)
        self.user_service.credit_account(valid_username, 16)
            
        self.assertEqual(user.account_balance, 2523)
        self.assertEqual(user.username, valid_username)

    def test_credit_user_for_different_users_and_gives_correct_balance__success(self):
        """
        Test: test_credit_user_for_different_users_and_gives_correct_balance__success
        """
        
        user_1 = self.user_service.create_user("different_user_001")
        user_2 = self.user_service.create_user("different_user_002")

        user_1 = self.user_service.credit_account(user_1.username, 387)
        user_2 = self.user_service.credit_account(user_2.username, 7843)
            
        self.assertEqual(user_1.account_balance, 387)
        self.assertEqual(user_2.account_balance, 7843)


class Test_TransferMoney(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.user_service = UserService()

    def test_transfer_money_with_insufficient_balance__error(self):
        """
        Test: test_transfer_money_with_insufficient_balance__error
        """
        
        user = self.user_service.create_user("valid_username_001")

        with self.assertRaises(Exception) as context:
            self.user_service.transfer(user.username, 10)
            
        self.assertTrue("Insufficient account balance!" in str(context.exception))

    def test_transfer_money_with_negative_amount__error(self):
        """
        Test: test_transfer_money_with_negative_amount__error
        """
        
        user = self.user_service.create_user("valid_username_002")

        with self.assertRaises(Exception) as context:
            self.user_service.transfer(user.username, -2.5)
            
        self.assertTrue("Amount must be greater than ZERO!" in str(context.exception))

    def test_transfer_money_with_zero_amount__error(self):
        """
        Test: test_transfer_money_with_zero_amount__error
        """
        
        user = self.user_service.create_user("valid_username_003")

        with self.assertRaises(Exception) as context:
            self.user_service.transfer(user.username, 0)
            
        self.assertTrue("Amount must be greater than ZERO!" in str(context.exception))

    def test_transfer_money_for_non_existing_user__error(self):
        """
        Test: test_transfer_money_for_non_existing_user__error
        """
        
        not_found_username = "@valid_username_003__404"

        with self.assertRaises(Exception) as context:
            self.user_service.transfer(not_found_username, 3)
            
        self.assertTrue("User not found!" in str(context.exception))

    def test_transfer_money_multiple_times_gives_correct_balance__success(self):
        """
        Test: test_transfer_money_multiple_times_gives_correct_balance__success
        """
        
        valid_username = "@multiple_credit_user_001"
        user = self.user_service.create_user(valid_username)
        self.user_service.credit_account(valid_username, 1000)

        self.user_service.transfer(valid_username, 100)
        self.user_service.transfer(valid_username, 200)
        self.user_service.transfer(valid_username, 300)
        self.user_service.transfer(valid_username, 350)
            
        self.assertEqual(user.account_balance, 50)


class Test_SendMoney(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.user_service = UserService()

    def test_send_money_with_insufficient_balance_for_sender__error(self):
        """
        Test: test_send_money_with_insufficient_balance_for_sender__error
        """
        
        user_1 = self.user_service.create_user("_username_001")
        user_2 = self.user_service.create_user("_username_002")

        with self.assertRaises(Exception) as context:
            self.user_service.send(user_1.username, user_2.username, 10)
            
        self.assertTrue("Insufficient account balance!" in str(context.exception))

    def test_send_money_with_negative_amount__error(self):
        """
        Test: test_send_money_with_negative_amount__error
        """
        
        user_1 = self.user_service.create_user("_username_003")
        user_2 = self.user_service.create_user("_username_004")

        with self.assertRaises(Exception) as context:
            self.user_service.send(user_1.username, user_2.username, -9999.999)
            
        self.assertTrue("Amount must be greater than ZERO!" in str(context.exception))

    def test_send_money_with_zero_amount__error(self):
        """
        Test: test_send_money_with_zero_amount__error
        """
        
        user_1 = self.user_service.create_user("_username_005")
        user_2 = self.user_service.create_user("_username_006")

        with self.assertRaises(Exception) as context:
            self.user_service.send(user_1.username, user_2.username, 0)
            
        self.assertTrue("Amount must be greater than ZERO!" in str(context.exception))

    def test_send_money_to_non_existing_user__error(self):
        """
        Test: test_send_money_to_non_existing_user__error
        """
        
        sender = self.user_service.create_user("_username_007")
        self.user_service.credit_account(sender.username, 100)

        not_found_username = "@_username_006_404"

        with self.assertRaises(Exception) as context:
            self.user_service.send(sender.username, not_found_username, 3)
            
        self.assertTrue("User not found!" in str(context.exception))

    def test_send_money_multiple_times_gives_correct_balances__success(self):
        """
        Test: test_send_money_multiple_times_gives_correct_balances__success
        """
        
        user_1 = self.user_service.create_user("_username_008")
        user_2 = self.user_service.create_user("_username_009")

        self.user_service.credit_account(user_1.username, 100)
        self.user_service.credit_account(user_2.username, 50)

        self.user_service.send(user_1.username, user_2.username, 5)
        self.user_service.send(user_1.username, user_2.username, 10)
        self.user_service.send(user_1.username, user_2.username, 15)
        self.user_service.send(user_1.username, user_2.username, 20)

        self.assertEqual(user_1.account_balance, 50)
        self.assertEqual(user_2.account_balance, 100)

    def test_send_money_to_oneself__error(self):
        """
        Test: test_send_money_to_oneself__error
        """
        
        sender = self.user_service.create_user("_username_010")
        self.user_service.credit_account(sender.username, 250)

        with self.assertRaises(Exception) as context:
            self.user_service.send(sender.username, sender.username, 250)
            
        self.assertTrue("Invalid operation - cannot send money to one's self!" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
