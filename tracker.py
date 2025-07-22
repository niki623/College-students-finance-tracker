import os

def clear_screen(): #to clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')

def validateInput(prompt, validator_func, error_message): #general invalid input function
    while True:
        try:
            user_input = input(prompt)
            if validator_func(user_input):
                return user_input
            print(error_message)
        except ValueError:
            print(error_message)

def validatePositiveFloat(value): #to ensure non-negative numbers are entered
    try:
        float_value = float(value)
        return float_value >= 0
    except ValueError:
        return False

def validateYesNo(value):
    """
    Validate Yes/No input.
    """
    return value.upper() in ['Y', 'N']

def addExpenseCategory(): #function to add expense categories to default list of expenses
    expenseCategories = [
        "Transportation fees",
        "School-related expenses",
        "Food",
        "Rent/Utilities",
        "Miscellaneous",
        "Personal expenses"
    ]

    while True:
        clear_screen()

        #display current expense categories
        print('\nCurrent Expense Categories:') 
        print('-' * 50)
        for i, category in enumerate(expenseCategories, 1):
            print(f"{i}. {category}")

        #input and validate add more categories choice (either yes or no)
        addMoreChoice = validateInput(
            '\nWould you like to add more categories? (Y/N): ', 
            validateYesNo, 
            "Invalid input. Please enter Y or N.\n"
        ).upper()

        if addMoreChoice != "Y":
            break

        #input and validate new category input: must not already exist and must not be empty
        newCategory = validateInput(
            'Please input your custom expense category (non-empty, unique): ', 
            lambda x: x.strip() and x not in expenseCategories, 
            "Invalid category. Category must be non-empty and not already exist.\n"
        )
        expenseCategories.append(newCategory)
    
    return expenseCategories

def collectExpenses(expenseCategories, isWeekly): #function to input expense amount per category
    expenses = {}
    timeframe = 'weekly' if isWeekly else 'monthly'

    clear_screen()  
    print("Great! You’ve entered all your expense categories.")
    print("Now, input your expenses for each category. If a category doesn't apply to you, enter 0.\n")

    #loop through each categroy, inputing the respective amount
    for category in expenseCategories:
        # Validate expense amount for each category
        amount = float(validateInput(
            f"Enter the {timeframe} amount for {category} in PHP: ", 
            validatePositiveFloat, 
            "Invalid amount. Please enter a non-negative number.\n"
        ))

        #convert weekly expense to its monthly equivalent if needed(multiply by 4)
        if isWeekly:
            amount *= 4

        expenses[category] = amount

    return expenses

