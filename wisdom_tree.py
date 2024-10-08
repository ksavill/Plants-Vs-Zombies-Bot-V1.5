import time
from pause_menus import pause_check
import dave_shop
from element_locator import SelGui

class WisdomTreeHandler:
    def __init__(self, sel_gui: SelGui):
        self.sel_gui = sel_gui
        self.highest_plant_index = 1  # Initialize to 1
    
    def buy_wisdom_fertilizer(self) -> bool:
        """
        Handles the purchase of wisdom fertilizer from Crazy Dave's shop.
        Returns True if purchase was successful, False otherwise.
        """
        if self.sel_gui.click('assets/dave_shop/zen_garden_shop_button.png', 0.9):
            dave_shop.Dave_Store.buy_request('wisdom_fertilizer', quantity=10)
            # Verify if the purchase was successful
            if self.sel_gui.find('assets/dave_shop/wisdom_fertilizer_empty.png', 0.9):
                print("Purchase failed: Insufficient funds.")
                return False
            print("Wisdom fertilizer purchased successfully.")
            return True
        print("Failed to click the shop button.")
        return False
    
    def select_plant(self):
        """
        Attempts to click on available plant slots in order of priority, 
        starting from the highest plant index previously clicked.
        """
        plant_images = [
            ('assets/wisdom_tree/plant_1.png', 0.9),
            ('assets/wisdom_tree/plant_2.png', 0.9),
            ('assets/wisdom_tree/plant_3.png', 0.95),
            ('assets/wisdom_tree/plant_4.png', 0.9),
            ('assets/wisdom_tree/plant_5.png', 0.9),
        ]
        
        # Start checking from the highest_plant_index - 1 (0-based indexing)
        for idx in range(self.highest_plant_index - 1, len(plant_images)):
            image, confidence = plant_images[idx]
            if self.sel_gui.click(image, confidence, timeout=0.25):
                current_plant = idx + 1  # Convert to 1-based index
                if current_plant > self.highest_plant_index:
                    self.highest_plant_index = current_plant
                    print(f"Updated highest plant index to: {self.highest_plant_index}")
                else:
                    print(f"Clicked plant_{current_plant}.")
                return  # Exit after successful click
        # Optionally handle the case where no plant was clicked
        print("No plant slots available to click.")
    
    def wisdom_tree(self):
        while True:
            pause_check.pause_menus()
            
            # Attempt to click the wisdom fertilizer
            if not self.sel_gui.click('assets/wisdom_tree/wisdom_fertilizer.png', 0.9, timeout=0.01):
                # If wisdom fertilizer is not available, check if it's empty
                if self.sel_gui.find('assets/dave_shop/wisdom_fertilizer_empty.png', 0.9, timeout=0.01):
                    # Attempt to purchase wisdom fertilizer
                    purchase_success = self.buy_wisdom_fertilizer()
                    if not purchase_success:
                        print("Exiting wisdom_tree loop due to purchase failure.")
                        break  # Exit the loop if purchase failed
            
            # Attempt to select a plant
            self.select_plant()
            
            # Optional: Add a short delay to prevent rapid looping
            time.sleep(0.5)
        
        # After exiting the loop, attempt to return to the main menu
        if self.sel_gui.click('assets/main_menu_top_right.png', 0.9):
            print("Returned to the main menu.")
            time.sleep(2)
        else:
            print("Failed to return to the main menu.")

def main():
    sel_gui = SelGui("Plants vs. Zombies")
    wisdom_handler = WisdomTreeHandler(sel_gui)
    wisdom_handler.wisdom_tree()

# Example Usage:
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
