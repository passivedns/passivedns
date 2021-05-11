import discord
from multiprocessing import Process

from channels.templates import ChannelTemplate
from models.channel_meta import ChannelDiscord


class DiscordSendingError(Exception):
    pass


def send_discord_process(user_id_str: str, channel_discord: ChannelDiscord, template: ChannelTemplate):
    """
    Send a message to a user through Discord API
    :param user_id_str: the User to contact
    :param channel_discord: the bot token
    :param template: the message to send
    :return:
    :raise: DiscordSendingError if message not sent
    """
    try:
        user_id = int(user_id_str)

        intents = discord.Intents.default()
        intents.members = True
        client = discord.Client(intents=intents)

        @client.event
        async def on_ready():
            user = client.get_user(user_id)
            await user.create_dm()
            await user.dm_channel.send(template.get_discord_msg())

            await client.close()

        client.run(channel_discord.bot_token)

    except Exception as e:
        raise DiscordSendingError(e)


def send_discord(user_id_str: str, channel_discord: ChannelDiscord, template: ChannelTemplate):
    """
    Discord client only work in a main thread because of the usage of asyncio
    That's why we create a new Process in order to create the client, so it can
    operate in a context of a main thread

    :param user_id_str: the user id as string
    :param channel_discord: the discord parameters
    :param template: template to send
    :return: None
    """
    p = Process(target=send_discord_process, args=(user_id_str, channel_discord, template))
    p.start()
    p.join()
