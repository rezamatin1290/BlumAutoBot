# BlumAutoBot

Blum Auto Bot is script that uses blum api to get points automatically without extra effort     
copy your query link blum account in `url.txt` file which can support multi account(> every line one account)



## How i can get link of my blum account?  

[Click Here](https://github.com/rezamatin1290/BlumAutoBot/issues/2#issuecomment-2424082631)




## What is config.json?
config that you can change in `config.json` file
like Below

```python
{
    "interval": 5, 
    "auto_complete_task": false, 
    "auto_play_game": true, 
    "game_point": {
        "low": 240,
        "high": 250
    }
}
```

set `auto_complete_task` to `True` if you want to complete task automatically in blum     
set `auto_play_game` to `True` if you want to script to use cards automatically to get point in range low and high gamepoint            

## Features

- [x] Auto Claim
- [x] Multi Account Support
- [x] Auto Play Game

## Linux

1. Make sure you computer was installed python and git.
   
   python
   ```shell
   sudo apt install python3 python3-pip
   ```
   git
   ```shell
   sudo apt install git
   ```

2. Clone this repository
   
   ```shell
   git clone https://github.com/rezamatin1290/BlumAutoBot.git
   ```

3. goto BlumAutoBot directory

   ```shell
   cd BlumAutoBot
   ```
4. Create and Edit `url.txt`, input your link account in `url.txt`. One line for one  account, if you want add your another account add in new line!
5. execute the main program 
   ```
   python main.py
   ```
## Windows 

1. [Download](https://github.com/rezamatin1290/BlumAutoBot/releases/download/v1.0.1/BlumBotWin.rar) and unzip
2. open frontend.exe and put your link in link account field and number of card you want to use enter and click on start

#####  If you find this project useful, please consider giving it a star! 
﻿
