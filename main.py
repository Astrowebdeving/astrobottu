import asyncio
import discord
from discord.ext import commands
from discord import guild
import json
import os
from dotenv import load_dotenv
import requests
from time import sleep
from discord import Client
from discord.ui import view
intents = discord.Intents.default()
intents.message_content = True
load_dotenv()
bot = commands.Bot(command_prefix="a!", intents=intents)
#client = Client(intents=intents)
users = []
def get_question():
    qs = ''
    id = 1
    response = requests.get("https://mysterious-headland-81216.herokuapp.com/api/random/")
    json_data = json.loads(response.text)
    qs += "Question: \n"
    qs+=json_data[0]['title']+"\n"
    qt = json_data[0]['title']
    for item in json_data[0]['answer']: #loop through the answer section, below is fields"
        qs += str(id)+". "+item['answer']+'\n'
        if item['is_correct']:
            answerval = item['answer']
            answer = id
        id+=1
    return(qs,answer, answerval, qt)


#@bot.command()
#async def test(ctx, arg):
#    if not type(arg) is str:
#        await ctx.send("invalid input")
#    await ctx.send(arg)

#@client.event
#async def question(ctx):
#    q, a = get_question()
#    await ctx.send(q)
@bot.command()
async def info(ctx):
    print(ctx.guild.id)
    await ctx.send("ID: {}".format(ctx.guild.id))

@bot.command()
async def quest(ctx):
    if ctx.guild.id != (768486039328391199 or 1132535095480287254):
         return 
    serverId = ctx.guild.id
    global q
    global a
    global av
    global qt
    q, a, av, qt = get_question()
    #view = ButtonView()
    #await view.wait()
    #view.add_item(discord.ui.Button(label="URL Button",style=discord.ButtonStyle.link,url="https://github.com/lykn"))
    await ctx.send(q, view=ButtonView())
    await asyncio.sleep(10)
    global users
    await ctx.send(f"The users: {users} are correct! The answer to {qt} is {av}!", ephemeral=False)
    
    users = []

        #def check(m):
        #        return m.author == message.author and m.content.isdigit()
                
        #try: 
        #    guessmsg = await client.wait_for('message', check=check, timeout = 8.0)
        #except asyncio.TimeoutError:
        #    return await message.channel.send('Sorry, you took to long')
        
        #if int(guessmsg.content) == a:
        #    await message.channel.send("You are correct!")
        #else:
        #    await message.channel.send("Incorrect!")
def textCheck(val, a, q):
        truth = False
        if val == str(a):
            truth = True
            return truth, f"You are correct, {q} is the correct answer."
        else:
            return truth, "You are incorrect."
def textsend(b):
        return b
class ButtonView(discord.ui.View):
    val = ""
    def __init__(self, *, timeout=10):
        super().__init__(timeout=timeout)
        self.clicked_users = []

    @discord.ui.button(label="1",row = 0, style=discord.ButtonStyle.blurple) # or .primary
    async def blurple_button(self, interaction: discord.Interaction, button: discord.ui.button):   
        global q
        global a
        global av
        global qt
        await asyncio.sleep(0.1)
        val = "1"
        user_id = interaction.user.id
        await asyncio.sleep(0.1)
        if user_id in self.clicked_users:
            # user has already pressed the button
            await interaction.response.send_message(content=f"You have already answered.", ephemeral=True)
            return
        self.clicked_users.append(user_id)
        button.disabled=True
        correctness, text = textCheck(val, a, av)
        if correctness:
             global users
             if (interaction.user.name in users)==False:
                  users.append(interaction.user.name)
        await interaction.response.send_message(textsend(text), ephemeral=True)
    @discord.ui.button(label="2",row = 0, style=discord.ButtonStyle.gray) # or .secondary/.grey
    async def gray_button(self, interaction: discord.Interaction, button: discord.ui.button):   
        global q
        global a
        global av
        global qt
        val = "2"
        user_id = interaction.user.id
        if user_id in self.clicked_users:
            # user has already pressed the button
            await interaction.response.send_message(content=f"You have already answered.", ephemeral=True)
            return
        self.clicked_users.append(user_id)
        button.disabled=True
        correctness, text = textCheck(val, a, av)
        if correctness:
            global users
            if (interaction.user.name in users)==False:
                users.append(interaction.user.name)
        await interaction.response.send_message(textsend(text), ephemeral=True)
    @discord.ui.button(label="3",row = 1, style=discord.ButtonStyle.green) # or .success
    async def green_button(self, interaction: discord.Interaction, button: discord.ui.button):   
        global q
        global a
        global av
        global qt
        val = "3"
        user_id = interaction.user.id
        if user_id in self.clicked_users:
            # user has already pressed the button
            await interaction.response.send_message(content=f"You have already answered.", ephemeral=True)
            return
        self.clicked_users.append(user_id)
        button.disabled=True
        correctness, text = textCheck(val, a, av)
        if correctness:
             global users
             if (interaction.user.name in users)==False:
                  users.append(interaction.user.name)
        await interaction.response.send_message(textsend(text),ephemeral=True)
    @discord.ui.button(label="4",row = 1, style=discord.ButtonStyle.red) # or .danger
    async def red_button(self, interaction: discord.Interaction, button: discord.ui.button):   
        global q
        global a
        global av
        global qt
        val = "4"
        user_id = interaction.user.id
        if user_id in self.clicked_users:
            # user has already pressed the button
            await interaction.response.send_message(content=f"You have already answered.", ephemeral=True)
            return
        self.clicked_users.append(user_id)
        button.disabled=True
        correctness, text = textCheck(val, a, av)
        if correctness:
             global users
             if (interaction.user.name in users)==False:
                  users.append(interaction.user.name)
        await interaction.response.send_message(textsend(text),ephemeral=True)
token = os.getenv('envtoken')
bot.run("MTEzMjUzNTU5MDcyMjc0NDQ1MA.GqS_Fl.3bCJqnrnKljU-wwZbSu0uxkSNQ9Y4VjfBOupGA")
