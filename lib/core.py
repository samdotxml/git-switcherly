import os
import json
import subprocess
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

def generate_key_str():
    # generate private/public key pair
    key = rsa.generate_private_key(backend=default_backend(), public_exponent=65537, \
        key_size=2048)

    # get public key in OpenSSH format
    public_key = key.public_key().public_bytes(serialization.Encoding.OpenSSH, \
        serialization.PublicFormat.OpenSSH)

    # get private key in PEM container format
    pem = key.private_bytes(encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption())

    # decode to printable strings
    private_key_str = pem.decode('utf-8')
    public_key_str = public_key.decode('utf-8')
    return [private_key_str, public_key_str]

#create keys and save them to file
def create_keys(data):
    username = data['githubName']
    email = data['githubEmail']
    keys = generate_key_str()
    priv_key_filename = get_folder() + "id_rsa_{uname}".format(uname=username)
    pub_key_filename = get_folder() + "id_rsa_{uname}.pub".format(uname=username)

    priv_key_file = open(priv_key_filename, "w")
    priv_key_file.write(keys[0])

    pub_key_file = open(pub_key_filename, "w")
    pub_key_file.write(keys[1])

    priv_key_file.close()
    pub_key_file.close()

    add_config_profile(username, email,"id_rsa_{uname}".format(uname=username), "id_rsa_{uname}.pub".format(uname=username))

#check if file exists
def check_file_existence(username):
    filename = get_folder() + "id_rsa_{uname}".format(uname=username)
    return os.path.isfile(filename)

#add config entry of profile
def add_config_profile(username, email, privkeypath, pubkeypath):
    file = open('config/config.json')
    data = json.load(file)
    file.close()

    data_block = {"Github Username" : username, "Github E-Mail" : email, "Private Key" : privkeypath, "Public Key" : pubkeypath}
    data['profiles'].append(data_block)

    json_object = json.dumps(data, indent = 4)
    with open('config/config.json', 'w') as outfile:
        outfile.write(json_object)
        outfile.close()

#read config json and return all profiles
def get_profiles():
    file = open('config/config.json')
    data = json.load(file)
    file.close()

    profiles = []
    for profile in data["profiles"]:
        profiles.append({"username" : profile["Github Username"], "email" : profile["Github E-Mail"]})
    return profiles

#check if ssh folder exists
def folder_exist():
    ssh_folder_path = str(Path.home()) + "/.ssh"
    return os.path.isdir(ssh_folder_path)

#get ssh folder
def get_folder():
    return str(Path.home().as_posix()) + "/.ssh/"

#run git bash with command specified
def run_git_bash_agent(key_path):
    key_path = str(Path.home().as_posix()) + "/.ssh/" + key_path
    path = Path().absolute().as_posix()
    script_path = path + "/ssh-agent.sh"
    proc = subprocess.Popen(["C:\Program Files\Git\git-bash.exe", script_path, key_path],
                     bufsize=-1,
                     executable=None,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     preexec_fn=None,
                     close_fds=True,
                     shell=False,
                     cwd=path,
                     )
    proc.wait()

def get_email(username):
    file = open('config/config.json')
    data = json.load(file)
    file.close()

    for profile in data["profiles"]:
        if(profile["Github Username"] == username):
            return profile["Github E-Mail"]

def edit_git_globaconfig(username, email):
    os.system("git config --global user.name \"{uname}\"".format(uname=username))
    os.system("git config --global user.email \"{address}\"".format(address=email))
