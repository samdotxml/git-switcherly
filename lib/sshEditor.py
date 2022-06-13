from sshconf import read_ssh_config

# add host entry to ~/.ssh/config
def changeHost(path, username):
    import os

    if not os.path.isfile(path):
        open(path, 'w').close()

    c = read_ssh_config(path)
    username = "~/.ssh/id_rsa_{uname}".format(uname=username)
    if('github.com' in c.hosts()):
        c.set("github.com", Hostname="github.com", User="git", IdentityFile=username)
    else:
        c.add("github.com", Hostname="github.com", User="git", IdentityFile=username)
    c.save()