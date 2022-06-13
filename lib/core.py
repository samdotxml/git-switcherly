from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from pathlib import Path
import os
import json
import subprocess

def generateKeyStr():
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
def createKeys(data):
    username = data['githubName']
    email = data['githubEmail']
    keys = generateKeyStr()
    privKeyFileName = getFolder() + "id_rsa_{uname}".format(uname=username)
    pubKeyFileName = getFolder() + "id_rsa_{uname}.pub".format(uname=username)

    privkeyFile = open(privKeyFileName, "w")
    privkeyFile.write(keys[0])

    pubkeyFile = open(pubKeyFileName, "w")
    pubkeyFile.write(keys[1])

    privkeyFile.close()
    pubkeyFile.close()

    addConfigProfile(username, email,"id_rsa_{uname}".format(uname=username), "id_rsa_{uname}.pub".format(uname=username))

#check if file exists
def checkFileExistence(username):
    fileName = getFolder() + "id_rsa_{uname}".format(uname=username)
    return os.path.isfile(fileName)

#add config entry of profile
def addConfigProfile(username, email, privkeypath, pubkeypath):
    f = open('config/config.json')
    data = json.load(f)
    f.close()

    dataBlock = {"Github Username" : username, "Github E-Mail" : email, "Private Key" : privkeypath, "Public Key" : pubkeypath}
    data['profiles'].append(dataBlock)

    json_object = json.dumps(data, indent = 4)
    with open('config/config.json', 'w') as outfile:
        outfile.write(json_object)
        outfile.close()

#read config json and return all profiles
def getProfiles():
    f = open('config/config.json')
    data = json.load(f)
    f.close()

    profiles = []
    for x in data["profiles"]:
        profiles.append({"username" : x["Github Username"], "email" : x["Github E-Mail"]})
    return profiles

#check if ssh folder exists
def folderExist():
    sshFolderPath = str(Path.home()) + "/.ssh"
    return os.path.isdir(sshFolderPath)

#get ssh folder
def getFolder():
    return str(Path.home().as_posix()) + "/.ssh/"

#run git bash with command specified
def runGitBashAgent(keyPath):
    keyPath = str(Path.home().as_posix()) + "/.ssh/" + keyPath
    path = Path().absolute().as_posix()
    scriptPath = path + "/ssh-agent.sh"
    p = subprocess.Popen(["C:\Program Files\Git\git-bash.exe", scriptPath, keyPath],
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
    p.wait()