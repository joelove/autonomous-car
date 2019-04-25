import time
import config

from joystick import Joystick
from threading import Thread
from multiprocessing import Queue


class Controller:
    def __init__(self):
        self.joystick = Joystick()
        self.joystick_state = Queue()


    def initialize_joystick(self):
        self.joystick.init()

        self.thread = Thread(target=self.joystick.begin_polling, args=(self.joystick_state,))
        self.thread.daemon = True
        self.thread.start()


    def query_joystick_state(self, state_handler):
        joystick_state = None

        while not self.joystick_state.empty():
            joystick_state = self.joystick_state.get_nowait()

        if joystick_state:
            state_handler(joystick_state)


    def read(self, state_handler):
        self.initialize_joystick()

        joystick_state = {}
        tick_length = 1.0 / config.DRIVE_LOOP_HZ

        while True:
            start_time = time.time()
            self.query_joystick_state(state_handler)
            time.sleep(tick_length - ((time.time() - start_time) % tick_length))
