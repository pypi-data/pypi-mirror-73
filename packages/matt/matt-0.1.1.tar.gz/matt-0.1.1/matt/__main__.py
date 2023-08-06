# This file is part of Matt.

# Copyright © 2020 Noisytoot
# MATT - MATT Arithmetic Training Test: Another maths test, this time in Python!

# Matt is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Matt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this Matt.  If not, see <https://www.gnu.org/licenses/>

import argparse, secrets, platform, sys, signal, os
# Import readline except on windows
if platform.system() != 'Windows':
    import readline
from matt.termcolor_wrapper import colored, cprint
from xdg.BaseDirectory import xdg_config_home
from pathlib import Path
config_file = os.path.join(xdg_config_home, "matt", "config.py")
config = {}
try:
    exec(Path(config_file).read_text(), config)
except FileNotFoundError:
    pass

# Initiali(s|z)e colorama (ANSI escape emulation on windows) (windows only)
if platform.system() == "Windows":
    import colorama
    colorama.init()

# Parse command line arguments
parser = argparse.ArgumentParser(prog="mat", description="A maths test program")
parser.add_argument("-m", "--minimum", help="The minimum number", type=str)
parser.add_argument("-M", "--maximum", help="The maximum number", type=str)
parser.add_argument("-o", "--operations", help='Allowed operations ("+", "-", "*", "/"), seperated by commas', type=str)
parser.add_argument("-d", "--difficulty", help="Difficulty profile (preset of difficulty related settings)", type=str)
parser.add_argument("-q", "--question-amount", help="Amount of questions", type=int)
args = parser.parse_args()

def sigint_exit(_signal, _frame):
    print("\nSIGINT caught, exiting…")
    sys.exit(0)

def sigterm_exit(_signal, _frame):
    print("\nSIGTERM caught, exiting…")
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_exit)
signal.signal(signal.SIGTERM, sigterm_exit)


def isfloat(number) -> bool:
    try:
        float(number)
        return True
    except ValueError:
        return False

# Default settings for difficulties
def default_difficulty(namespace, number):
    if namespace == "default":
        if number == 1:
            return {
                "operations": ["+", "-"],
                "maximum": 10,
                "minimum": 0
            }
        elif number == 2:
            return {
                "operations": ["+", "-", "*", "/"],
                "maximum": 20,
                "minimum": 0
            }

def do_level(namespace: str, number: int, question_amount: int):
    if "difficulty" in config and config["difficulty"](namespace, number) != None:
        difficulty = config["difficulty"](namespace, number)
    else:
        difficulty = default_difficulty(namespace, number)
    
    # Set value for minimum and maximum from arguments and default
    try:
        difficulty["minimum"] = int(args.minimum)
    except TypeError:
        if "minimum" not in difficulty:
            difficulty["minimum"] = 0
    try:
        difficulty["maximum"] = int(args.maximum)
    except TypeError:
        if "maximum" not in difficulty:
            difficulty["maximum"] = difficulty["minimum"] + 10
    try:
        difficulty["operations"] = args.operations.split(",")
    except AttributeError:
        if "operations" not in difficulty:
            difficulty["operations"] = ["+", "-", "*", "/"]
    
    score: float = 0
    question: int = 0
    while question < question_amount:
        # Generate random operation
        operation: str = secrets.choice(difficulty["operations"])
        
        # Generate 2 random numbers
        try:
            n1 = secrets.choice(range(difficulty["minimum"], difficulty["maximum"]))
            n2 = secrets.choice(range(difficulty["minimum"], difficulty["maximum"]))
        except IndexError:
            message = f"""\
Fatal Error: minimum cannot be equivalent to maximum
minimum = {difficulty["minimum"]}
maximum = {difficulty["maximum"]}\
"""
            sys.exit(colored(message, "red", attrs=["bold"]))
        if operation == "/":
            divanswer = n1
            n1 = divanswer * n2
        
        # Set correct answer
        if operation == "+":
            correct_answer = n1 + n2
        elif operation == "-":
            correct_answer = n1 - n2
        elif operation == "*":
            correct_answer = n1 * n2
        elif operation == "/":
            correct_answer = divanswer
        
        # Get the user's answer
        answer = ""
        while not isfloat(answer):
            answer = input(colored(f"What is {n1} {operation} {n2}? ", "cyan", attrs=["bold"]))
        answer = float(answer)
        
        # Check the user's answer
        if correct_answer == answer:
            cprint("Correct!", "green", attrs=["bold"])
            score += 1
        elif abs(correct_answer - answer) <= 2:
            points = 0.5 - 4 / difficulty["maximum"]
            cprint(f"Not quite right, the correct answer was {correct_answer}, you get {points} points.", "yellow", attrs=["bold"])
            score += points
        else:
            cprint(f"Wrong, the correct answer was {correct_answer}.", "red", attrs=["bold"])
            question_amount += 1
        
        # Increment the question
        question += 1
    cprint(f"Your score was {score}/{question_amount}.", "yellow", attrs=["bold"])

try:
    difficulty: list = args.difficulty.split(":")
except AttributeError:
    cprint("Warning: difficulty not set, defaulting to default:1", "red", file=sys.stderr)
    difficulty: list = ["default", 1]

try:
    question_amount: int = int(args.question_amount)
except TypeError:
    cprint("Warning: amount of questions not set, defaulting to 10", "red", file=sys.stderr)
    question_amount: int = 10

do_level(difficulty[0], int(difficulty[1]), question_amount)

# Deinitiali(s|z)e colorama (windows only)
if platform.system() == "Windows":
    colorama.deinit()
