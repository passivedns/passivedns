PARSE_MODE_HTML = "HTML"
PARSE_MODE_MARKDOWN = "Markdown"



class EmailTemplate(object):
    """
    The Email template
    Needs the Subject and the content as HTML
    """

    def __init__(self, subject: str, msg: str):
        self.subject = subject
        self.msg = msg

class RedisTemplate(object):
    """
    The Redis template
    Needs the content as markdown
    """

    def __init__(self, msg: str):
        self.msg = msg


class ChannelTemplate(object):
    """
    The base class for templates
    Can be parsed into channels specific format
    """

    def __init__(self, email, redis):
        self.email = email
        self.redis_channel = redis
        self.formatted_att = {}

    def set_format(self, **formatted_att):
        self.formatted_att = formatted_att

    def get_email_msg(self):
        return self.email.msg.format(**self.formatted_att)

    def get_redis_msg(self):
        return self.redis_channel.msg
