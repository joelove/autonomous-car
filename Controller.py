import time
import config

from threading import Thread
from multiprocessing import Queue

from Joystick import Joystick


class Controller:
    def __init__(self):
        self.joystick = Joystick()
        self.joystick_state = Queue()
        self.joystick.init()

        self.thread = Thread(target=self.joystick.begin_polling, args=(self.joystick_state,))
        self.thread.daemon = True
        self.thread.start()
