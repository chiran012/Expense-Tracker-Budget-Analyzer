from datetime import date

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
    income = []
    categories = []

    add_category(categories, "food", 200)
    add_category(categories, "transport", 50)

    print()
    add_expense(categories, "food", 50)    # 25% - just logged
    add_expense(categories, "food", 110)   # 80% - approaching limit
    add_expense(categories, "food", 30)    # 95% - still approaching
    add_expense(categories, "food", 20)    # 105% - over budget

    print()
    add_expense(categories, "transport", 60)  # over budget on first log
    add_expense(categories, "rent", 10)       # category doesn't exist

    print()
    add_category(categories, "entertainment", -15)
    add_expense(categories, "entertainment", 15)  # should refuse - zero budget

    print("\n--- Summary ---")
    show_summary(categories)

if __name__ == "__main__":
    main()