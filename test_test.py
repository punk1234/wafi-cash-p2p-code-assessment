import unittest

from test import UserService

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

        self.assertEqual(len(user.wallets.keys()), 4)
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

        self.assertEqual(len(user.wallets.keys()), 4)
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
        self.user_service.credit_account(user.username, 10, "USD")
        self.user_service.credit_account(user.username, 20, "NGN")
        self.user_service.credit_account(user.username, 30, "GBP")
        self.user_service.credit_account(user.username, 40, "YUAN")

        self.assertEqual(user.username, "valid_username")
        self.assertEqual(user.wallets["USD"], 10)
        self.assertEqual(user.wallets["NGN"], 20)
        self.assertEqual(user.wallets["GBP"], 30)
        self.assertEqual(user.wallets["YUAN"], 40)

    def test_credit_user_account_with_negative_amount__error(self):
        """
        Test: test_credit_user_account_with_negative_amount__error
        """
        
        user = self.user_service.create_user("valid_username_01")

        with self.assertRaises(Exception) as context:
            self.user_service.credit_account(user.username, -3, "USD")
            
        self.assertTrue("Amount must be greater than ZERO!" in str(context.exception))

    def test_credit_user_account_with_zero_amount__error(self):
        """
        Test: test_credit_user_account_with_zero_amount__error
        """
        
        user = self.user_service.create_user("valid_username_02")

        with self.assertRaises(Exception) as context:
            self.user_service.credit_account(user.username, 0, "USD")
            
        self.assertTrue("Amount must be greater than ZERO!" in str(context.exception))

    def test_credit_user_that_does_not_exist__error(self):
        """
        Test: test_credit_user_that_does_not_exist__error
        """
        
        not_found_username = "@not_found_username_404"

        with self.assertRaises(Exception) as context:
            self.user_service.credit_account(not_found_username, 7, "USD")
            
        self.assertTrue("User not found!" in str(context.exception))

    def test_credit_user_with_unsupported_currency__error(self):
        """
        Test: test_credit_user_with_unsupported_currency__error
        """
        
        user = self.user_service.create_user("valid_username_credit_01")

        with self.assertRaises(Exception) as context:
            self.user_service.credit_account(user.username, 7, "ABC")
            
        self.assertTrue("Invalid currency!" in str(context.exception))

    def test_credit_user_that_multiple_credits_gives_correct_balance__success(self):
        """
        Test: test_credit_user_that_multiple_credits_gives_correct_balance__success
        """
        
        valid_username = "@multiple_credit_user"
        user = self.user_service.create_user(valid_username)

        self.user_service.credit_account(valid_username, 7, "USD")
        self.user_service.credit_account(valid_username, 2500, "USD")
        self.user_service.credit_account(valid_username, 16, "USD")
            
        self.assertEqual(user.wallets["USD"], 2523)
        self.assertEqual(user.username, valid_username)

    def test_credit_user_for_different_users_and_gives_correct_balance__success(self):
        """
        Test: test_credit_user_for_different_users_and_gives_correct_balance__success
        """
        
        user_1 = self.user_service.create_user("different_user_001")
        user_2 = self.user_service.create_user("different_user_002")

        user_1 = self.user_service.credit_account(user_1.username, 387, "USD")
        user_2 = self.user_service.credit_account(user_2.username, 7843, "USD")
            
        self.assertEqual(user_1.wallets["USD"], 387)
        self.assertEqual(user_2.wallets["USD"], 7843)


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
            self.user_service.transfer(user.username, 10, "USD")
            
        self.assertTrue("Insufficient account balance!" in str(context.exception))

    def test_transfer_money_with_negative_amount__error(self):
        """
        Test: test_transfer_money_with_negative_amount__error
        """
        
        user = self.user_service.create_user("valid_username_002")

        with self.assertRaises(Exception) as context:
            self.user_service.transfer(user.username, -2.5, "USD")
            
        self.assertTrue("Amount must be greater than ZERO!" in str(context.exception))

    def test_transfer_money_with_zero_amount__error(self):
        """
        Test: test_transfer_money_with_zero_amount__error
        """
        
        user = self.user_service.create_user("valid_username_003")

        with self.assertRaises(Exception) as context:
            self.user_service.transfer(user.username, 0, "USD")
            
        self.assertTrue("Amount must be greater than ZERO!" in str(context.exception))

    def test_transfer_money_for_non_existing_user__error(self):
        """
        Test: test_transfer_money_for_non_existing_user__error
        """
        
        not_found_username = "@valid_username_003__404"

        with self.assertRaises(Exception) as context:
            self.user_service.transfer(not_found_username, 3, "USD")
            
        self.assertTrue("User not found!" in str(context.exception))

    def test_transfer_money_with_unsupported_currency__error(self):
        """
        Test: test_transfer_money_with_unsupported_currency__error
        """
        
        user = self.user_service.create_user("valid_username_transfer_01")

        with self.assertRaises(Exception) as context:
            self.user_service.transfer(user.username, 7, "ABC")
            
        self.assertTrue("Invalid currency!" in str(context.exception))

    def test_transfer_money_multiple_times_gives_correct_balance__success(self):
        """
        Test: test_transfer_money_multiple_times_gives_correct_balance__success
        """
        
        valid_username = "@multiple_credit_user_001"
        user = self.user_service.create_user(valid_username)
        self.user_service.credit_account(valid_username, 1000, "USD")

        self.user_service.transfer(valid_username, 100, "USD")
        self.user_service.transfer(valid_username, 200, "USD")
        self.user_service.transfer(valid_username, 300, "USD")
        self.user_service.transfer(valid_username, 350, "USD")
            
        self.assertEqual(user.wallets["USD"], 50)

    def test_transfer_money_that_allows_for_sender_multicurrency_debit__success(self):
        """
        Test: test_transfer_money_that_allows_for_sender_multicurrency_debit__success
        """
        
        sender = self.user_service.create_user("_username_025")

        self.user_service.credit_account(sender.username, 20, "USD")
        self.user_service.credit_account(sender.username, 1000, "NGN")

        self.user_service.transfer(sender.username, 22, "USD")

        self.assertEqual(sender.wallets["USD"], 0)
        self.assertEqual(sender.wallets["NGN"], (1000 - (2 * 415)))
        self.assertEqual(sender.wallets["GBP"], 0)
        self.assertEqual(sender.wallets["YUAN"], 0)

    def test_transfer_money_that_allows_for_sender_multicurrency_debit__insufficient_success(self):
        """
        Test: test_transfer_money_that_allows_for_sender_multicurrency_debit__insufficient_success
        """
        
        sender = self.user_service.create_user("_username_125")

        self.user_service.credit_account(sender.username, 20, "USD")
        self.user_service.credit_account(sender.username, 1000, "NGN")

        with self.assertRaises(Exception) as context:
            self.user_service.transfer(sender.username, 30, "USD")
            
        self.assertTrue("Insufficient account balance!" in str(context.exception))


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
            self.user_service.send(user_1.username, user_2.username, 10, "USD")
            
        self.assertTrue("Insufficient account balance!" in str(context.exception))

    def test_send_money_with_negative_amount__error(self):
        """
        Test: test_send_money_with_negative_amount__error
        """
        
        user_1 = self.user_service.create_user("_username_003")
        user_2 = self.user_service.create_user("_username_004")

        with self.assertRaises(Exception) as context:
            self.user_service.send(user_1.username, user_2.username, -9999.999, "USD")
            
        self.assertTrue("Amount must be greater than ZERO!" in str(context.exception))

    def test_send_money_with_zero_amount__error(self):
        """
        Test: test_send_money_with_zero_amount__error
        """
        
        user_1 = self.user_service.create_user("_username_005")
        user_2 = self.user_service.create_user("_username_006")

        with self.assertRaises(Exception) as context:
            self.user_service.send(user_1.username, user_2.username, 0, "USD")
            
        self.assertTrue("Amount must be greater than ZERO!" in str(context.exception))

    def test_send_money_to_non_existing_user__error(self):
        """
        Test: test_send_money_to_non_existing_user__error
        """
        
        sender = self.user_service.create_user("_username_007")
        self.user_service.credit_account(sender.username, 100, "USD")

        not_found_username = "@_username_006_404"

        with self.assertRaises(Exception) as context:
            self.user_service.send(sender.username, not_found_username, 3, "USD")
            
        self.assertTrue("User not found!" in str(context.exception))

    def test_send_money_with_unsupported_currency__error(self):
        """
        Test: test_send_money_with_unsupported_currency__error
        """
        
        user_1 = self.user_service.create_user("valid_username_send_01")
        user_2 = self.user_service.create_user("valid_username_send_02")

        with self.assertRaises(Exception) as context:
            self.user_service.send(user_1.username, user_2.username, 7, "ABC")
            
        self.assertTrue("Invalid currency!" in str(context.exception))

    def test_send_money_multiple_times_gives_correct_balances__success(self):
        """
        Test: test_send_money_multiple_times_gives_correct_balances__success
        """
        
        user_1 = self.user_service.create_user("_username_008")
        user_2 = self.user_service.create_user("_username_009")

        self.user_service.credit_account(user_1.username, 100, "USD")
        self.user_service.credit_account(user_2.username, 50, "USD")

        self.user_service.send(user_1.username, user_2.username, 5, "USD")
        self.user_service.send(user_1.username, user_2.username, 10, "USD")
        self.user_service.send(user_1.username, user_2.username, 15, "USD")
        self.user_service.send(user_1.username, user_2.username, 20, "USD")

        self.assertEqual(user_1.wallets["USD"], 50)
        self.assertEqual(user_2.wallets["USD"], 100)

    def test_send_money_to_oneself__error(self):
        """
        Test: test_send_money_to_oneself__error
        """
        
        sender = self.user_service.create_user("_username_010")
        self.user_service.credit_account(sender.username, 250, "USD")

        with self.assertRaises(Exception) as context:
            self.user_service.send(sender.username, sender.username, 250, "USD")
            
        self.assertTrue("Invalid operation - cannot send money to one's self!" in str(context.exception))

    def test_send_money_that_allows_for_sender_multicurrency_debit__success(self):
        """
        Test: test_send_money_that_allows_for_sender_multicurrency_debit__success
        """
        
        sender = self.user_service.create_user("_username_020")
        recipient = self.user_service.create_user("_username_030")

        self.user_service.credit_account(sender.username, 20, "USD")
        self.user_service.credit_account(sender.username, 1000, "NGN")

        self.user_service.credit_account(recipient.username, 3, "USD")
        self.user_service.credit_account(recipient.username, 3, "YUAN")

        self.user_service.send(sender.username, recipient.username, 22, "USD")

        self.assertEqual(sender.wallets["USD"], 0)
        self.assertEqual(sender.wallets["NGN"], (1000 - (2 * 415)))
        self.assertEqual(sender.wallets["GBP"], 0)
        self.assertEqual(sender.wallets["YUAN"], 0)

        self.assertEqual(recipient.wallets["USD"], 25)
        self.assertEqual(recipient.wallets["NGN"], 0)
        self.assertEqual(recipient.wallets["GBP"], 0)
        self.assertEqual(recipient.wallets["YUAN"], 3)

    def test_send_money_that_allows_for_sender_multicurrency_debit__insufficient_error(self):
        """
        Test: test_send_money_that_allows_for_sender_multicurrency_debit__insufficient_error
        """
        
        sender = self.user_service.create_user("_username_120")
        recipient = self.user_service.create_user("_username_130")

        self.user_service.credit_account(sender.username, 20, "USD")
        self.user_service.credit_account(sender.username, 1000, "NGN")

        self.user_service.credit_account(recipient.username, 3, "USD")

        with self.assertRaises(Exception) as context:
            self.user_service.send(sender.username, recipient.username, 50, "USD")
            
        self.assertTrue("Insufficient account balance!" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
