#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This is the description of the module"""

import os
import random
import time
import sys
import threading

WIDTH = 80  # Terminal number of columns
HEIGHT = 24  # Terminal number of rows
MAX_WEIGHT = 6
MIN_HEIGHT = 6  # Should be greater than MAX_WEIGHT
MAX_HEIGHT = 23  # Should be greater than MIN_HEIGHT and lower than HEIGHT

COL_TIME = (0.05, 0.1)  # Time constant possible values
NB_SPACE = 7  # Density factor

USED_BAND = (32, 126)  # ASCII band used
COLOR = ("\u001b[32m", "\u001b[0m")  # ANSI codes used at the beginning
UP = "\u001b[{}A"
DOWN = "\u001b[{}B"
RIGHT = "\u001b[{}C"
LEFT = "\u001b[{}D"
ORIGIN = (UP + LEFT).format(HEIGHT + 2, WIDTH + 2)

lock = threading.RLock()
pprint = sys.stdout.write


def randchar():
    """Return a random character"""
    return chr(random.randint(*USED_BAND))


class ColumnHandler(threading.Thread):
    """Handle a column"""

    def __init__(self, col_no):
        """Init method"""
        super().__init__()
        self._col = []
        self._col_no = col_no
        self._height = random.randint(MIN_HEIGHT, MAX_HEIGHT)
        self._weight_max = min(self._height, MAX_WEIGHT)
        self._col = [" "] * self._height
        self._weight = 0
        self._falling = True
        self._col_time = (COL_TIME[0] +
                          random.random() * (COL_TIME[1] - COL_TIME[0]))
        self._running = True

    def make_forward(self):
        """Compute the new column"""
        if self._falling:
            if random.random() < 1 / (NB_SPACE - 1):
                self._col = [randchar()] + self._col[:-1]
                self._falling = False
                self._weight = 1
            else:
                self._col = [" "] + self._col[:-1]
        else:
            if self._weight > self._weight_max:
                self._col = [" "] + self._col[:-1]
                self._falling = True
            else:
                self._col = [randchar()] + self._col[:-1]
                self._weight += 1

    def draw(self):
        """Draw the column on the screen"""
        start_time = time.time()
        with lock:
            pprint(ORIGIN)
            if self._col_no:
                pprint(RIGHT.format(self._col_no))
                for char in self._col:
                    pprint(char + LEFT.format(1) + DOWN.format(1))
            sys.stdout.flush
        elapsed_time = time.time() - start_time
        if elapsed_time < self._col_time:
            time.sleep(self._col_time - elapsed_time)
            # time.sleep(self._col_time)

    def run(self):
        """Thread launching method"""
        while self._running:
            self.make_forward()
            self.draw()

    def stop(self):
        """Stop the thread"""
        self._running = False


class ThreadPool(object):
    """Handle a pool of ColumnHandler threads"""

    def __init__(self, width):
        """Init method"""
        super().__init__()
        self._pool = []
        self._width = width
        for col_no in range(self._width):
            self._pool.append(ColumnHandler(col_no))

    def launch_pool(self):
        """Launch the thread pool"""
        for thread in self._pool:
            thread.start()

    def join_pool(self):
        """Wait the end of each thread"""
        for thread in self._pool:
            thread.join()

    def stop_pool(self):
        """Stop the thread pool"""
        for thread in self._pool:
            thread.stop()

    def terminate_pool(self):
        """Correctly terminate all threads"""
        try:
            self.join_pool()
            print("M A T R I X   K I L L E D")
        except:
            print("\nK I L L I N G   M A T R I X . . .")
            self.stop_pool()
            self.terminate_pool()


def main():
    """Main function"""
    os.system("clear")
    my_pool = ThreadPool(WIDTH)
    pprint(COLOR[0])
    my_pool.launch_pool()
    my_pool.terminate_pool()
    pprint(COLOR[1])


if __name__ == "__main__":
    main()
