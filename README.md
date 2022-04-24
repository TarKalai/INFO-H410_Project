# 2048

You will find here below the instructions and details on the 2048 game. The goal of the game is to merge as much tiles as possible and try to reach the 2048 tile. To merge tiles they need to have the same number, and each time tiles merge the resulting number of the merge is added to your score.

this implementation of the game uses 2 different AI : Expectimax and Montecarlo. You can fine tune the settings in the setting.py file

# Installation

To install the application, first start by coping the git repository, either by getting the zip archive from github, or with the command:

```
git clone https://github.com/TarKalai/INFO-H410_Project.git
```
then acces the file :
```
cd 2048
```
after you have installed python and poetry, you can start installing the dependecies for the project by running :
```
poetry install
```
# Utilisation 
to launch the game :
```
poetry run python main.py
```