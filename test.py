import discord
intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)





class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='Click Me!', style=discord.ButtonStyle.primary)
    async def test(self,interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Button clicked!', ephemeral=True)

@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user: # if the message is from the bot then return
        return 

    if message.content == "test":
        await message.channel.send("test", view=Buttons())
key = open("key.txt","r").read()
client.run(key)