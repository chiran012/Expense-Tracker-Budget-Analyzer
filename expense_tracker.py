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


def main():
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