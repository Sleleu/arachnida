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
from PIL import Image
from PIL.ExifTags import TAGS

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

def printImageInfo(image: Image) -> None:
    is_animated = getattr(image, "is_animated", False)
    nb_frames = getattr(image, "n_frames", 1)
    print(f"{LIGHT_GREEN}Format description:{YELLOW}  {image.format_description} | {image.format}{END}")
    print(f"{LIGHT_GREEN}Mode:{YELLOW}                {image.mode}{END}")
    print(f"{LIGHT_GREEN}Size:{YELLOW}                {image.size} (width x height){END}")
    print(f"{LIGHT_GREEN}Color Palette:{YELLOW}       {image.palette}{END}")
    print(f"{LIGHT_GREEN}Is animated:{YELLOW}         {is_animated}{END}")
    print(f"{LIGHT_GREEN}Frames in image:{YELLOW}     {nb_frames}{END}")
    for tag, data in image.info.items():
        if isinstance(data, bytes):
            try:
                data = data.decode()
            except:
                data = "Non readable data"
        print(f"{LIGHT_GREEN}{tag:20}{YELLOW} {data}{END}")

def printExifInfo(exif_data) -> None:
    if exif_data:
        for tag_id in exif_data:
            tag = TAGS.get(tag_id, tag_id) # Transform tag id to human readable string
            data = exif_data.get(tag_id) # Get data from tag id
            if isinstance(data, bytes):
                data = data.decode()
            print(f"{LIGHT_GREEN}{tag + ':':20}{YELLOW} {data}{END}")
    else:
        print(f"{LIGHT_GREEN}EXIF data:{YELLOW}           None{END}")

def scorpion(file: str) -> None:
    try:
        image = Image.open(file)
    except:
        print(f"{YELLOW}\nCannot open file: {file}{END}\n")
        return
    print(f"\n{LIGHT_RED}|----- Extracting metadata from {YELLOW}'{file}'{LIGHT_RED}-----|\n{END}")
    printImageInfo(image)
    exif_data = image.getexif()
    printExifInfo(exif_data)

if __name__ == "__main__":
    print(f"{LIGHT_RED}{ascii_header}{END}")
    files = parse_arguments()
    for file in files:
        scorpion(file)