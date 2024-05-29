# pip install pycryptodome
from Crypto.Protocol.KDF import bcrypt
import subprocess
import os
from getpass import getpass

with open("db/_init_db.js", "r") as f:
    script_js = f.read()


print("[DATABASE CONFIGURATION]")
db_root_password = getpass("Enter the password for the database root: ")
db_password = getpass("Enter the password for the database user (passive_dns_user): ")

with open("env/default/default.db.env", "r") as f:
    db_env = f.read()

with open("env/db.env", "w") as f:
    db_env = db_env.replace("{db_root_password}", db_root_password)
    f.write(db_env)


print("\n[APPLICATION ADMIN]")
admin_name = input("Enter the application administrator username: ")
admin_email = input("Enter the application administrator email: ")
admin_password = getpass("Enter the application administrator password: ")
admin_hashed_password = bcrypt(admin_password, 14).decode()

print("\n[APPLICATION SECURITY]")
jwt_key = getpass("Enter the key to use for creating JWT: ")

print("\n[APPLICATION MISC]")
timezone = input(
    "Enter your timezone (i.e: 'Europe/Paris') (if not provided, UTC is used): "
)
if timezone == "":
    timezone = "UTC"

with open("env/default/default.api.env", "r") as f:
    api_env = f.read()


with open("env/api.env", "w") as f:
    api_env = api_env.replace("{db_password}", db_password)
    api_env = api_env.replace("{jwt_key}", jwt_key)
    api_env = api_env.replace("{timezone}", timezone)
    f.write(api_env)

print("\n[DEFAULT MAIL CHANNEL]")
smtp_host = input("Enter the SMTP host to use when sending automated mails: ")
smtp_port = input("Enter the SMTP port: ")
sender_email = input("Enter the email address to use when sending automated mails: ")
sender_password = getpass("Enter the SMTP password: ")

print("\n[DEFAULT SCHEDULER]")
scheduler_name = input("Enter the name of the default scheduler: ")
scheduler_password = getpass("Enter the scheduler password: ")
scheduler_hashed_password = bcrypt(scheduler_password, 14).decode()

with open("env/default/default.scheduler.env", "r") as f:
    sched = f.read()

with open("env/scheduler.env", "w") as f:
    sched = sched.replace("{scheduler_user}", scheduler_name)
    sched = sched.replace("{scheduler_password}", scheduler_password)
    f.write(sched)

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
    script_js = script_js.replace("{scheduler_name}", scheduler_name)
    script_js = script_js.replace(
        "{scheduler_hashed_password}", scheduler_hashed_password
    )
    f.write(script_js)
