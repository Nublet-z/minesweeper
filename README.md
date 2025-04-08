# Minesweeper
## Installation
To run the game, you need to have a python installed on your machine. You can first create the python environment by running the following command:
```bash
$ conda create -n minesweeper python=3.8
$ conda activate minesweeper
```

After that installed all the requirements using the following command:
```bash
$ pip install -r requirements.txt
```

## Run the app
This app can be run on both GUI and console. However, for the console mode the program will only printing the generated board with the mines location.

There are several settings that you can adjust to generate the game board:
- `--board_height`: Height of the board (number of tiles)
- `--board_width` : Width of the board (number of tiles)
- `--mines_number` : Number of mines
- `--game_level` : Difficulty level (easy, medium, hard)
- `--gui` : A boolean parameter to enable GUI mode

If you set the game level, it will change the other settings except the gui into a default settings based on the level difficulties.

To run the app on GUI, you can try with the following command:
```bash
# With medium level default settings
$ python main.py --game_level 'medium' --gui

# Using custom settings
$ python main.py --board_height 16 --board_width 10 --mines_number 20 --gui
```

While to run it on console, you just need to remove `--gui` from the command:
```bash
# With medium level default settings
$ python main.py --game_level 'medium'

# Using custom settings
$ python main.py --board_height 16 --board_width 10 --mines_number 20
```
