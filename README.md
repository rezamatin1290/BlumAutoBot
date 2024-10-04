

﻿# BlumAutoBot

Blum Auto Bot is script that uses blum api to get points automatically without extra effort     
copy your query link blum account in `url.txt` file which can support multi account(> every line one account)

<hr>

# How To work
+ Very simple, no need telegram web
+ does not need to login to the Telegram account

  1. Need Enable webview inspecting option (in the `Telegram settings => Advanced => Experimental settings => Enable webview inspecting`)
  2. Press **F12** then in the console tab
  3. Copy **Authorization** and enter it in the program

https://github.com/user-attachments/assets/69b25085-dfb7-49af-89de-c884717bcb0b

# What is config.json?
config that you can change in `config.json` file
like Below

```python
{
    "interval": 5, 
    "auto_complete_task": False, 
    "auto_play_game": True, 
    "game_point": {
        "low": 240,
        "high": 250
    }
}
```

set `auto_complete_task` to `True` if you want to complete task automatically in blum     
set `auto_play_game` to `True` if you want to script to use cards automatically to get point in range low and high gamepoint            

#####  If you find this project useful, please consider giving it a star! 
﻿
