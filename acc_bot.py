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
    # i want it to convert to 0:00:00.00 format
    if x == 0:
        return "0:00.00"
    x = datetime.timedelta(seconds=x)
    hours, remainder = divmod(x.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds - int(seconds)) * 100)
    seconds = int(seconds)
    if hours == 0:
        return f"{minutes}:{seconds:02}.{milliseconds:02}"
    return f"{int(hours)}:{int(minutes):02}:{seconds:02}.{milliseconds:02}"

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
                await asyncio.sleep(5)


        
key = open("key.txt","r").read()
client.run(key)
