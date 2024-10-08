import dearpygui.dearpygui as dpg
import time
import threading
import os
import zipfile

import wisdom_tree
import slot_machine
import extended_zen_garden

from element_locator import SelGui

SelGui = SelGui("Plants vs. Zombies")

class PVZAutomationGUI:
    def __init__(self):
        if self.setup_assets():
            self.setup_gui()

    def setup_assets(self):
        """
        Checks if the ./assets directory exists. If not, but assets.zip exists, extracts it to create the directory.
        If neither ./assets nor assets.zip exists, returns False.
        """
        if not os.path.exists('./assets'):
            if os.path.exists('assets.zip'):
                print("Assets directory not found. Extracting assets.zip...")
                try:
                    with zipfile.ZipFile('assets.zip', 'r') as zip_ref:
                        zip_ref.extractall('./')
                    print("Assets extracted successfully.")
                    return True
                except zipfile.BadZipFile:
                    print("Error: assets.zip is corrupted.")
                    return False
            else:
                print("Error: assets directory and assets.zip not found.")
                return False
        return True

    def setup_gui(self):
        dpg.create_context()
        dpg.create_viewport(title='PVZ Automation Tool', width=850, height=500)
        dpg.setup_dearpygui()

        with dpg.window(
            label="Main Menu",
            tag="main_menu",
            width=850,
            height=500,
            on_close=self.on_main_menu_close  # Assigning the on_close callback
        ):
            dpg.add_text("Plants Vs. Zombies Main Automation Menu\n\n")
            dpg.add_text("Ensure the game is in windowed mode\nAND at the main menu with the big grave.\n\n")

            # Slot Machine Automation
            dpg.add_checkbox(label="Include Slot Machine Minigame Automation", tag="slot_machine")
            dpg.add_input_int(
                label="Number of Minigame Wins Before Moving to Next Task",
                width=300,
                tag="win_count",
                default_value=10
            )
            dpg.add_separator()

            # Zen Garden Automation
            dpg.add_text("\nExtended Zen Garden AFK Automation includes chocolate to snail and setting AFK hours.")
            dpg.add_checkbox(
                label="Include Extended Zen Garden AFK Automation (Chocolate Functionality Included)",
                tag="extended_zen_garden"
            )
            dpg.add_input_float(
                label="How Many Hours to AFK in Zen Garden?",
                tag="zen_garden_hours",
                default_value=1.0,
                min_value=0.1
            )
            dpg.add_separator()

            # Wisdom Tree Automation
            dpg.add_checkbox(label="Include Wisdom Tree Automation", tag="wisdom_tree")
            dpg.add_separator()

            # Start Button
            dpg.add_button(
                label="Start Game Automation",
                tag="start_automation",
                callback=self.start_automation
            )

        dpg.show_viewport()
        dpg.set_primary_window("main_menu", True)  # Optional: Set main_menu as the primary window
        dpg.start_dearpygui()
        dpg.destroy_context()

    def on_main_menu_close(self, sender, app_data, user_data):
        """
        Callback function triggered when the Main Menu window is closed.
        It schedules the window to be shown again after a short delay.
        """
        print("Main Menu closed. Reopening...")
        time.sleep(1)
        PVZAutomationGUI().reopen_main_menu()

    def reopen_main_menu(self):
        """
        Reopens the Main Menu window.
        """
        if not dpg.is_item_visible("main_menu"):
            dpg.show_item("main_menu")
            print("Main Menu has been reopened.")

    def start_automation(self, sender, app_data, user_data):
        """
        Callback for the 'Start Game Automation' button.
        Starts the automation process in a separate thread.
        """
        # Start the automation in a separate thread to keep the GUI responsive
        automation_thread = threading.Thread(target=self.run_automation, daemon=True)
        automation_thread.start()

    def run_automation(self):
        """
        Executes the automation tasks based on user selections.
        """
        # Retrieve values from the GUI
        slot_machine_automation = dpg.get_value("slot_machine")
        win_count = dpg.get_value("win_count")
        extended_zen_garden_automation = dpg.get_value("extended_zen_garden")
        zen_garden_hours = dpg.get_value("zen_garden_hours")
        wisdom_tree_automation = dpg.get_value("wisdom_tree")

        # Validate zen_garden_hours
        if zen_garden_hours < 0.001:
            zen_garden_hours = 1.0

        # Check if at least one automation option is selected
        if any([slot_machine_automation,
                extended_zen_garden_automation, wisdom_tree_automation]):
            print("At least one option is selected, proceeding with script")
            time.sleep(1)

            if slot_machine_automation:
                print("Starting Slot Machine Minigame Automation...")
                try:
                    SelGui.click(r'assets/main_menu/minigames.png', 0.9, timeout=20)
                    slot_machine.slot_machine(win_count)
                    print(f"Completed Slot Machine Automation with {win_count} wins.")
                except Exception as e:
                    print(f"Error in Slot Machine Automation: {e}")
                time.sleep(3)

            if extended_zen_garden_automation:
                print("Starting Extended Zen Garden AFK Automation...")
                try:
                    SelGui.click(r'assets/main_menu/zen_garden_icon.png', 0.9, timeout=20)
                    extended_time_seconds = zen_garden_hours * 3600
                    print(f"Total AFK time in Zen Garden: {zen_garden_hours} hours ({extended_time_seconds} seconds)")
                    extended_zen_garden.zen_garden(extended_time_seconds)
                    print("Completed Extended Zen Garden AFK Automation.")
                except Exception as e:
                    print(f"Error in Extended Zen Garden Automation: {e}")
                time.sleep(3)

            if wisdom_tree_automation:
                print("Starting Wisdom Tree Automation...")
                try:
                    SelGui.click(r'assets/main_menu/zen_garden_icon.png',.9, timeout=20)
                    time.sleep(1)
                    SelGui.click(r'assets/main_menu/golden_arrow.png',.9)
                    while True:
                        try:
                            SelGui.find(r'assets/wisdom_tree/wisdom_tree_text.png',.9)
                            break
                        except:
                            SelGui.click(r'assets/main_menu/golden_arrow.png',.9)
                    wisdom_tree.main()
                    print("Completed Wisdom Tree Automation.")
                except Exception as e:
                    print(f"Error in Wisdom Tree Automation: {e}")
                time.sleep(3)
        else:
            print("No automation options selected. Waiting for user to start again.")

if __name__ == '__main__':
    PVZAutomationGUI()