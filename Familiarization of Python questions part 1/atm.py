balance = 0
def check_balance():
    global balance
    if(balance == 0):
        print("No Balance")
    else:
        print("Balance = ",balance)
def deposit(cash):
    global balance
    if cash == 0:
        print("No cash to Deposit")
    else:
        balance+=cash
        print("Cash Deposited..")
def withdraw(cash):
    global balance
    check = balance-cash
    if(cash!=0 and balance!=0 and check>=0): 
        balance-=cash
        print("Cash Withdrawn..")
    else:
        print("Not available to Withdraw this cash")
while(1):
    print('''
        Menu
        ----
    1.Check Balance
    2.Deposit Money
    3.Withdraw Money
    4.Exit
    ''')
    choice = int(input("Enter the choice: "))
    if choice == 1:
        check_balance()
    elif choice == 2:
        cash = int(input("Enter the cash to deposit: "))
        deposit(cash)
    elif choice == 3:
        cash = int(input("Enter the cash to Withdraw: "))
        withdraw(cash)
    else:
        print("Thank you")
        break