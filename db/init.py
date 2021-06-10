# pip install pycryptodome
from Crypto.Protocol.KDF import bcrypt
import subprocess
import os
from getpass import getpass

with open("db/_init_db.js", "r") as f:
    script_js = f.read()

db_password = getpass("Enter the password for the database user (passive_dns_user)\n")

admin_name = input("Enter the application administrator username: ")
admin_email = input("Enter the application administrator email: ")
admin_password = getpass("Enter the application administrator password: ")
admin_hashed_password = bcrypt(admin_password, 14).decode()
smtp_host = input("Enter the SMTP host to use when sending automated mails: ")
smtp_port = input("Enter the SMTP port: ")
sender_email = input("Enter the email address to use when sending automated mails: ")
sender_password = input("Enter the SMTP password: ")

tmp_file = "db/_init_db_tmp.js"
with open(tmp_file, "w") as f:
    script_js = script_js.replace("{db_password}", db_password)
    script_js = script_js.replace("{admin_name}", admin_name)
    script_js = script_js.replace("{admin_email}", admin_email)
    script_js = script_js.replace("{admin_hashed_password}", admin_hashed_password)
    script_js = script_js.replace("{smtp_host}", smtp_host)
    script_js = script_js.replace("{smtp_port}", smtp_port)
    script_js = script_js.replace("{sender_email}", sender_email)
    script_js = script_js.replace("{sender_password}", sender_password)
    f.write(script_js)

