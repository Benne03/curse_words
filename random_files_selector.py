# Author: Benne Jongsma
# Date: 24-3-2022
# File name: random_files_selector.py
# Usage: python3 random_files_selector.py gz_files.txt
# A python program that uses a text file from the command-line that contains
# the paths to the compressed files from the corpus on each line and selects
# 10 lines(paths) randomly.

import random
import sys


def select_random_lines(file):
    """selects 10 random lines from the text file that do not contain the
    string 'Tekst' in them.
    """

    filtered_lines = []
    with open(file) as fr:
        for line in fr:
            if "Tekst" not in line:
                filtered_lines.append(line.rstrip())
    random_line = "\n".join(random.sample(filtered_lines, 10))
    return random_line


def main(argv):
    print(select_random_lines(argv[1]))


if __name__ == "__main__":
    main(sys.argv)