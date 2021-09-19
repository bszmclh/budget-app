class Category:

    def __init__(self, nam):
        self.name = nam
        self.ledger = []
        self.balance = 0
    
    def __str__(self):
        rtnList = []
        rtnList.append("*" * int((30-len(self.name))/2) + self.name + "*" * (int((30-len(self.name))/2)+ (30-len(self.name))%2))
        for item in self.ledger:
            formatAmount = '{:.2f}'.format(item["amount"])

            spaces = 30 - len(formatAmount) - len(item['description'][0:23])
            rtnList.append(item['description'][0:23] + " " * spaces + formatAmount[0:7])

        rtnList.append('Total: ' + '{:.2f}'.format(self.balance))
        return "\n".join(rtnList)
    
    def deposit(self, amount, desc = ""):
        self.ledger.append({"amount": amount, "description":desc})
        self.balance += amount

    def withdraw(self, amount, desc = ""):
        if self.check_funds(amount):
            self.balance -= amount
            self.ledger.append({"amount": 0-amount, "description": desc})
            return True
        else:
            return False

    def get_balance(self):
        return float('{:.2f}'.format(self.balance))

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.balance -= amount
            self.ledger.append({"amount": 0 - amount, "description": 'Transfer to '+category.name})
            category.deposit(amount, 'Transfer from '+ self.name)
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount > self.balance:
            return False
        else: 
            return True


def create_spend_chart(categories):
    if len(categories) >4: return False

    items=[]
    total = 0
    for item in categories:
        spent = 0
        for i in item.ledger:
            if(i["amount"] < 0): 
                spent += i["amount"]
                total += i["amount"]
            
        items.append({'name': item.name, 'spent': spent})
    
    for item in items:
        item['percent'] = int((item['spent'] / total) * 10) * 10

    result = []
    result.append('Percentage spent by category')
    divider = "    -"
    for i in range(100, -10, -10):
        line = " "*(3-len(str(i))) + str(i) + "| "
        for item in items:
            if item['percent'] >= i:
                line += "o  "
            else:
                line +="   "
        result.append(line)


    maxLen = 0
    
    for item in items:
        if len(item['name']) > maxLen: maxLen = len(item['name'])
        divider += "---"

    result.append(divider)

    for i in range(maxLen):
        line = '     '
        for item in items:
            try:
                line += item['name'][i] + "  "
            except:
                line += "   "
        
        result.append(line)
        

    return "\n".join(result)

