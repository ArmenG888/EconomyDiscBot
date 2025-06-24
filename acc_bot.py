from pyaccsharedmemory import accSharedMemory
import discord
import time
import asyncio
import datetime

intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)


asm = accSharedMemory()
print(asm.read_shared_memory())

def convert_time(x):
    seconds=(x/1000)%60
    seconds = int(seconds)
    minutes=(x/(1000*60))%60
    minutes = int(minutes)
    hours=(x/(1000*60*60))%24
    if int(hours) == 0:
        d = datetime.time(int(hours), int(minutes), int(seconds)).strftime("%M:%S")
    else:
        d = datetime.time(int(hours), int(minutes), int(seconds)).strftime("%H:%M.%S")
    return d

@client.event
async def on_message(message):
    if message.author == client.user:
        return 
    if message.content.startswith("!start"):
        
        msg = await message.channel.send(f"Starting")
        while True:
            sm = asm.read_shared_memory()
            try:
                info = f"""```
    {sm.Graphics.session_type} | Time Left: {convert_time(sm.Graphics.session_time_left)} | Track: {convert_time(sm.Graphics.clock)}
    Lap: {convert_time(sm.Graphics.current_time)} | Best: {convert_time(sm.Graphics.best_time) if sm.Graphics.completed_lap != 0 else "0:00.00"} | Last: {convert_time(sm.Graphics.last_time) if sm.Graphics.completed_lap != 0 else "0:00.00"}
    Pos: {sm.Graphics.position}/{sm.Graphics.active_cars} | Lap: {sm.Graphics.completed_lap} | Dist: {round(sm.Graphics.distance_traveled, 3)} m
    Fuel: {round(sm.Physics.fuel,1)} L | Est: {round(sm.Graphics.fuel_estimated_laps,1)} laps | /Lap: {round(sm.Graphics.fuel_per_lap,2)} L
    Pressures: FL:{sm.Physics.wheel_pressure.front_left:.2f} psi FR:{sm.Physics.wheel_pressure.front_right:.2f} psi RL:{sm.Physics.wheel_pressure.rear_left:.2f} psi RR:{sm.Physics.wheel_pressure.rear_right:.2f} psi
    Temps: FL:{sm.Physics.tyre_core_temp.front_left:.1f}°C FR:{sm.Physics.tyre_core_temp.front_right:.1f}°C RL:{sm.Physics.tyre_core_temp.rear_left:.1f}°C RR:{sm.Physics.tyre_core_temp.rear_right:.1f}°C
```"""
                await msg.edit(content=info)
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Error: {e}")
                await message.channel.send(f"ACC session ended")
                break

        
key = open("key.txt","r").read()
client.run(key)
