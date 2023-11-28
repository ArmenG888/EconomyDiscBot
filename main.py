import re
import discord,sqlite3,datetime,random,time,math

import sympy as sp
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)



class main:
    def __init__(self):
        self.con = sqlite3.connect("db.sqlite3")
        self.cur = self.con.cursor()
    def get_user(self, name):
        self.cur.execute("SELECT id FROM main_user WHERE name = ?", (name,))
        id = self.cur.fetchone()
        if id is None:
            self.cur.execute("INSERT INTO main_user (name, money) VALUES (?, ?)", (name, 0.00))
            self.con.commit()
            self.cur.execute("SELECT id FROM main_user WHERE name = ?", (name,))
            id = self.cur.fetchone()
        return id[0]
    def get_money(self, id):
        self.cur.execute("SELECT money FROM main_user WHERE id = ?", (id,))
        money = self.cur.fetchone()[0]
        return money
    def set_money(self, id, money):
        self.cur.execute("UPDATE main_user SET money = ? WHERE id = ?", (money, id))
        self.con.commit()
        return money
    def add_money(self, id, money):
        user_money = int(self.get_money(id))
        new_balance = user_money + int(money)
        self.cur.execute("UPDATE main_user SET money = ? WHERE id = ?", (new_balance, id))
        self.con.commit()
        return new_balance
    def get_xp(self, id):
        self.cur.execute("SELECT xp FROM main_user WHERE id = ?", (id,))
        xp = self.cur.fetchone()[0]
        return xp
    def add_message(self, id, message):
        self.cur.execute("INSERT INTO main_message (user_id, message,date) VALUES (?, ?, ?)", (id, message,datetime.datetime.now()))
        xp = self.get_xp(id)
        if xp != None:
            xp += 1
        else:
            xp = 1
        self.cur.execute("UPDATE main_user SET xp = ? WHERE id = ?", (xp, id))
        self.con.commit()
        return xp
    def get_stock_by_name(self, stock):
        self.cur.execute("SELECT id FROM main_stock WHERE name = ?", (stock,))
        id = self.cur.fetchone()
        if id is None:
            self.cur.execute("INSERT INTO main_stock (name, price) VALUES (?, ?)", (stock, 0.00))
            self.con.commit()
            self.cur.execute("SELECT id FROM main_stock WHERE name = ?", (stock,))
            id = self.cur.fetchone()
            print(id)
        return id[0]

    def get_stock_by_id(self, id):
        self.cur.execute("SELECT name FROM main_stock WHERE id = ?", (id,))
        name = self.cur.fetchone()[0]
        return name
    def get_stock_price(self, id):
        self.cur.execute("SELECT price FROM main_stock WHERE id = ?", (id,))
        price = self.cur.fetchone()[0]
        return price
    def get_user_stock(self,user_id,stock_id):
        self.cur.execute("SELECT amount FROM main_user_stocks WHERE user_id = ? AND stock_id = ?", (user_id,stock_id))
        amount = self.cur.fetchone()
        if amount is None:
            self.cur.execute("INSERT INTO main_user_stocks (user_id, stock_id, amount) VALUES (?, ?, ?)", (user_id,stock_id,0))
            self.con.commit()
            self.cur.execute("SELECT amount FROM main_user_stocks WHERE user_id = ? AND stock_id = ?", (user_id,stock_id))
            amount = self.cur.fetchone()
        return amount[0]
    def set_user_stock(self,user_id,stock_id,amount):
        self.cur.execute("UPDATE main_user_stocks SET amount = ? WHERE user_id = ? AND stock_id = ?", (amount,user_id,stock_id))
        self.con.commit()
        return amount
    def add_user_stock(self,user_id,stock_id,amount):
        user_stock = int(self.get_user_stock(user_id,stock_id))
        new_amount = user_stock + int(amount)
        self.cur.execute("UPDATE main_user_stocks SET amount = ? WHERE user_id = ? AND stock_id = ?", (new_amount,user_id,stock_id))
        self.con.commit()
        return new_amount
    
    def set_stock_price(self,id,price):
        self.cur.execute("UPDATE main_stock SET price = ? WHERE id = ?", (price,id))
        self.con.commit()
        


