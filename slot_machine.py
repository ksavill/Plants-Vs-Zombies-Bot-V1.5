import time
from pause_menus import pause_check
from element_locator import SelGui, ElementNotFound

# Initialize SelGui with the game window title
sel_gui = SelGui("Plants vs. Zombies")

class PlacePlant:
    def __init__(self, sel_gui: SelGui):
        self.sel_gui = sel_gui
        self.columns = range(1, 10)  # Columns 1 through 9
        self.rows = range(1, 6)      # Rows 1 through 5
        self.plant_types = {
            'sunflower': 'assets/special_items/sun.png',
            'walnut': 'assets/slot_machine/walnut.png',
            'peashooter': 'assets/slot_machine/peashooter.png',
            'frozen_peashooter': 'assets/slot_machine/frozen_peashooter.png'
        }
        self.retry_limit = 3  # Number of retries for finding a plant

    def try_again_prompt(self):
        """Attempts to click the 'Try Again' prompt if it appears."""
        try:
            self.sel_gui.click(r'assets/slot_machine/try_again.png', 0.9, timeout=0.25)
            print("Clicked 'Try Again' prompt.")
        except ElementNotFound:
            print("'Try Again' prompt not found.")

    def find_plants(self):
        """Finds available plants and attempts to place them on the grid."""
        self.try_again_prompt()
        print("Starting to find and place plants.")

        for plant_name, plant_image in self.plant_types.items():
            print(f"Attempting to find {plant_name}.")
            for attempt in range(1, self.retry_limit + 1):
                try:
                    self.sel_gui.click(plant_image, 0.9, timeout=0.25)
                    print(f"{plant_name.capitalize()} found. Attempting to place.")
                    self.place_plant()
                    break  # Move to the next plant after successful placement
                except ElementNotFound:
                    print(f"Attempt {attempt}: {plant_name.capitalize()} not found.")
                    if attempt == self.retry_limit:
                        print(f"Failed to find {plant_name.capitalize()} after {self.retry_limit} attempts.")
            else:
                continue  # Continue to the next plant if current plant not found

    def place_plant(self):
        """Attempts to place a plant in the available grid slots."""
        for column in self.columns:
            for row in self.rows:
                position_image = f'assets/slot_machine/c{column}r{row}.png'
                try:
                    self.sel_gui.click(position_image, 0.9, timeout=0.25)
                    print(f"Placed plant at column {column}, row {row}.")
                    return  # Exit after successfully placing the plant
                except ElementNotFound:
                    print(f"Position c{column}r{row} not available.")
                    continue  # Try the next row in the same column
        print("No available spots to place the plant.")

def try_again_prompt():
    """Attempts to click the 'Try Again' prompt outside the PlacePlant class."""
    try:
        sel_gui.click(r'assets/slot_machine/try_again.png', 0.9, timeout=0.25)
        print("Clicked 'Try Again' prompt.")
    except ElementNotFound:
        print("'Try Again' prompt not found.")

