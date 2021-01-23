import discord
import random

client = discord.Client()
commands = {}
random_commands = {}
file = open('commands.txt', 'w')


async def send_message(c, message):
    await c.channel.send(message)


def add_command(command_dict, trigger, message):
    try:
        new_command = message
        command = new_command[len(trigger) + 1:]
        command = command.split(';')
        key, value = command
        command_dict[key] = value
    except:
        return -1


def add_random_command(key, values):
    random_commands[key] = values


def check_commands(message):
    for key, value in commands.items():
        if key in message:
            return value

    for key, values in random_commands.items():
        if key in message:
            return random.choice(values[2:len(values) - 1].split(','))
    return False


def remove_command(command):
    for key, value in commands.items():
        if key == command:
            del commands[key]
            break

    for key, value in random_commands.items():
        if key == command:
            del random_commands[key]
            break


def get_commands():
    with open('commands.txt', 'r') as file:
        command = file.readlines()
        for line in command:
            line = line.strip().split()
            if line[0] == 'rand':
                random_commands[line[1]] = line[2]
            elif line[0] == 'cmd':
                commands[line[1]] = line[2]


get_commands()

def handle_commands():
    with open('commands.txt', 'a'):
        for key, value in commands.items():
            file.write(f'cmd {key} {value}\n')

        for key, value in random_commands.items():
            file.write(f'rand {key} {value}\n')


@client.event
async def on_member_join(member):
    for channel in meber.guild.channels:
        if str(channel) == 'welcome':
            await channel.send_message(f'Welcome to the server {member.mention}')


@client.event
async def on_ready():
    print("Logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    server_id = client.get_guild(799035458449309746)
    print(client.user)
    if message.author == client.user:
        return

    if message.author == "destinie#7704" or message.author == "FishieFish#3010":
        await send_message(message, "Invalid User")
        return

    if message.content.startswith('bot.remove:'):
        c = message.content[11:]
        remove_command(c)
        return

    if message.content == "bot.users":
        await send_message(message, f"""# of members {server_id.member_count}""")

    if check_commands(message.content):
        await send_message(message, check_commands(message.content))

    if message.content.find("bot.add_command:") != -1:
        try:
            trigger = "bot.add_command:"
            add_command(commands, trigger, message.content)

            await send_message(message, "Command Added!")
        except:
            await send_message(message, 'Please try again, bot.help for commands')
        return

    if message.content.startswith('bot.add_random_command:'):
        try:
            trigger = "bot.add_random_command:"
            add_command(random_commands, trigger, message.content)

            await send_message(message, 'Random Command Added!')
        except:
            await send_message(message, 'Please try again, use bot.help for commands')
        return

    if message.content.startswith('bot.save_commands'):
        handle_commands()
        await send_message(message, "All Commands Saved!")
        return

    if message.content.startswith('bot.clear_commands'):
        file = open('commands.txt', 'w')
        file.truncate()
        file.close()
        await send_message(message, "All Commands Cleared!")
client.run('Nzk5NjczODI1NjM2OTA5MTI3.YAHASQ.bRQ25rQLbE6jnqIuWiiuIcTHgzk')
