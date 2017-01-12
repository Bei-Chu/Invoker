# Invoker
This program helps playing hero Invoker in game Dota 2.

Only support playing under 1920*1080 resolution in full screen mode.

## Prerequisites
Anaconda version of Python 2.

PyHook.

## Installation
Download folder Invoker.

## Usage
Run "python Invoker\Invoker.py"

Start Dota 2, choose Invoker, change your key bindings to Dota key bindings

The program will monitor all key events while keeping track of 
certain area of the screen to detect current invoked aibilities
of Invoker.

When you pressed a hotkey of an ability that's not already invoked, the program
converts the key stroke to a series of strokes that invokes the ability and give
Invoker 3 wex instances(for 3 wex is usually most useful during battle).

For example, if your current abilities are cold snap and emp, when you press 't',
Dota 2 will act as if you pressed 'eeerwww'. But if you press 'y', you'll just cast
cold snap.

## Known Issues