def displayResults(monthlyIncome, expenses, goalBudget): #function to calculate and display results

    totalExpenses = sum(amount for amount in expenses.values())

    clear_screen() 
    print('='*90)
    print("END-OF-MONTH EXPENSE RESULTS") #print table header
    print('='*90)
    
    #print monthly allowance, total expenses, daily and weekly average expenditure
    print(f"{'Monthly Allowance': <38} {'PHP':>5} {monthlyIncome:<10.2f}")

    print(f"{'Total Expenses':<38} {'PHP':>5} {totalExpenses:<10.2f}")
    net = monthlyIncome - totalExpenses
    projectedValue = 12 * net

    daily_avg = totalExpenses / 30
    print(f"{'Approx. daily expenditure':<38} {'PHP':>5} {daily_avg:<10.2f} {''}") #Assuming 30 days in the month

    weekly_avg = totalExpenses / 4
    print(f"{'Approx. weekly expenditure':<38} {'PHP':>5} {weekly_avg:<10.2f}") #Assuming 4 weeks in the month

    print('\n'+'-'*90)
    print("SUMMARY")
    print('-'*90)

    #display net value and portion of allowance saved/spent:
    if net == 0: #for no net gain/deficit
        print(f"{'Net value': <38} {'PHP':>5} {net:<10.2f}")
        print("You did not experience a net gain or deficit this month.")
    elif net < 0: #for net deficit
        portionSpent = (totalExpenses / monthlyIncome) * 100
        print(f"{'Portion of allowance spent': <40} {portionSpent:<3.2f} {'%':<3}") #display portion of allowance spent
        print(f"{'Net Deficit': <38} {'PHP':>5} {net:<10.2f}")
        print("❌ Deficit alert!")
    else: #for net gain
        portionSaved = (net / monthlyIncome) * 100
        print(f"{'Portion of allowance saved': <40} {portionSaved:<3.2f} {'%':<3}") #display portion of allowance saved
        print(f"{'Net Gain': <38} {'PHP':>5} {net:<10.2f}")

    print(f"{'\nGoal Budget':<39} {'PHP':>5} {goalBudget:<10.2f}")     # Display how user is faring towards goal budget
    if net == goalBudget: #if net gain is exactly equal to the goal budget
        print("Congratulations! You are exactly meeting your set goal budget!")
        print(f"{'Projected savings after 12 months':<38} {'PHP':>5} {projectedValue:<10.2f}")        
        print("👍 Great budgeting!")
    else:  #for net values not equal to the goal budget
        difference = abs(net - goalBudget)
        if net > goalBudget: #exceeding goal budget
            print(f"Congratulations! You have met your set goal budget and still have PHP {difference:.2f} remaining!")
            print(f"{'Projected savings after 12 months':<38} {'PHP':>5} {projectedValue:<10.2f}")        
            print("👍 Great budgeting!")
        elif net < goalBudget and net >= 0: #net is less than goal budget but non-negative
            print(f"You are PHP {difference:.2f} short of your goal budget.")
            print(f"{'Projected savings after 12 months':<38} {'PHP':>5} {projectedValue:<10.2f}")        
            print("⚠️ Be careful, you're overspending!")
        else: #net is negative(and thus less than goal budget)
            print(f"You are PHP {difference:.2f} short of your goal budget.")
            print(f"{'Projected deficit after 12 months':<38} {'PHP':>5} {projectedValue:<10.2f}")        
            print("⚠️ Be careful, you're overspending!")

    print("\n" + '-'*90)
    print(f"{'EXPENSE BREAKDOWN': <40} {'Cost' :<15} {'Percent':>10}")
    print('-'*90)
    
    def percentage(amount): #function to calculate a category's portion of the total expense
        return (amount / totalExpenses) * 100 if totalExpenses > 0 else 0

    #display all expenses with percentages
    for i, (category, amount) in enumerate(expenses.items(),1):
        print(f"{i}. {category:<35} {'PHP':>5} {amount:<10.2f} {percentage(amount):>10.2f}%")
    
    #display Top 3 biggest expenses
    print("\nTop 3 biggest expenses:")
    sortedExpenses = sorted(expenses.items(), key=lambda x: x[1], reverse=True) #sort by descending order
    topExpenses = sortedExpenses[:3]  #get top 3 expenses
    for i, (item, cost) in enumerate(topExpenses, 1):
        print(f"{i}. {item:<35} {'PHP':>5} {cost:<10.2f} {percentage(cost):>10.2f}%")

    #display saving tips for top 3 expenses
    topExpenseCategories = [item for item, cost in topExpenses]
    print('')
    if "Transportation fees" in topExpenseCategories:   
        print("🚗 Tip! Walk, carpool, or commute to reduce transportation costs!")
    if "School-related expenses" in topExpenseCategories: 
        print("📚Tip! Buy used textbooks, use library resources, and borrow materials from classmates to reduce school-related expenses!")
    if "Food" in topExpenseCategories:
        print("🧑‍🍳Tip! Cook instead of ordering food to reduce food expenses!")
    if "Rent/Utilities" in topExpenseCategories:
        print("⚡️Tip! Find roommates to split rent and utilities, and conserve electricity and water!")
    if "Personal expenses" in topExpenseCategories or "Miscellaneous" in topExpenseCategories:
        print("💡Tip! Avoid impulse purchases and avail of second-hand items to reduce unnecessary expenses!")
    print('')

def runTracker(): #function to run tracker
    clear_screen()
    print('Welcome to the Expense Tracker!')
    print('This program will analyze your monthly finances based on your allowance, expenses, and goal budget.')
    
    #input and validate income input type (weekly or monthly)
    while True:
        choice = validateInput(
            '\nDo you want to input monthly or weekly expenses and allowance? (input m or w): ', 
            lambda x: x.lower() in ['m', 'w'], 
            "Invalid input. Please enter m for monthly or w for weekly."
        ).lower()

        #input and validate income amount
        if choice == 'w':
            weeklyAllowance = float(validateInput(
                'Please input your weekly allowance in PHP: ', 
                validatePositiveFloat, 
                "Invalid amount. Please enter a non-negative number."
            ))
            monthlyIncome = 4 * weeklyAllowance
            isWeekly = True
            break
        elif choice == 'm':
            monthlyIncome = float(validateInput(
                'Please input your monthly allowance in PHP: ', 
                validatePositiveFloat, 
                "Invalid amount. Please enter a non-negative number."
            ))
            isWeekly = False
            break
    
    #input and validate goal budget
    goalBudget = float(validateInput(
        'Please input your end-of-month goal budget in PHP: ', 
        validatePositiveFloat, 
        "Invalid amount. Please enter a non-negative number."
    ))
    

    expenseCategories = addExpenseCategory() #allow user to add expense categories
    expenseDictionary = collectExpenses(expenseCategories, isWeekly) #user inputs all expense amounts
    print("")
    input("Press enter to view your budget summary...")
    displayResults(monthlyIncome, expenseDictionary, goalBudget) #calculate and display analysis of expenses

def main():
    while True:
        runTracker()

        input("Press enter to continue...")
        clear_screen()
        #allow user to run the tracker again
        again = validateInput(
            "\nWould you like to track your finances again or input hypothetical expense values? (Y/N): ", 
            validateYesNo,
            "Invalid input. Please enter Y or N."
        ).upper()
        if again != 'Y':
            print("\nThank you for using our college finance tracker! Goodbye and happy budgeting! 💰\n")
            break

main()


