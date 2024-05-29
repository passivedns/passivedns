PARSE_MODE_HTML = "HTML"
PARSE_MODE_MARKDOWN = "Markdown"


class TelegramTemplate(object):
    """
    The Telegram template
    Needs the content and how to parse it (HTML, Markdown)
    """

    def __init__(self, msg, parse_mode):
        self.msg = msg
        self.parse_mode = parse_mode


class EmailTemplate(object):
    """
    The Email template
    Needs the Subject and the content as HTML
    """

    def __init__(self, subject: str, msg: str):
        self.subject = subject
        self.msg = msg


class DiscordTemplate(object):
    """
    The Discord template
    Needs the content as markdown
    """

    def __init__(self, msg: str):
        self.msg = msg


class ChannelTemplate(object):
    """
    The base class for templates
    Can be parsed into channels specific format
    """

    def __init__(self, email, telegram, discord):
        self.email = email
        self.telegram = telegram
        self.discord = discord
        self.formatted_att = {}

    def set_format(self, **formatted_att):
        self.formatted_att = formatted_att

    def get_email_msg(self):
        return self.email.msg.format(**self.formatted_att)

    def get_telegram_msg(self):
        return self.telegram.msg.format(**self.formatted_att)

    def get_discord_msg(self):
        return self.discord.msg.format(**self.formatted_att)
