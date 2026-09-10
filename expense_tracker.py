import time, sys
import json
from datetime import date

def save_data(categories, income, filename="budget_data.json"):

    for category in categories:
        for entry in category['spendings']:
            entry['date'] = entry['date'].isoformat()

    for entry in income:
        entry['date'] = entry['date'].isoformat()

    data = {
        'categories' : categories,
        'income' : income
    }

    with open(filename, "w") as file:
        json.dump(data, file)

def load_data(filename="budget_data.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            categories = data['categories']
            income = data['income']

            for category in categories:
                for entry in category['spendings']:
                    entry['date'] = date.fromisoformat(entry['date'])

            for entry in income:
                entry['date'] = date.fromisoformat(entry['date'])

            return categories, income
    except FileNotFoundError:
        return [], []

def animation(message = "Loading", duration = 2):
    end_time = time.time() + duration   
    while end_time > time.time():
        for dots in range(1, 6):
            sys.stdout.write(f"\r{message}{'.' * dots}{' ' *(5-dots)}")
            sys.stdout.flush()
            time.sleep(0.3)
    sys.stdout.write("\r" + " " * (len(message) + 10) + "\r")
    sys.stdout.flush()

def clear_line(text):
  sys.stdout.write("\r" + " " * (len(text) + 10) + "\r")
  sys.stdout.flush()

def loading_animation(message, duration=2):
    animation(message, duration)
    text = "Done!"
    sys.stdout.write(f"\r{text}")
    sys.stdout.flush()
    time.sleep(1)
    clear_line(text)

def add_category(categories, category_name, max_budget):
    for category in categories:
        if category_name == category['category_name']:
            category['max_budget'] += max_budget
            print(f"Successfully updated maximum budget for category '{category_name}'")
            return
        
    category_details = {
        'category_name' : category_name,
        'max_budget' : max_budget,
        'spendings' : [],
        'total_amount_spent' : 0,
    }
    categories.append(category_details)
    print(f"Successfully added category named '{category_name}'")


def calculate_percent_spent(category):
    if category['max_budget'] != 0:
        return (category['total_amount_spent'] / category['max_budget']) * 100
    return 0

def add_income(income, amount):
    income_entry = {
        'date' : date.today(),
        'amount' : amount
    }
    income.append(income_entry)

def overspending(categories):
    if not categories:
        print("Error! Add some category and spendings first")
        return

    overspent_category = 0
    amount_overspent = 0
    is_overspent = False
    for index, category in enumerate(categories):
        if category['total_amount_spent'] < 0:
            print("Error! Negative balance in total amount spent")
            return
        
        if category['total_amount_spent'] > category['max_budget']:
            overspent = abs(category['max_budget'] - category['total_amount_spent'])
            if overspent > amount_overspent:
                overspent_category = index
                amount_overspent = overspent
                is_overspent = True

    if is_overspent:
        print(f"Overspent category with furthest spendings compared to max budget : '{categories[overspent_category]['category_name']}' by ${amount_overspent:.2f}")
        return
    print(f"No category with spendings more than budget.")

def add_expense(categories, category_name, amount):
    if not categories:
        print("Error! No categories found. Add some categories first")
        return

    for category in categories:
        if category_name == category['category_name']:
            if category['max_budget'] <= 0:
                print("Cannot add spendings if the category's budget is zero or negative. Update it first to add spendings")
                return
            spending_details = {
                'date' : date.today(),
                'amount_spent' : amount
            }
            category['spendings'].append(spending_details)
            category['total_amount_spent'] += amount

            percent_spent = calculate_percent_spent(category)
            if percent_spent < 80:
                print(f"\nLogged ${amount:.2f} in '{category_name}'")
            if percent_spent >= 80 and percent_spent < 100:
                print(f"\nApproaching your budget limit for {category_name}")
                print(f"Total spendings in percentage : {percent_spent:.2f}")
            elif percent_spent >= 100:
                exceeded_amount = category['total_amount_spent'] - category['max_budget']
                print(f"\nOver 100% used over budget for '{category_name}' by ${exceeded_amount:.2f}")
            return
    print(f"\nNo category found with the name '{category_name}'")
    return

def show_summary(categories):
    if not categories:
        print("Error! No categories found. Add some categories first")
        return

    for category in categories:
        if category['max_budget'] <= 0:
            print(f"\nNo spending data available for '{category['category_name']}' because of ${category['max_budget']:.2f} budget.")
            continue
        percent_spent = calculate_percent_spent(category)
        print(f"\nCategory name : {category['category_name']}")
        print(f"Max budget : ${category['max_budget']:.2f}")
        print(f"Total amount spent : ${category['total_amount_spent']:.2f} | Percent : {percent_spent:.2f}")
        print("Spendings details : ")
        for details in category['spendings']:
            print("-"*50)
            print(f"    Date : {details['date']}")
            print(f"    Amount spent : ${details['amount_spent']:.2f}")
            print("-"*50)
    return

def total_spent_in_month(categories, target_month, target_year):
    total = 0
    for category in categories:
        for entry in category['spendings']:
            if entry['date'].month == target_month and entry['date'].year == target_year:
                total += entry['amount_spent']
    return total

def total_spent_in_year(categories, target_year):
    total = 0
    for month in range(1, 13):
        total += total_spent_in_month(categories, month, target_year)
    return total

def total_income_in_year(income, target_year):
    total = 0
    for month in range(1, 13):
        total += total_income_in_month(income, month, target_year)
    return total

def total_income_in_month(income, target_month, target_year):
    total = 0
    for entry in income:
        if entry['date'].month == target_month and entry['date'].year == target_year:
            total += entry['amount']
    return total

def calculate_net_for_month(categories, income, target_month, target_year):
    target_month_spendings = total_spent_in_month(categories, target_month, target_year)
    target_month_income = total_income_in_month(income, target_month, target_year)

    print(f"Net for month {target_month}/{target_year} : ${target_month_income - target_month_spendings:.2f}")
    return

def calculate_net_for_year(categories, income, target_year):
    target_year_income = total_income_in_year(income, target_year)
    target_year_spendings = total_spent_in_year(categories, target_year)

    print(f"Net for year {target_year} ${target_year_income - target_year_spendings:.2f}")
    return

def year_to_year_comparison(categories, first_year, next_year):
    if not categories:
        print("Error! No categories found. Add some categories and spendings first")
        return

    first_year_total = total_spent_in_year(categories, first_year)
    next_year_total = total_spent_in_year(categories, next_year)

    if first_year_total > next_year_total:
        print(f"Year '{first_year}' has higher spendings than '{next_year}' by ${first_year_total - next_year_total:.2f}")
        print(f"Total spendings : ${first_year_total:.2f}")
        return
    elif next_year_total > first_year_total:
        print(f"Year '{next_year}' has higher spendings than '{first_year}' by ${next_year_total - first_year_total:.2f}")
        print(f"Total spendings : ${next_year_total:.2f}")
        return
    else:
        print(f"Both years have same spendings of ${first_year_total:.2f}")
        return


def month_to_month_comparison(categories, first_month, first_year, next_month, next_year):
    if not categories:
        print("Error! No categories found. Add some categories and spendings first")
        return
    
    first_month_total = total_spent_in_month(categories, first_month, first_year)
    next_month_total = total_spent_in_month(categories, next_month, next_year)

    if first_month_total > next_month_total:
        print(f"'{first_month}' has higher spendings than '{next_month}' by ${first_month_total - next_month_total:.2f}")
        print(f"Total spendings : ${first_month_total:.2f}")
        return
    elif first_month_total < next_month_total:
        print(f"'{next_month}' has higher spendings than '{first_month}' by ${next_month_total - first_month_total:.2f}")
        print(f"Total spendings : ${next_month_total:.2f}")
        return
    else:
        print(f"Both months has same spendings of ${first_month_total:.2f}")
        return


def main():
    loading_animation("Lodaing data", duration = 4)
    income = []
    categories = []

    categories, income = load_data()

    while True:
        print("\n" + "=" * 60)
        print("EXPENSE TRACKER & BUDGET ANALYZER".center((60)))
        print("="*60)
        print("1. Add category / set budget")
        print("2. Log an expense")
        print("3. Log income")
        print("4. View summary")
        print("5. Check overspending")
        print("6. Compare two months")
        print("7. Compare two years")
        print("8. Calculate net for month")
        print("9. Calculate net for year")
        print("10. Exit")
        print("-" * 60)

        try:
            choice = int(input("Enter from the above options (1-10) : "))
            if choice in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                if choice == 1:
                    category_name = input("Enter category name : ")
                    max_budget = float(input("Enter your budget : $"))
                    loading_animation("Adding category / setting budget", duration = 2)
                    
                    add_category(categories, category_name, max_budget)

                elif choice == 2:
                    category_name = input("Enter category name : ")
                    expense = float(input("Enter expense amount : $"))

                    add_expense(categories, category_name, expense)

                elif choice == 3:
                    amount = float(input("Enter your income amount : $"))
                    loading_animation("Logging income", duration = 2)

                    add_income(income, amount)

                elif choice == 4:
                    loading_animation("Loading summary", duration = 2)
                    show_summary(categories)

                elif choice == 5:
                    loading_animation("Checking overspendings", duration = 2)
                    overspending(categories)

                elif choice == 6:
                    first_month = int(input("Input first month in number (1-12) : "))
                    first_year = int(input("Input first year (eg: 2026) : "))
                    second_month = int(input("Enter second month in number : "))
                    second_year = int(input("Enter second year : "))
                    loading_animation(f"Comparing month {first_month} of {first_year} with month {second_month} of {second_year}", duration = 2)

                    month_to_month_comparison(categories, first_month, first_year, second_month, second_year)

                elif choice == 7:
                    first_year = int(input("Enter first year (eg: 2025) : "))
                    second_year = int(input("Enter second year : "))
                    loading_animation(f"Comparing year {first_year} with year {second_year}", duration = 2)

                    year_to_year_comparison(categories, first_year, second_year)

                elif choice == 8:
                    month = int(input("Enter month in number (1-12) : "))
                    year = int(input("Enter year (eg: 2026) : "))
                    loading_animation(f"Calculating net for month {month} of {year}", duration = 2)

                    calculate_net_for_month(categories, income, month, year)

                elif choice == 9:
                    year = int(input("Enter year (eg: 2026) : "))
                    loading_animation(f"Calculating net for year {year}", duration = 2)

                    calculate_net_for_year(categories, income, year)

                else:
                    loading_animation("Exiting expense tracker & budget analyzer", duration = 3)
                    print("Thank you for using expense tracker & budget analyzer!")
                    break
            else:
                print("Error! Invalid choice")
                continue
        except ValueError:
            print("Error! Invalid input")
            continue
    save_data(categories, income)

if __name__ == "__main__":
    main()