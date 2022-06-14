# Git Switcherly

Git Switcherly is a lightweight GitHub account switcher. It allows you to create an RSA-Keypair for GitHub SSH-Access. Using GitHub via SSH is generally better than via HTTPS anyway. The Profiles get stored in the config file. You can then simply switch accounts within the CLI. In the background, all it does is change the `~/.ssh/config` file and use the `ssh-agent` to change the private key in your credentials manager.

## Platforms support
I have tested the Tool on Windows. The inquirer package can sometimes be buggy in the cmd. If you're on Windows, then use the Git Bash Terminal. I haven't tested the tool on Linux, but it should work flawlessly.

Windows 10 | Linux | MacOS
:------------ | :-------------| :-------------|
:heavy_check_mark: | :heavy_check_mark: |  :no_entry:

## Dependencies
For the script to work you need following things installed on your computer:
- Git (Obviously)
- PIP-Packages from `requirements.txt`

## Why?
Git Switcherly is a simple tool I wrote. I always had issues switching accounts on my Windows-Computer. I quickly sought for the best practices in regard to GitHub account management on a single PC. Upon looking at some tutorials, the whole (tedious) process annoyed me. I wrote a little tool that makes my life much easier. Maybe someone else's too.

## Installation / Usage
The "Installation" is easy. You simply clone this repository and run the `main.py` file. You could add the tool to your enviroment-variables. With this, you could access git-switcherly without going into the folder. A simple alias in your `.bashrc` would also do it.
```bash
git clone <this repo>
cd git-switcherly
python3 main.py
```

## Contributing
Pull requests are more than welcome. For major changes, please open an issue first to discuss what you would like to change. I wrote this tool in a day, so I know there are some things that could be improved.

## Todo
- [] Refactoring
- [] Import Identities/Accounts

... potentially even more :)

## License
[MIT](https://choosealicense.com/licenses/mit/)