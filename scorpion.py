#!/bin/python3

# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: sleleu <sleleu@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/09/17 00:26:45 by sleleu            #+#    #+#              #
#    Updated: 2023/09/17 00:27:51 by sleleu           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse

YELLOW = "\033[1;33m"
RED = "\033[0;31m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_GREEN = "\033[1;32m"
LIGHT_RED = "\033[1;31m"
END = "\033[0m"

ascii_header = """
  _________                         .__               
 /   _____/ ____  _________________ |__| ____   ____  
 \_____  \_/ ___\/  _ \_  __ \____ \|  |/  _ \ /    \ 
 /        \  \__(  <_> )  | \/  |_> >  (  <_> )   |  \\
/_______  /\___  >____/|__|  |   __/|__|\____/|___|  /
        \/     \/            |__|                  \/ 

                Created by : https://github.com/Sleleu
"""
# Ascii font info : Figlet conversion by patorjk, April 17, 2008

def parse_arguments() -> list:
    desc = "Scorpion receive image files as parameters and parse them for EXIF"
    parser = argparse.ArgumentParser(description=desc)

    parser.usage = "./scorpion.py FILE1 [FILE2 ...]"
    parser.add_argument("FILES", nargs='+', help="List of files from which you want to extract metadata")
    files: list = parser.parse_args().FILES
    return (files)

def scorpion(files: list) -> None:
    print(files)

if __name__ == "__main__":
    print(f"{LIGHT_RED}{ascii_header}{END}")
    files = parse_arguments()
    scorpion(files)