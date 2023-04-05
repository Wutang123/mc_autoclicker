
import sys
import time
import threading
import random
import pynput.mouse
from pynput.mouse import Button
import pynput.keyboard
from pynput.keyboard import Key
import logging
from gui import Gui_Interface
import argparse


class ClickMouse(threading.Thread):
    def __init__(self, testing):
        super(ClickMouse, self).__init__()
        self.trident_running   = False
        self.bow_running       = False
        self.sword_running     = False
        self.pickaxe_running   = False
        self.program_running   = True

        self.sword_start_time  = 0

        self.commands_string   = []

        if testing:
            self.afk_time_seconds_start_range = 5
            self.afk_time_seconds_end_range   = 10
        else:
            self.afk_time_seconds_start_range = 60 * 2
            self.afk_time_seconds_end_range   = 60 * 3


    def trident_start_clicking(self):
        self.trident_running = True


    def trident_stop_clicking(self):
        self.trident_running = False


    def bow_start_clicking(self):
        self.bow_running = True


    def bow_stop_clicking(self):
        self.bow_running = False


    def sword_start_clicking(self):
        self.sword_running    = True
        self.sword_start_time = time.time()
        self.commands_string  = []


    def sword_stop_clicking(self):
        self.sword_running    = False
        self.commands_string  = []


    def pickaxe_start_clicking(self):
        self.pickaxe_running = True


    def pickaxe_stop_clicking(self):
        self.pickaxe_running = False


    def stop_other_runs(self):
        self.trident_stop_clicking()
        self.bow_stop_clicking()
        self.sword_stop_clicking()
        self.pickaxe_stop_clicking()


    def exit(self):
        logging.info("exit")
        self.stop_other_runs()
        self.program_running = False


    def not_afk(self):
        logging.info("\tI'm not AFK!")

        typing_delay_start_range = 0.12
        typing_delay_end_range   = 0.15
        enter_delay_start_range  = 0.3
        enter_delay_end_range    = 0.5

        # Randomly choose command path
        choice = random.choice([0, 1, 2])
        logging.info(f"choice = {choice}")
        if choice == 0:
            self.commands_string  = ["location", "wwww", "1", "/back", "2"]
        elif choice == 1:
            self.commands_string  = ["/pv 5", "esc", "sssss", "     ", "wwwww"]
        elif choice == 2:
            self.commands_string  = ["/pv 7", "esc", "location", "            ", "/back"]

        for command_string in self.commands_string:

            # Randomly choose a location
            if command_string == "location":
                choice = random.choice([0, 1])
                logging.info(f"\choice = {choice}")
                if choice == 0:
                    command_string = "/mine"
                elif choice == 1:
                    command_string = "/orechunk"

            press_enter = False
            if "/" in command_string:
                press_enter = True

            # Press esc
            if command_string == "esc":
                keyboard.press(Key.esc)
                keyboard.press(Key.esc)
                time.sleep(random.uniform(typing_delay_start_range, typing_delay_end_range))
                continue

            for idx, ch in enumerate(command_string):

                if ch != " ":
                    keyboard.press(ch)

                    # For walking
                    if ch == "w" or ch == "s" or ch == "a" or ch == "d":
                        time.sleep(random.uniform(typing_delay_start_range, typing_delay_end_range))

                    keyboard.release(ch)

                else: # Press space
                    keyboard.press(Key.space)
                    keyboard.release(Key.space)

                time.sleep(random.uniform(typing_delay_start_range, typing_delay_end_range))

                # Momentary mining
                if ch == "1":
                    mining_time_end = time.time() + 10
                    first_press = True
                    while time.time() < mining_time_end:
                        if first_press:
                            mouse.press(Button.left)
                            first_press = False
                    mouse.release(Button.left)

                # Press enter after each command
                if press_enter and (idx == len(command_string) - 1):
                    keyboard.press(Key.enter)
                    keyboard.release(Key.enter)
                    time.sleep(random.uniform(enter_delay_start_range, enter_delay_end_range))

        # Update timer
        self.sword_start_time = time.time()


    def run(self):
        while self.program_running:
            # Trident/Bow
            while self.trident_running:
                delay_start_range = 1.0
                delay_end_range   = 1.1
                delay = random.uniform(delay_start_range, delay_end_range)
                logging.debug(f"\tdelay = {delay}")

                mouse.press(Button.right)
                time.sleep(delay)
                mouse.release(Button.right)
                time.sleep(delay)

            # Bow
            while self.bow_running:
                delay_start_range = 0.9
                delay_end_range   = 1.2
                delay = random.uniform(delay_start_range, delay_end_range)
                logging.debug(f"\tdelay = {delay}")

                mouse.press(Button.right)
                time.sleep(delay)
                mouse.release(Button.right)
                time.sleep(delay)

            # Sword
            while self.sword_running:
                # Delay between each click (in seconds), average person cps is 6.51
                delay_start_range = 0.15
                delay_end_range   = 0.25
                delay = random.uniform(delay_start_range, delay_end_range)
                logging.debug(f"\tdelay = {delay}")

                mouse.click(Button.left)
                time.sleep(delay)

                # AFK BOT
                if time.time() - self.sword_start_time >= random.uniform(self.afk_time_seconds_start_range, self.afk_time_seconds_end_range):
                    self.not_afk()

            time.sleep(0.1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--testing', default=False, action='store_true')
    args = parser.parse_args()

    if args.testing:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info("Starting Program....")

    mouse        = pynput.mouse.Controller()
    keyboard     = pynput.keyboard.Controller()
    click_thread = ClickMouse(args.testing)
    click_thread.start()

    gui = Gui_Interface(mouse, keyboard, click_thread)
    gui.run()

    logging.info("Exiting Program...")
    sys.exit()