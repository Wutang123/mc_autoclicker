import tkinter
from pynput.mouse import Button
from pynput.keyboard import Listener, Key, KeyCode
import logging
import time

INPUT_SLEEP = 1

class Gui_Interface():
    def __init__(self, mouse, keyboard, click_thread):

        # Create root window
        self.root = tkinter.Tk()

        self.mouse        = mouse
        self.keyboard     = keyboard
        self.click_thread = click_thread

        # The key used for start and stop of the click while you run the program for executing the auto clicker
        self.sword_start_stop_key   = Key.f9
        self.trident_start_stop_key = Key.f10
        self.pickaxe_start_stop_key = Key.f11
        self.bow_start_stop_key     = Key.f12

        # The key used to terminate the auto clicker that is being executed.
        self.stop_key = KeyCode(char='z')

        # GUI window size
        self.window_width  = 400
        self.window_height = 400

        # GUI button size
        self.btn_width  = int(self.window_width / 2)
        self.btn_height = int(self.window_height / 4)

        # GUI button color
        self.btn_bg_unactive_color = "#C1C1CD"
        self.btn_bg_active_color   = "red"

        self.screen_width  = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.window_x = int(self.screen_width / 2) - int(self.window_width / 2)
        self.window_y = int(self.screen_height / 2) - int(self.window_height / 2)
        logging.debug(f"self.screen_width: {self.screen_width}, self.screen_height: {self.screen_height}")

        self.create()


    def trident(self):
        if self.click_thread.trident_running:
            logging.info("=>Stopping click for trident\n")
            self.trident_btn.configure(bg=self.btn_bg_unactive_color)
            self.click_thread.trident_stop_clicking()
        else:
            logging.info("=>Starting click for trident")
            self.trident_btn.configure(bg=self.btn_bg_active_color)
            self.click_thread.stop_other_runs()
            self.click_thread.trident_start_clicking()


    def bow(self):
        if self.click_thread.bow_running:
            logging.info("=>Stopping click for bow\n")
            self.bow_btn.configure(bg=self.btn_bg_unactive_color)
            self.click_thread.bow_stop_clicking()
        else:
            logging.info("=>Starting click for bow")
            self.bow_btn.configure(bg=self.btn_bg_active_color)
            self.click_thread.stop_other_runs()
            self.click_thread.bow_start_clicking()


    def sword(self):
        if self.click_thread.sword_running:
            logging.info("=>Stopping click for sword\n")
            self.sword_btn.configure(bg=self.btn_bg_unactive_color)
            self.click_thread.sword_stop_clicking()
        else:
            logging.info("=>Starting click for sword")
            self.sword_btn.configure(bg=self.btn_bg_active_color)
            self.click_thread.stop_other_runs()
            time.sleep(INPUT_SLEEP)
            self.click_thread.sword_start_clicking()


    def pickaxe(self):
        if self.click_thread.pickaxe_running:
            logging.info("=>Stopping click for pickaxe\n")
            self.pickaxe_btn.configure(bg=self.btn_bg_unactive_color)
            self.click_thread.pickaxe_stop_clicking()

            self.mouse.release(Button.left)
            self.keyboard.release("w")
        else:
            logging.info("=>Starting click for pickaxe")
            self.pickaxe_btn.configure(bg=self.btn_bg_active_color)
            self.click_thread.stop_other_runs()
            self.click_thread.pickaxe_start_clicking()

            time.sleep(INPUT_SLEEP)
            self.mouse.press(Button.left)
            self.keyboard.press("w")


    def create(self):
        # Root window title
        self.root.title("Autoclicker")

        # Root dimension
        self.root.geometry(f'{self.window_width}x{self.window_height}+{self.window_x}+{self.window_y}')

        self.sword_btn   = tkinter.Button(self.root, text = "Start/Stop Auto Sword (F9)" ,    fg = "black", bg = self.btn_bg_unactive_color, command=self.sword)
        self.trident_btn = tkinter.Button(self.root, text = "Start/Stop Auto Trident (F10)" , fg = "black", bg = self.btn_bg_unactive_color, command=self.trident)
        self.pickaxe_btn = tkinter.Button(self.root, text = "Start/Stop Auto Pickaxe (F11)" , fg = "black", bg = self.btn_bg_unactive_color, command=self.pickaxe)
        self.bow_btn     = tkinter.Button(self.root, text = "Start/Stop Auto Bow (F12)",      fg = "black", bg = self.btn_bg_unactive_color, command=self.bow)

        self.sword_btn.place(bordermode=tkinter.INSIDE, height=self.btn_height, width=self.btn_width, x = 100, y= 0)
        self.trident_btn.place(bordermode=tkinter.INSIDE, height=self.btn_height, width=self.btn_width, x = 100, y= 100)
        self.pickaxe_btn.place(bordermode=tkinter.INSIDE, height=self.btn_height, width=self.btn_width, x = 100, y= 200)
        self.bow_btn.place(bordermode=tkinter.INSIDE, height=self.btn_height, width=self.btn_width, x = 100, y= 300)


    def on_press(self, key):
        logging.debug(f"Key Pressed: {key}")

        if key == self.trident_start_stop_key:
            self.trident()
        elif key == self.bow_start_stop_key:
            self.bow()
        elif key == self.sword_start_stop_key:
            self.sword()
        elif key == self.pickaxe_start_stop_key:
            self.pickaxe()
        elif key == self.stop_key:
            logging.info("PRESSED: stop_key")
            self.root.destroy()


    def run(self):
        # Start keyboard listener
        listener = Listener(on_press = self.on_press)
        listener.start()

        # Execute Tkinter
        self.root.mainloop()

        # Exit click_thread after mainloop has finish
        self.click_thread.exit()
