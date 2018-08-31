# Hack-a-neck

Microsoft Award winning hack from CambridgeHack Recurse 2017

## Demo:
https://vimeo.com/201535797

## Devpost:
https://devpost.com/software/pain-in-the-neck

## Inspiration

As all the programmers we also experience the downsides of hours of hacking in front of computers. While researchers constantly encourage the importance of stretching exercise to release tension in our muscles, it is not always an appealing activity. As it is difficult to get out of the work zone, we propose a nerdy and fun solution that also takes good care of your health. Inspired by the Arthritis Research UK, we designed a software that encourages the programmers to remotely control the game flow while exercising the neck and face muscles.

## What it does

It allows the users to remotely control the game using the movement of their necks and heads in near real time, which are based on the simple excercises recommended by the Arthritis Research UK. Consequently it releases the tension and allows you to take a break from intensive work. More importantly, it is a great fun!

## How we built it

interfaceWe used the Microsoft Cognitive Services, in particular, faces and emotions APIs to track the position of the head with respect to xy axes in order to link the user movement to the game control. In addition, a twist was added with the emotions API to perform certain actions with some facial expressions. We used Pygame and multithreading to control the game flow in near real time. We implemented two games, a Tetris and a Football dribbler for different target groups. We also considered features to alert the users when they stayed in the same position for too long, and offered a game.