def slot_machine(win_count: int):
    """Automates the slot machine minigame until a specified win count is reached."""
    i = 0
    place_plant = PlacePlant(sel_gui)

    while True:
        if i >= win_count:
            print(f"Automation has won {i} times, exiting minigame automation to next major task.")
            time.sleep(10)
            break

        # Start a new game
        try:
            sel_gui.click(r'assets/slot_machine/slot_machine_minigame.png', 0.9, timeout=0.25)
            sel_gui.click(r'assets/slot_machine/new_game.png', 0.9, timeout=0.25)
            time.sleep(0.25)
            sel_gui.click(r'assets/slot_machine/new_game_1.png', 0.9, timeout=0.25)
            print("Started a new slot machine minigame.")
        except ElementNotFound:
            print("Failed to start a new slot machine minigame.")
            continue  # Skip to the next iteration if game start fails

        pause_check.pause_menus()

        # Attempt to find and place plants
        place_plant.find_plants()

        pause_check.pause_menus()

        # Attempt to click chocolate
        try:
            sel_gui.click(r'assets/slot_machine/chocolate.png', 0.9, timeout=0.25)
            print("Clicked chocolate.")
        except ElementNotFound:
            print("Chocolate not found.")

        pause_check.pause_menus()

        # Attempt to click present
        try:
            sel_gui.click(r'assets/special_items/present_box.png', 0.9, timeout=0.25)
            print("Clicked present.")
        except ElementNotFound:
            print("Present not found.")
        
        pause_check.pause_menus()

        # Attempt to click trophy bag
        try:
            sel_gui.click(r'assets/slot_machine/trophybag.png', 0.9, timeout=0.25)
            time.sleep(1)
            try:
                sel_gui.click(r'assets/slot_machine/trophybag.png', 0.9, timeout=0.25)
            except ElementNotFound:
                pass
            print("Trophy found and clicked, level ended.")
            i += 1
            print(f"Current win count: {i}")
        except ElementNotFound:
            try:
                sel_gui.click(r'assets/slot_machine/trophybag.png', 0.9, timeout=0.25)
            except ElementNotFound:
                pass

        pause_check.pause_menus()

        # Attempt to click diamond
        try:
            sel_gui.click(r'assets/slot_machine/diamond.png', 0.9, timeout=0.25)
            print("Clicked diamond.")
        except ElementNotFound:
            print("Did not find a diamond.")

        pause_check.pause_menus()

        # Attempt to click sunflower
        try:
            sel_gui.click(r'assets/special_items/sun.png', 0.8, timeout=0.25)
            sel_gui.click_in_place(clicks=5, interval=0.1)
            print("Clicked sunflower multiple times.")
            time.sleep(0.1)
        except ElementNotFound:
            print("Sunflower not found. Attempting to interact with the spin handle.")
            try:
                # Assuming 'current_coords' is a method to get current mouse coordinates
                # If not defined, implement it or remove its usage
                mousex, mousey = sel_gui.current_coords()
                print("Finding handle.")
                while True:
                    try:
                        sel_gui.click(r'assets/slot_machine/spin_handle.png', 0.8, timeout=0.25)
                        print("Clicked Spin Handle.")
                        sel_gui.goto_coords(mousex, mousey)
                    except ElementNotFound:
                        print("Spin handle not found.")
                        break

                    j = 0
                    while True:
                        try_again_prompt()
                        try:
                            print("Finding sunflower.")
                            sel_gui.click(r'assets/special_items/sun.png', 0.8, timeout=0.25)
                            sel_gui.click_in_place(clicks=5, interval=0.1)
                            print("Clicked sunflower multiple times.")
                            j += 1
                        except ElementNotFound:
                            break

                    try:
                        sel_gui.find(r'assets/slot_machine/spin_again.png', 0.7, timeout=0.25)
                        print("'Spin Again' text detected, clicking handle again...")
                    except ElementNotFound:
                        print("'Spin Again' text not detected, moving to place plants.")
                        break

                # After handling spin, attempt to place plants again
                place_plant.find_plants()
            except AttributeError:
                print("'current_coords' method not defined in SelGui. Skipping spin handle interaction.")
            except Exception as e:
                print(f"An unexpected error occurred while interacting with spin handle: {e}")

        # Optional: Add a short delay to prevent rapid looping
        time.sleep(0.5)

    # After exiting the loop, attempt to return to the main menu
    try:
        sel_gui.click(r'assets/main_menu/back_to_main_menu_bottom_left.png', 0.9, timeout=0.25)
        print("Returned to the main menu.")
    except ElementNotFound:
        print("Failed to return to the main menu.")

def main():
    win_count = 5  # Example win count; adjust as needed
    try:
        slot_machine(win_count)
    except KeyboardInterrupt:
        print("Keyboard interruption detected. Stopping automation.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()