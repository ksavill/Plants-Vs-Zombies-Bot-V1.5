# pause_check.py

import time
from element_locator import SelGui, ElementNotFound

sel_gui = SelGui("Plants vs. Zombies")

class pause_check:
    @staticmethod
    def pause_menus():
        """
        Checks if pause menus are open and pauses the script until they are closed.
        """
        # Check for the main pause menu
        try:
            print("Checking for main pause menu...")
            sel_gui.find(r'assets/pause_menus/menu.png', confidence_value=0.9, timeout=0.01)
            print("Main pause menu detected. Pausing automation...")
            while True:
                try:
                    sel_gui.find(r'assets/pause_menus/menu.png', confidence_value=0.9, timeout=0.01)
                    time.sleep(1)  # Wait before rechecking
                except ElementNotFound:
                    print("Main pause menu no longer detected. Resuming automation.")
                    break
        except ElementNotFound:
            print("No main pause menu detected.")

        # Check for the game paused popup
        try:
            print("Checking for game paused popup...")
            sel_gui.find(r'assets/pause_menus/game_paused.png', confidence_value=0.9, timeout=0.01)
            print("Game paused popup detected. Pausing automation...")
            while True:
                try:
                    sel_gui.find(r'assets/pause_menus/game_paused.png', confidence_value=0.9, timeout=0.01)
                    time.sleep(1)  # Wait before rechecking
                except ElementNotFound:
                    print("Game paused popup no longer detected. Resuming automation.")
                    break
        except ElementNotFound:
            print("No game paused popup detected.")
