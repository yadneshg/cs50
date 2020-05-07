import os
import shutil
from os import path


def main():
    # make a duplicate of an existing file

    if path.exists("guru99.txt"):
        # get the path to the file in the current directory
        src = path.realpath("guru99.txt");

        # rename the original file
        os.rename('guru99.txt', 'career.guru99.txt')


if __name__ == "__main__":
 main()
