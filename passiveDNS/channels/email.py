import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from passiveDNS.channels.templates import ChannelTemplate
from passiveDNS.models.channel_meta import ChannelEmail


class MailSendingError(Exception):
    pass


def send_email(user_email: str, channel_email: ChannelEmail, template: ChannelTemplate):
    """
    Send an HTML message with email
    :param user_email: the User to contact
    :param channel_email: the SMTP settings
    :param template: the message to send
    :return:
    :raise: MailSendingError if message not sent
    """
    try:
        sender = channel_email.sender_email
        recipient = user_email

        msg = MIMEMultipart("alternative")
        msg["Subject"] = template.email.subject
        msg["From"] = sender
        msg["To"] = recipient

        part = MIMEText(template.get_email_msg(), "html")
        msg.attach(part)

        with smtplib.SMTP(channel_email.smtp_host, channel_email.smtp_port) as s:
            s.starttls()
            s.login(channel_email.sender_email, channel_email.sender_password)
            s.sendmail(sender, recipient, msg.as_string())

    except Exception as e:
        raise MailSendingError(e)
