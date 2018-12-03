# Sp00k-Invaders

## About
This was created for Local Hack Day 2018. This project is inspired by Space Invaders. It includes a custom built controller using an Arduino Uno, joystick and accelerometer modules. The Arduino then reads the signals from the modules and is transmitted over serial to your computer. The python program will parse the serial controls to control the players ship. The play is able to rotate the controller to aim their ships directions. Pressing the joystick allows for the player ship to start shooting. The joystick is used to control the ships movement. The game gets more spooky as the players score increases. Most of the game logic came within the last 1.5 hours of the competition and is very basic. I have plans to continue working on this as this was my first attempt at any kind of game.


## Requirements
* Python 3.x
    * Pygame
    * Pyserial
* Arduino

## Installation
`pip3 install -r requirements.txt`

## Running
`python3 thegame.py`
