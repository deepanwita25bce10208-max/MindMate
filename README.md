# MindMate

A mental health based app, for mood tracking and journal writing. 

-------

## Overview

This project is a desktop app designed to help users keep track of their daily mood and thoughts. It uses Python and Tkinter to provide an offline, easy-to-use interface where entries are saved locally to a JSON file. The goal is to offer a straightforward tool anyone can use to reflect on how they're feeling over time, without the complexity or distractions of larger apps, and offers the user complete control over the data they have.

-------

## Features

- Clean, minimalistic Tkinter interface
- Daily mood entries can be added along with journal notes
- Automatically stores each entry with a date and time
- Saves all data to a local JSON file so the user has full control
- Allows users to view their past entries at any time

-------

## Tools Used

- Python 3.x
- Tkinter (for the graphical interface)
- JSON (for local data storage)
- OS module (basic file handling)

-------

## Steps to Install and Run the Project

- Ensure Python 3 is installed on your system
- Download or clone the project folder from GitHub
- Open the folder in your code editor or terminal
- Run the main Python file using: python main.py

The application window will open and you can start using the mood tracker immediately.

-------

## Instructions for Testing

Open the program and try adding a few mood entries.
Check the JSON file (mood_entries.json) to verify that new entries are being stored correctly.
Reopen the program to confirm that previously saved entries load without issues.

Test edge cases like empty notes or repeated entries to ensure the program behaves as expected.
