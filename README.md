# pymerchant - working title
Hanseatic league merchant trading game, written in Python, inspired by old school games like Vermeer, Patrician, 1860, and Port Royale

# Requirements
Python 3.11
Packages: Rich

This project was built in part with a third party library Rich.
	"Rich is a Python library for rich text and beautiful formatting in the terminal."

See the documentation here and review the repo here:
	Repository: https://github.com/Textualize/rich
	Documentation: https://rich.readthedocs.io/en/stable/index.html

Rich supports both windows and mac/unix systems and supports the classic windows CMD prompt but it has feature support for the new Windows Terminal and it is recommended for better support.

# Install

To get the pepare your system to run Pymerchant, using PyPi or your preferred package manager in your terminal or shell enviroment run the command:

	'pip install Rich'

To run the game itself, in your preferred terminal enviroment, run the pymerchant.py app by calling

	python pymerchant.py


# Background

As of July 2023, The game is still in active development and I am currently working on a feature roadmap. It is the product of a summer semester COSC1336 Intro to Fundamentals of Computer Programming course at Austin Community College. I have spent roughly 40 days thinking about, designing, and developing the game to where it is today. In retrospect, I would approach it a little more differently than I did when I started as I went through multiple refactors and design changes.

Toward the end I purchased "Design Patterns: Elements of Reusable Object Oriented Software" by the Gang of Four "Refactoring: Improving the Design of Existing Code Second Edition" in a fleeting attempt to try to decouple classes and functions and increase cohension but at a loss to pace of development. I tried to strike a balance in delivering a MVP with the knowledge I had and at the same time still think through the problems that I had created for myself in my approach.

In the end, I've learned more in this project about Python and software design than I have in any other setting and intend to continue working on the project, albeit with a pause now to really refactor and change my design and approach. There were many problems that took multiple days of intense focus and thinking. In the last weeks, I have found myself able to almost effortlessly see a problem and immediately can envision a solution to and begin building immediately. I'm hoping with some more reading and programming that this will come even more naturally than it is now.

One thing of note is that commenting and documentation that is missing from functions are from the latest work where pressed for time I am submitting without and will document and reformat later at a github repo yet to be released.

# Gameplay
You are merchant of the Hanse, in the 12th century in Northern Europe. You travel with your cog across the seas from one hanseatic city to another trading goods that were historically traded in these times. You start in the city of Lubeck, the capital city of the Hanseatic league. With 1000 gold (historically denarius) you set out to buy low and sell high traveling from city to city.

Currently the game features a command-line interface and has some features such as a in-game clock that advances with time, table representation inventory management, hand routed distances in nautical miles between cities, active loading bars that run in command line and dynamic per item pricing in each city.

# Roadmap
Currently the game has been designed from outset to describe advanced and dynamic pricing models for trade goods using regions, cities, distances, and market events that affect supply and demand! Goods are inputs to other goods as well and as such, their pricing will affect and build up the prices of those composite goods. In addition to the market event shocks that describe real world supply and demand shocks, there is in place a framework to describe travel modifiers that will slow or prevent your ships from traveling to certain cities when ports are frozen over, or a blockade occurs and the consequences of pirate activity on the seas.

In addition, because of the date time system that is currently implemented, market events, which will be displayed to the user through interactions with towns people, can be created, dispatched, and set for destruction or add different effects on a time scale that the user can take advantage of.

# Closing
In the end this is as much of a labor of love born out of my love of old economic trading games and my background in Finance as it is a learning opportunity. In the time that I have been studying programming in the last few years, nothing comes close to this project in helping develop my understanding and improving my fluency in reading and interpretting code.

# Contribute
 If you have comments or would like to contribute to this project please email me at michael.a.golden@gmail.com

# License

MIT License

Copyright (c) 2023 Michael Golden

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

