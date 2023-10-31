#!/usr/bin/env python3

import time

def main():

    date = time.ctime(time.time())
    print(date)
    file_name = "Drawing " + date +".png"
    print("Saving png image as " + file_name)

if __name__ == "__main__":
    main()