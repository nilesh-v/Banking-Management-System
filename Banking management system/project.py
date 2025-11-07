import random
import datetime
import pickle
import os

class Account:
    def __init__(self, name, initial_deposit, account_type):
        self.account_number = self.generate_account_number()
        self.name = name
        self.balance = initial_deposit
        self.account_type = account_type
        self.transactions = []
        self.date_opened = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.is_active = True
        
    def generate_account_number(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(10)])
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.record_transaction("Deposit", amount)
            return True
        return False
    
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.record_transaction("Withdrawal", -amount)
            return True
        return False
    
    def transfer(self, amount, target_account):
        if self.withdraw(amount):
            target_account.deposit(amount)
            self.record_transaction("Transfer to " + target_account.account_number, -amount)
            target_account.record_transaction("Transfer from " + self.account_number, amount)
            return True
        return False
    
    def record_transaction(self, transaction_type, amount):
        transaction = {
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'type': transaction_type,
            'amount': amount,
            'balance': self.balance
        }
        self.transactions.append(transaction)
    
    def get_statement(self):
        statement = f"Account Statement for {self.name} ({self.account_number})\n"
        statement += f"Account Type: {self.account_type}\n"
        statement += f"Current Balance: {self.balance:.2f}\n\n"
        statement += "Date                 Type          Amount       Balance\n"
        statement += "-" * 60 + "\n"
        
        for transaction in self.transactions:
            statement += f"{transaction['date']}  {transaction['type']:12}  {transaction['amount']:10.2f}  {transaction['balance']:10.2f}\n"
        
        return statement
    
    def close_account(self):
        if self.balance == 0:
            self.is_active = False
            return True
        return False
    
    def __str__(self):
        return (f"Account Number: {self.account_number}\n"
                f"Customer Name: {self.name}\n"
                f"Account Type: {self.account_type}\n"
                f"Balance: {self.balance:.2f}\n"
                f"Date Opened: {self.date_opened}\n"
                f"Status: {'Active' if self.is_active else 'Closed'}")


class Bank:
    def __init__(self, name):
        self.name = name
        self.accounts = {}
        self.load_accounts()
    
    def create_account(self, name, initial_deposit, account_type):
        account = Account(name, initial_deposit, account_type)
        self.accounts[account.account_number] = account
        self.save_accounts()
        return account
    
    def get_account(self, account_number):
        return self.accounts.get(account_number)
    
    def delete_account(self, account_number):
        account = self.accounts.get(account_number)
        if account and account.close_account():
            del self.accounts[account_number]
            self.save_accounts()
            return True
        return False
    
    def save_accounts(self):
        with open('bank_data.pkl', 'wb') as f:
            pickle.dump(self.accounts, f)
    
    def load_accounts(self):
        if os.path.exists('bank_data.pkl'):
            with open('bank_data.pkl', 'rb') as f:
                self.accounts = pickle.load(f)
    
    def get_all_accounts(self):
        return self.accounts.values()
    
    def total_deposits(self):
        return sum(account.balance for account in self.accounts.values() if account.is_active)
    
    def search_accounts(self, search_term):
        results = []
        for account in self.accounts.values():
            if (search_term.lower() in account.name.lower() or 
                search_term in account.account_number):
                results.append(account)
        return results


class BankApp:
    def __init__(self):
        self.bank = Bank("Python OOP Bank")
        self.current_account = None
        self.run()
    
    def display_menu(self):
        if not self.current_account:
            print("\nWelcome to", self.bank.name)
            print("1. Create Account")
            print("2. Login")
            print("3. Exit")
        else:
            print(f"\nWelcome, {self.current_account.name}")
            print("1. View Account Details")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Transfer")
            print("5. View Statement")
            print("6. Close Account")
            print("7. Logout")
    
    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            
            if not self.current_account:
                if choice == '1':
                    self.create_account()
                elif choice == '2':
                    self.login()
                elif choice == '3':
                    print("Thank you for banking with us!")
                    break
                else:
                    print("Invalid choice. Please try again.")
            else:
                if choice == '1':
                    self.view_account_details()
                elif choice == '2':
                    self.deposit()
                elif choice == '3':
                    self.withdraw()
                elif choice == '4':
                    self.transfer()
                elif choice == '5':
                    self.view_statement()
                elif choice == '6':
                    self.close_account()
                elif choice == '7':
                    self.logout()
                else:
                    print("Invalid choice. Please try again.")
    
    def create_account(self):
        print("\nCreate New Account")
        name = input("Enter your full name: ")
        account_type = input("Enter account type (Savings/Current): ").capitalize()
        initial_deposit = float(input("Enter initial deposit amount: "))
        
        if initial_deposit < 0:
            print("Initial deposit cannot be negative.")
            return
            
        account = self.bank.create_account(name, initial_deposit, account_type)
        print("\nAccount created successfully!")
        print(f"Your account number is: {account.account_number}")
    
    def login(self):
        print("\nLogin to Your Account")
        account_number = input("Enter your account number: ")
        account = self.bank.get_account(account_number)
        
        if account and account.is_active:
            self.current_account = account
            print(f"Welcome back, {account.name}!")
        else:
            print("Account not found or is closed.")
    
    def view_account_details(self):
        print("\nAccount Details:")
        print(self.current_account)
    
    def deposit(self):
        amount = float(input("Enter amount to deposit: "))
        if self.current_account.deposit(amount):
            self.bank.save_accounts()
            print(f"Deposit successful. New balance: {self.current_account.balance:.2f}")
        else:
            print("Invalid deposit amount.")
    
    def withdraw(self):
        amount = float(input("Enter amount to withdraw: "))
        if self.current_account.withdraw(amount):
            self.bank.save_accounts()
            print(f"Withdrawal successful. New balance: {self.current_account.balance:.2f}")
        else:
            print("Invalid withdrawal amount or insufficient funds.")
    
    def transfer(self):
        target_account_number = input("Enter recipient's account number: ")
        target_account = self.bank.get_account(target_account_number)
        
        if not target_account or not target_account.is_active:
            print("Recipient account not found or is closed.")
            return
        
        if target_account.account_number == self.current_account.account_number:
            print("Cannot transfer to the same account.")
            return
            
        amount = float(input("Enter amount to transfer: "))
        
        if self.current_account.transfer(amount, target_account):
            self.bank.save_accounts()
            print(f"Transfer successful. New balance: {self.current_account.balance:.2f}")
        else:
            print("Transfer failed. Check amount and balance.")
    
    def view_statement(self):
        print("\nAccount Statement")
        print(self.current_account.get_statement())
    
    def close_account(self):
        if self.current_account.balance == 0:
            if self.bank.delete_account(self.current_account.account_number):
                print("Account closed successfully.")
                self.current_account = None
            else:
                print("Failed to close account.")
        else:
            print("Cannot close account with non-zero balance.")
    
    def logout(self):
        self.current_account = None
        print("Logged out successfully.")


if __name__ == "__main__":
    BankApp()