m = main()
class Buttons(discord.ui.View):
    def __init__(self,i):
        super().__init__()
        print(i)
    @discord.ui.button(label='Get a lawyer ($100)', style=discord.ButtonStyle.primary)
    async def test(self,interaction: discord.Interaction, button: discord.ui.Button):
        random_number = random.randint(0,1)
        if random_number == 0:
            await interaction.response.send_message('You got a lawyer and won the case!', ephemeral=True)
        else:
            await interaction.response.send_message('You got a lawyer and lost the case!', ephemeral=True)
        #await interaction.response.send_message('Button clicked!', ephemeral=True)
    
    @discord.ui.button(label='Free lawyer', style=discord.ButtonStyle.primary)
    async def test(self,interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Button clicked!', ephemeral=True)

def send_embed(title, description, color=0x00FF00):
    embed = discord.Embed(title=title, description=description)
    embed.color = color
    return embed

async def test(message, id, name, *args):
    await message.channel.send("test", view=Buttons(100))
async def set_money(message, id, name, *args):
    if args[0] == True:
        money = m.set_money(id, message.content.split(" ")[2])
        await message.channel.send(embed=send_embed("Money Set", f"> {name} now has :coin: {money}"))

async def add_money(message, id, name, *args):
    if args[0] == True:
        money = m.add_money(id, message.content.split(" ")[2])
        await message.channel.send(embed=send_embed("Money Added", f"> {name} now has :coin: {money}"))

async def bal(message, id, name, *args):
    money = m.get_money(id)
    mesg = f"> :coin: {money} ``Balance``\n\n**Stocks**\n"
    
    user_stocks = {}
    for i in stocks:
        stock_id = m.get_stock_by_name(i)
        amount = m.get_user_stock(id, stock_id)
        mesg += f"> :coin: {amount} ``{i.capitalize()}``\n"
        user_stocks[i] = amount


    await message.channel.send(embed=send_embed(f"Balance {name}", mesg, 0x0000FF))

async def steam_market_fee(message, id, name, *args):
    price = float(message.content.split(" ")[1])
    if price > 0.10:
        price *= 1.15
    else:
        price += 0.02

    await message.channel.send(embed=send_embed(f"Steam", f"Price after fee: {price}", 0x0000FF))
    
def evaluate_equation(eq, x_values):
    x = sp.symbols('x')
    expression = sp.sympify(eq)
    y_values = []
    for value in x_values:
        y_val = expression.subs(x, value)
        # Use real part if complex, otherwise use the value directly
        y_values.append(float(y_val.as_real_imag()[0]))
    return y_values

colors = [
    'red',
    'blue',
    'green',
    'yellow',
    'black',
    'white',
    'orange',
    'purple',
    'brown',
    'pink',
]
async def graph(message, id, name, *args):
    equation = message.content.replace("!graph ","").replace("y=","").replace("^","**").split(" ")[0]
    color = "blue"
    if message.content.replace("!graph ","").split(" ")[1] in colors:
        color = message.content.replace("!graph ","").split(" ")[1]
    equation = re.sub(r'([0-9])([a-zA-Z])', r'\1*\2', equation)
    rangex = 3
    x_values = np.linspace(-rangex, rangex, 400)  # Adjust the range and number of points as needed

    # Evaluate the equation
    try:
        y_values = evaluate_equation(equation, x_values)

        # Create a plot
        plt.figure(figsize=(8, 6))
        plt.plot(x_values, y_values, label=f'y = {message.content.replace("!graph ","").replace("y=","").split(" ")[0]}',color=color)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Graph of y = {message.content.replace("!graph ","").replace("y=","").split(" ")[0]}')
        plt.grid(True)
        
        x_integers = np.arange(-rangex, rangex+1)
        y_integers = [evaluate_equation(equation, [x])[0] for x in x_integers]
        plt.scatter(x_integers, y_integers, color='red', marker='o', label='Integer Points')
        plt.axhline(0, color='black',linewidth=0.5)  # Add a horizontal axis line
        plt.axvline(0, color='black',linewidth=0.5)
        #plt.xticks(np.arange(-4,5, 1))  # Adjust the range and interval as needed for the x-axis
        #plt.axis('equal')
        plt.legend()

        # Save the plot as an image
        plt.savefig('equation_graph.png', dpi=300)
            
        # Send the image to the Discord channel
        with open('equation_graph.png', 'rb') as file:
            await message.channel.send(f'Graph of y = {message.content.replace("!graph ","").replace("y=","")}', file=discord.File(file))
    except Exception as e:
        print(e)
        
async def graph_ascii(message, id, name, *args):
    
    size = 20
    lst = np.zeros((size-1, size-1))


    f_of_x = {}
    for i in range(-9,9):
        try:
            eq = message.content.replace("!graph_old ","").replace("!math quad ","").replace("^","**").replace("x",f"*({str(i)})")
            if eq[0] == "*":
                eq = eq[1:]
            print(eq)
            f_of_x[i] = eval(eq)
        except Exception as e:
            print(e)
    print(f_of_x)

    for i in f_of_x:
        try:
            x_index = i + 9 
            y_index = int(f_of_x[i]) + 9
            if 0 <= x_index < size and 0 <= y_index < size:
                lst[y_index, x_index] = 1
        except:
            continue
    output = ""
    x = 0
    output += "           Y\n"
    for indx,i in enumerate(lst[::-1]):
        if 9-indx >= 0:
            output += f" {9-indx}"
        else:
            output += f"{9-indx}"
        
        for ii in i:
            if ii == 0:
                if x == 9:
                    output += "|"
                        
                else:
                    output += " "
                
            else:
                output += "█"
            x += 1
        if 9-indx == 0:
            output += "\n X <---------------> X"
        output += "\n"
        x = 0
    output += "           Y\n"
    await message.channel.send(embed=send_embed(f"Graph for f(x)={message.content.replace('!graph ','')}", f"```\n{output}```", 0x0000FF))
async def math_equation(message, id, name, *args):
    eq = message.content.split(" ")[1]
    split_values = re.split(r'(?<=[+\-*/^])|(?=[+\-*/^])', eq)
    split_values = [value for value in split_values if value is not None and value != '']

    def drg(func,trig):
        inside = func.replace(f"{trig}(","").replace(")","")
        if "deg" in inside:
            inside = inside.replace("deg","")
            inside = math.radians(float(inside))
        else:
            inside = float(inside)
        return inside
    total = 0
    operator = "+"
    for equation in split_values:
        if equation in ['+','-','*','/','^']:
            operator = equation
            continue
        if "log" in equation:
            log = equation.split(")")[0]
            base = float(log.replace("log","").split("(")[0])
            inside = float(log.split("(")[1].replace(")",""))
            answer = math.log(inside)/math.log(base)
        elif "sqrt" in equation:
            inside = float(equation.replace("sqrt(","").replace(")",""))
            answer = math.sqrt(inside)
        elif "quad" in equation:
            quad = message.content.split(" ")[2]
            print(quad)
            pattern = r'([-+]?[\d.]*x\^2)?\s*([-+]?[\d.]*x)?\s*([-+]?\d+)?'
            match = re.match(pattern, quad)
            if match:
                a = float(match.group(1).replace('x^2', '').strip()) if match.group(1) else 1.0
                b = float(match.group(2).replace('x', '').strip()) if match.group(2) else 0.0
                c = float(match.group(3)) if match.group(3) else 0.0

                discriminant = b**2 - 4*a*c

                if discriminant >= 0:
                    root1 = (-b + math.sqrt(discriminant)) / (2*a)
                    root2 = (-b - math.sqrt(discriminant)) / (2*a)
                    total = f"""
                    ## Solution

                    **x-intercepts**
                    ``({round(root1,2)},0.0)``,
                    ``({round(root2,2)},0.0)``

                    **y-intercept**
                    ``({0},{c})``
                    """
                    
                else:
                    total = "The quadratic equation has no real roots."
                
            else:
                total = "Invalid quadratic expression format."
            await message.channel.send(embed=send_embed(f"# Math", f"{total}", 0x0000FF))
            if "Invalid" not in total:
                await graph_ascii(message, id, name)
            return
        elif "atan" in equation:
            answer = math.atan(drg(equation.split(")")[0],"atan"))
        elif "cot" in equation:
            answer = 1/math.tan(drg(equation.split(")")[0],"cot"))
        elif "sec" in equation:
            answer = 1/math.cos(drg(equation.split(")")[0],"sec"))
        elif "csc" in equation:
            answer = 1/math.sin(drg(equation.split(")")[0],"csc"))
        elif "ln" in equation:
            answer = math.log(drg(equation.split(")")[0],"ln"))
        elif "sin" in equation:
            answer = math.sin(drg(equation.split(")")[0],"sin"))
        elif "cos" in equation:
            answer = math.cos(drg(equation.split(")")[0],"cos"))
        elif "tan" in equation:
            answer = math.tan(drg(equation.split(")")[0],"tan"))
        elif "asin" in equation:
            answer = math.asin(drg(equation.split(")")[0],"asin"))
        elif "acos" in equation:
            answer = math.acos(drg(equation.split(")")[0],"acos"))
        elif "e" in equation:
            try:
                answer = math.e * float(equation.split("e")[0])
            except:
                answer = math.e
        elif "pi" in equation:
            try:
                answer = math.pi * float(equation.split("pi")[0])
            except:
                answer = math.pi

        else:   
            answer = eval(equation)
            print(answer)
        if operator == "+":
            total += answer
        elif operator == "-":
            total -= answer
        elif operator == "*":
            total *= answer
        elif operator == "/":
            total /= answer
        elif operator == "^":
            total **= answer
        else:
            total = answer
        
    if type(total) == float:
        answer = round(total,2)
    await message.channel.send(embed=send_embed(f"Math", f"{total}", 0x0000FF))
    


async def help(message, *args):
    await message.channel.send(embed=send_embed("Help", help_text, 0x0000FF))
    
async def work(message, id, name, *args):
    job = jobs[random.randint(0,len(jobs)-1)]
    money = random.randint(1,100)
    m.add_money(id, money)
    await message.channel.send(embed=send_embed("Work", f"> You worked as an {job} and made :coin: {money}"))   

async def rob(message, id, name, *args):
    if name == message.author.name:
        await message.channel.send(embed=send_embed("Rob", "> You cannot rob yourself", 0xFF0000))
        return
    if m.get_money(m.get_user(name)) < 0:
        await message.channel.send(embed=send_embed("Rob", f"> {name} does not have enough money to rob", 0xFF0000))
        return
    person_robbed_id = m.get_user(name) # gets user id by name
    amount = random.randint(-m.get_money(person_robbed_id), person_robbed_id) 
    m.add_money(id, amount) # adds money with args id,money
    m.add_money(person_robbed_id, -amount) # adds money with args id, money
    if amount < 0:
        await message.channel.send(embed=send_embed("Rob", (f"> {message.author.name} tried to rob {name} but got caught -:coin: {abs(amount)}", 0xFF0000)))
    else:
        await message.channel.send(embed=send_embed("Rob", f"> {message.author.name} has robbed {name} and earned :coin: 10"))
    return

async def crime(message, id, name, *args):
    crime_mes = crimes[random.randint(0,len(jobs)-1)]
    money = random.randint(-200,200)
    m.add_money(id, money)
    if money < 0:
        await message.channel.send(embed=send_embed("Crime", f"> You {crime_mes} and got caught -:coin: {abs(money)}", 0xFF0000))
    else:
        await message.channel.send(embed=send_embed("Crime", f"> You {crime_mes} and earned :coin: {money}"))

stocks = {
    'apple': 'AAPL',
    'microsoft': 'MSFT',
    'google': 'GOOG',
    'amazon': 'AMZN',
}



time_formats = {
    'relative': 'r',
    'short': 't',
    'long': 'f',
}

async def time_with_timezone(message,id,name, *args):
    def time_format(format_argument):
        if format_argument not in time_formats:
            format = format_argument
        else:
            format = time_formats[format_argument]
        if format == "":
            format = "F"
        return format
    date_time = datetime.datetime.now()
    arguments = message.content.split(" ")
    mes = message.content.replace("!time ","")
    format = "F"
    if len(arguments) > 2:
        format = time_format(mes.split(":")[1].split(" ")[1].lower())
        
    if len(arguments) > 1:
        
        try:
            hour = int(mes.split(":")[0])
            if "PM" in name or "pm" in name:
                hour = int(mes.split(":")[0])+12
            mes = mes.replace("pm", "").replace("PM", "").replace("am", "").replace("AM", "")
            date_time = date_time.replace(hour=hour, minute=int(mes.split(":")[1].split(" ")[0]))
        except:
            format = time_format(mes)

    target_unix_timestamp = time.mktime(date_time.timetuple())
    await message.channel.send(embed=send_embed("Time", f"> <t:{int(target_unix_timestamp)}:{format}>", 0x0000FF))

async def random_number(message, id, name, *args):
    args = message.content.split(" ")
    if len(args) > 1:
        if args[1] == "yn":
            num = random.randint(0,1)
            if num == 0:
                num = "No"
            else:
                num = "Yes"
        else:
            nums = args[1].split(",")
            if len(nums) > 1:
                num = random.randint(int(nums[0]),int(nums[1]))
            else:
                num = random.randint(0,int(args[1]))
    else:
        num = random.randint(0,100)
    
    await message.channel.send(embed=send_embed("Random", f"> {num}", 0x0000FF))


async def stock_market(message, id, name, *args):
    mes = ""
    for stock in stocks:
        stockX = yf.Ticker(stocks[stock])
        dataX = stockX.history(period='1d')
        price = round(dataX['Open'].tail(1).iloc[0],2)
        print(stock)
        id = m.get_stock_by_name(stock)
        m.set_stock_price(id, price)
        mes += f"> :coin: {round(price,2)} ``{stock.capitalize()}``\n" 
        
    await message.channel.send(embed=send_embed("Stocks", mes, 0x0000FF))


async def buy_stock(message, id, name, *args):
    mes = message.content.replace("!buy ", "")
    stock = mes.split(" ")[0]
    amount = mes.split(" ")[1]
    stock_id = m.get_stock_by_name(stock)
    price = m.get_stock_price(int(stock_id))
    total_price = price * int(amount)
    user_money = int(m.get_money(id))
    if user_money < total_price:
        await message.channel.send(embed=send_embed("Stocks", f"> You do not have enough money to buy {amount} {stock.capitalize()} stocks", 0xFF0000))
        return
    m.add_money(id, -total_price)
    m.add_user_stock(id, stock_id, amount)
    await message.channel.send(embed=send_embed("Stocks", f"> You bought {amount} {stock.capitalize()} stocks for :coin: {total_price}", 0x0000FF))
    return
async def sell_stock(message, id, name, *args):
    mes = message.content.replace("!sell ", "")
    stock = mes.split(" ")[0]
    amount = mes.split(" ")[1]
    stock_id = m.get_stock_by_name(stock)
    price = m.get_stock_price(int(stock_id))
    total_price = price * int(amount)
    user_stock = m.get_user_stock(id, stock_id)
    if int(user_stock) <= int(amount):
        await message.channel.send(embed=send_embed("Stocks", f"> You do not have enough {stock.capitalize()} stocks to sell", 0xFF0000))
        return
    m.add_money(id, total_price)
    m.add_user_stock(id, stock_id, -int(amount))
    await message.channel.send(embed=send_embed("Stocks", f"> You sold {amount} {stock.capitalize()} stocks for :coin: {total_price}", 0x0000FF))



help_text = """
> - ``!bal <user (optional)>`` - Check your balance or someone else's
> - ``!work`` - Work and earn money
> - ``!rob <user>`` - Rob someone and earn money (or lose money)
> - ``!time <hour>:<minute> (optional) <format> (optional)`` - Get the time in a timezone
> - Time formats: ``relative``, ``short``, ``long`` or ``f`` for full, ``r`` for relative, ``t`` for short
> - EX: !time 12:00PM short, P!time short, !time 12:00PM, !time 12:00PM r
> - ``!crime`` - Do a crime and earn money (or lose money)
> - ``!random <min>,<max>`` - Get a random number between min and max if no arguments then get a random number between 0 and 100
> - ``!random <max>`` - Get a random number between 0 and max
> - ``!random yn`` - Get a random yes or no
> - ``!stocks`` - Get the current stock prices
> - ``!buy <stock> <amount>`` - Buy a stock
> - ``!sell <stock> <amount>`` - Sell a stock
> - ``!steam_fee <price>`` - Get the price after steam market fee
> - ``!math <equation>`` - Solve a math equation
> - ``!graph <equation>`` - Graph a math equation
"""
jobs = [
    'Programmer',
    'Teacher',
    'Doctor',
    'Lawyer',
    'Police Officer',
    'Firefighter',
    'Chef',
    'Mechanic',
    'Cashier',
    'Waiter',
    'Janitor',
    'Construction Worker',
    'Electrician',
    'Plumber',
    'Nurse',
    'Dentist',
    'Veterinarian',
    'Pharmacist',
    'Psychologist',
    ':flag_at:Artist',
]
crimes = [
    'Robbed a bank',
    'Stole a car',
    'Stole a bike',
    'Stole a wallet',
    'Nuked the toilet',
    'Sold drugs',
    'Sold a gun',
    'Sold a stolen item',
    'did Prostitution',
    'did human trafficking',
    'did money laundering',
    'did tax evasion',
    'did fraud',
    'did embezzlement',
    'did insider trading',
    'did extortion',
    'did blackmail',
    'did bribery',
    'did forgery',
    'did arson',
    'did vandalism',
    'did kidnapping',
]
admins = [
    '.armeng'
] # list of admins

commands = {
    '!set_money':set_money,
    '!add_money':add_money,
    '!bal':bal,
    '!help':help,
    '!work':work,
    '!rob':rob,
    '!crime':crime,
    '!time':time_with_timezone,
    '!random':random_number,
    '!stocks':stock_market,
    '!steam_fee':steam_market_fee,
    '!math':math_equation,
    '!buy':buy_stock,
    '!sell':sell_stock,
    '!graph':graph,
    '!graph_old':graph_ascii,
    '!test':test,
}

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


levels = {
    'Level 1': '0',
    'Level 2': '30',
    'Level 3': '60',
    'Level 4': '120',
    'Level 5': '200',
    'Level 6': '300',
    'Level 7': '400',
    'Level 8': '600',
    'Level 9': '850',
    'Level 10': '1001',
}

@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user: # if the message is from the bot then return
        return 

    if "danny" in message.content.lower():
         await message.channel.send("Fatass :japanese_goblin: ")


    xp = m.add_message(m.get_user(message.author.name), message.content)# adds message to the db
    for i in levels:
        if xp > int(levels[i]):
            role = i
    await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=role))
    
    name = lambda: message.author.name
    id = m.get_user(name()) 
    if not message.content.startswith("!"):
        return

    
    admin = True if message.author.name in admins else False # check if author admin

    command = message.content.split(" ")[0]
    if command in commands:
        try:
            await commands[command](message, id, name(), admin)
        except Exception as e:
            print(e)
            await message.channel.send(embed=send_embed("Error", "Invalid Command usage, ``!help`` for help"))
    else:
        await message.channel.send(embed=send_embed("Error", "Invalid Command use ``!help`` for help"))
     
key = open("key.txt","r").read()
client.run(key)