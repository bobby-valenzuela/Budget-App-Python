class Category:

  total_withdrawal_amount = 0
  withdrawn_amnt_by_cat = {}

  def __init__(self, name):
    self.name = name
    self.ledger = []
    self.balance = 0.00
    self.amount_withdrawn = 0.00

  def deposit(self, amount, description=''):
    self.ledger.append({"amount": amount, "description": description})
    self.balance += amount
  
  def withdraw(self, amount, description=''):
    if self.check_funds(amount):
      self.ledger.append({"amount": -amount, "description": description})
      self.balance -= amount
      self.amount_withdrawn += abs(amount)
      Category.total_withdrawal_amount += abs(amount)
      return True
    else:
      return False

  def transfer(self, amount, category):
    # If we have the funds, then process the transfer      
    if self.check_funds(amount):
      destination_budget_name = category.name
      self.withdraw(amount,f"Transfer to {destination_budget_name}")
      category.deposit(amount,f"Transfer from {self.name}")
      return True 
    else:
      return False

  def get_balance(self):
    return self.balance
  
  def check_funds(self,amount):
    if amount <= self.balance :
      return True
    else:
      return False

  def amount_spent(self):
    return self.amount_withdrawn / Category.total_withdrawal_amount 

  def __str__(self):

    output = ""
    total = 0.00

    # Manage title
    name_length = len(self.name)
    num_of_stars = 30 - name_length
    num_of_stars_per_side = int(num_of_stars/2)
    title = f"{'*'*num_of_stars_per_side}{self.name}{'*'*num_of_stars_per_side}\n"
    output = title

    # Manage list items
    for item in self.ledger:
      #  Description
      desc = f"{item['description']}"[0:23]
      desc_len = len(desc)
      # Amounts
      amnt = float(item['amount'])
      amnt_formatted = format(amnt,'.2f')
      amnt_formatted = amnt_formatted[0:6]
      amnt_len = len(amnt_formatted)
      total += amnt
      # Whitespace
      num_of_space = 30 - (desc_len + amnt_len)
      white_space = ' ' * num_of_space 
      # List item Output
      output += f"{desc}{white_space}{amnt_formatted}\n"

    output += f"Total: {total}"
    return output

def create_spend_chart(categories):

  chart = 'Percentage spent by category\n'
  
  # Build rows
  rows = {
    "100":"100|",
    "90":" 90|",
    "80":" 80|",
    "70":" 70|",
    "60":" 60|",
    "50":" 50|",
    "40":" 40|",
    "30":" 30|",
    "20":" 20|",
    "10":" 10|",
    "0" :"  0|"
  }

  name_rows = []
  name_rows_text = '    '
  longest_cat_name_len = 0

  cat_idx = -1

  for category in categories:

    balance = category.balance
    amount_spent = category.amount_spent()
    cat_idx += 1

    # Calculate Percentage
    percent_spent = amount_spent * 100
    amount_over_tenth_divisible = percent_spent % 10
    if amount_over_tenth_divisible >= 5 :
      percent_spent = percent_spent + ( 10.00 - amount_over_tenth_divisible )
    else:
      percent_spent = percent_spent - amount_over_tenth_divisible 
      
    num_of_circles = int( percent_spent / 10 )

    # Populate percent rows
    for i in range(0, 101, 10):
      # Adding circles
      if i <= percent_spent:
        # rows[f"{i}"] += f' {amount_spent}|{balance} '
        rows[f"{i}"] += f' o '
        # rows[f"{i}"] += f' {percent_spent} '
      else:
        rows[f"{i}"] += '   '
    
    # Determine longest name
    if len(category.name) > longest_cat_name_len:
      longest_cat_name_len = len(category.name)

    # Add to name matrix
    name_rows.append([])
    for n in category.name:
      name_rows[cat_idx].append(n)

    name_rows_text += "---"
    
  # Add names to bottom of chart
  name_rows_text += "-\n"
  
  for r in range(longest_cat_name_len):
    
    name_rows_text += "    "
    
    for name in name_rows:
      
      if len(name) > r :
        name_rows_text += f" {name[r]} "
      else:
        name_rows_text += f"   "

    # name_rows_text = name_rows_text[0:-1]
    name_rows_text += ' \n'
      
  # Add  all rows to main chart
  for row in rows.values():
    chart += f"{row} \n"

  name_rows_text = name_rows_text[0:-1]
  chart += name_rows_text
  

  return chart
