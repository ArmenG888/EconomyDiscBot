import discord,sqlite3,datetime,random,time
from discord.ui import Button

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
    
m = main()

class Buttons(discord.ui.View):
    def __init__(self, inv:str):
        super().__init__()
        self.inv = inv
        self.add_item(discord.ui.Button(label="Click Me!", style=discord.ButtonStyle.primary, custom_id="test"))

    @discord.ui.button(label='Click Me!', style=discord.ButtonStyle.primary, custom_id="test")
    async def test(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message('Button clicked!', ephemeral=True)


def send_embed(title, description, color=0x00FF00):
    embed = discord.Embed(title=title, description=description)
    embed.color = color
    return embed

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
    await message.channel.send(embed=send_embed("Balance", f"> {name} has :coin: {money}", 0x0000FF))
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
                num = random.randint(int(args[1]))
    else:
        num = random.randint(0,100)
    
    await message.channel.send(embed=send_embed("Random", f"> {num}", 0x0000FF))
help_text = """
> - ``!bal <user (optional)>`` - Check your balance or someone else's
> - ``!work`` - Work and earn money
> - ``!rob <user>`` - Rob someone and earn money (or lose money)
> - ``!time <hour>:<minute> (optional) <format> (optional)`` - Get the time in a timezone
> EX: !time 12:00PM short
> EX: !time
> - ``!crime`` - Do a crime and earn money (or lose money)


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
]

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
    if message.author == client.user: # if the message is from the bot then return
        return 
   
    xp = m.add_message(m.get_user(message.author.name), message.content)# adds message to the db
    for i in levels:
        if xp > int(levels[i]):
            role = i
    await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=role))
    
    name = lambda: message.author.name if len(message.content.split(" ")) <= 1 else message.content.split(" ")[1] # if argument in the message then use that as the name else use the author's name
    id = m.get_user(name()) 
    if not message.content.startswith("!"):
        return

    
    admin = True if message.author.name in admins else False # check if author admin

    command = message.content.split(" ")[0]
    if command in commands:
        await commands[command](message, id, name(), admin)
    else:
        await message.channel.send(embed=send_embed("Error", "Invalid Command use ``!help`` for help"))
     
key = open("key.txt","r").read()
client.run(key)