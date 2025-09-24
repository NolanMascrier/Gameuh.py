![Tests](https://github.com/NolanMascrier/Gameuh.py/actions/workflows/tests.yml/badge.svg) [![codecov](https://codecov.io/gh/NolanMascrier/Gameuh.py/branch/main/graph/badge.svg)](https://codecov.io/gh/NolanMascrier/Gameuh.py) ![Pylint](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/NolanMascrier/Gameuh.py/refs/heads/gh-pages/pylint-badge.json?refresh=true)

Currently in a playble state !
# Gameuh.py
A python rewrite of my favourite University project, a small incremental dungeon crawler.

Instead, it's now a looter bullet hell. Yeah
# TODO list
* ~~Adding the jewel system for spells~~ Done !
* ~~Adding jewels to the loot pools~~ Done !
* ~~Rewrite the spellbook page, adding data about cooldown, costs, projectiles ...~~ Done !
* ~~Adding area modifier and level selector~~ Done !
* Adding at least two bosses (Wave boss and unique boss)
* Adding more options in the options menu (gamma, color correction, etc)
* Real saving system
* Adding general content
* Deciding on a art style and theme (thinking of going for Mechas ?)
* Sounds and musics ?
* Lore and story mode ?
* More game modes (boss rush, rogue like infinite waves, dungeons ?)
* General optimisation -> Objective is a stable 50-60 FPS in battle

# Known Bugs
* ~~After dragging a spell to a spellslot, it cannot be removed (it can be overwritten though) until the page is reloaded~~ FIXED
* Random SEGFAULT when launching a level (Origin of the error unknown, reoccurs randomly)
* ~~The same item is sometimes added multiple time to the inventory~~ FIXED

# Launching the game
You can clone the repo and compile it yourself, either by compiling and launching the launcher in `wrapper/`, or simply calling python from your own system or a virtual env.

You can also download the releases version; Linux version assumes you already have up-to-date `git` and `python3` installation. Windows version comes with a prepackaged git and python. Due to using pygame, you must have a python 3.12 installation for it to work.
