# pip install pycryptodome
from Crypto.Protocol.KDF import bcrypt
import subprocess
import os
from getpass import getpass

with open("db/_init_db.js", "r") as f:
    script_js = f.read()

db_password = getpass("Enter the password to use with the Passive DNS database user\n")

admin_name = input("Enter the application administrator username: ")
admin_email = input("Enter the application administrator email: ")
admin_password = getpass("Enter the application administrator password: ")
admin_hashed_password = bcrypt(admin_password, 14).decode()

tmp_file = "db/_init_db_tmp.js"
with open(tmp_file, "w") as f:
    script_js = script_js.replace("{db_password}", db_password)
    script_js = script_js.replace("{admin_name}", admin_name)
    script_js = script_js.replace("{admin_email}", admin_email)
    script_js = script_js.replace("{admin_hashed_password}", admin_hashed_password)
    f.write(script_js)


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line 
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

print("Enter the the database root password")
for line in execute(["arangosh", "--javascript.execute", f"{tmp_file}"]):
    print(line)



os.unlink(tmp_file)


