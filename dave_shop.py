# dave_shop.py

import time
from element_locator import SelGui

sel_gui = SelGui("Plants vs. Zombies", strict=False)

class Dave_Store:
    # Define valid items and their corresponding image paths
    VALID_ITEMS = {
        'fertilizer': 'assets/dave_shop/fertilizer.png',
        'bug_spray': 'assets/dave_shop/bug_spray.png',
        'crap_plant': None,  # Assuming no image needed
        'wisdom_fertilizer': 'assets/dave_shop/wisdom_fertilizer.png',
        'garden_rake': None  # Assuming no image needed
    }

    # Define other UI elements
    NEXT_BUTTON = 'assets/dave_shop/next.png'
    INSUFF_FUNDS_IMAGE = 'assets/dave_shop/insufficient_funds.png'
    OK_BUTTON = 'assets/dave_shop/ok.png'
    BUY_ITEM_PROMPT = 'assets/dave_shop/buy_item_prompt.png'
    YES_BUTTON = 'assets/dave_shop/yes.png'
    GO_BACK_BUTTON = 'assets/dave_shop/go_back.png'

    @classmethod
    def buy_request(cls, item: str, quantity: int = 1) -> dict:
        """
        Attempts to purchase the specified item from Crazy Dave's shop.

        Parameters:
            item (str): The name of the item to purchase.
            quantity (int): The number of items to purchase. Defaults to 1.

        Returns:
            dict: Result of the purchase attempt with keys:
                  - 'purchased' (int): Number of successfully purchased items.
                  - 'status' (str): 'successfully', 'partial', 'insufficient', 'invalid', 'unknown_error'.
        """
        if item not in cls.VALID_ITEMS:
            print(f"Invalid item buy request: '{item}'.")
            return {"purchased": 0, "status": "invalid"}

        successful_purchases = 0

        for i in range(quantity):
            print(f"\nAttempting to purchase '{item}' (Attempt {i+1}/{quantity}).")
            time.sleep(1)  # Reduced sleep time for efficiency; adjust as needed
            print("Initiating purchase sequence.")

            image_path = cls.VALID_ITEMS[item]
            if image_path:
                print(f"Locating '{item.replace('_', ' ')}' in the shop.")
                item_found = cls._find_and_click_item(image_path)
                if not item_found:
                    print(f"Unable to locate '{item}'. Stopping further purchase attempts.")
                    break  # Exit loop if the item cannot be found
                purchase_result = cls.insufficient_funds_check()
                if purchase_result == "successfully":
                    successful_purchases += 1
                    print(f"Successfully purchased '{item}' ({successful_purchases}/{quantity}).")
                elif purchase_result == "insufficient":
                    print("Insufficient funds detected. Stopping further purchase attempts.")
                    break  # Exit loop if there are insufficient funds
                else:
                    print("An unknown error occurred during the purchase. Stopping further attempts.")
                    break  # Exit loop on unknown errors
            else:
                print(f"Skipping purchase of '{item}' as no image path is provided.")
                break  # Exit loop if no image path is available

        # Determine overall status based on the number of successful purchases
        if successful_purchases == quantity:
            overall_status = "successfully"
        elif successful_purchases > 0:
            overall_status = "partial"
        else:
            overall_status = "failed"

        # Attempt to click 'Go Back' to exit the shop
        if sel_gui.click(cls.GO_BACK_BUTTON, confidence_value=0.9, timeout=0.25):
            print("Clicked 'Go Back' to exit the shop.")
        else:
            print("Failed to click 'Go Back'. It might already be closed or not present.")

        print(f"\nPurchase Summary: {successful_purchases}/{quantity} '{item}' purchased. Status: {overall_status}.")
        return {"purchased": successful_purchases, "status": overall_status}

    @classmethod
    def _find_and_click_item(cls, image_path: str) -> bool:
        """
        Helper method to locate and click an item. Navigates through the shop using the 'next' button
        if the item is not immediately found.

        Parameters:
            image_path (str): The file path to the item's image.

        Returns:
            bool: True if the item was found and clicked successfully, False otherwise.
        """
        max_pages = 5  # Prevent infinite loops; adjust based on shop size
        current_page = 1

        while current_page <= max_pages:
            location = sel_gui.find(image_path, confidence_value=0.9, timeout=2.0)
            if location:
                clicked = sel_gui.click(image_path, confidence_value=0.9, timeout=2.0)
                if clicked:
                    print(f"Clicked on '{image_path}' successfully.")
                    return True
                else:
                    print(f"Failed to click on '{image_path}'.")
                    return False
            else:
                print(f"'{image_path}' not found on page {current_page}. Attempting to navigate to the next page.")
                next_clicked = sel_gui.click(cls.NEXT_BUTTON, confidence_value=0.9, timeout=2.0)
                if not next_clicked:
                    print("Failed to click 'Next' button. Assuming end of shop pages.")
                    break  # Exit if 'Next' button cannot be clicked
                current_page += 1
                time.sleep(1)  # Wait for the next page to load

        print(f"Item '{image_path}' could not be found after navigating through {max_pages} pages.")
        return False

    @classmethod
    def insufficient_funds_check(cls) -> str:
        """
        Checks if the purchase was successful or if there were insufficient funds.

        Returns:
            str: Result of the funds check ('insufficient', 'successfully', 'unknown_error').
        """
        if sel_gui.find(cls.INSUFF_FUNDS_IMAGE, confidence_value=0.9, timeout=0.25):
            print("Insufficient funds detected.")
            if sel_gui.click(cls.OK_BUTTON, confidence_value=0.9, timeout=0.25):
                print("Clicked 'OK' to acknowledge insufficient funds.")
            else:
                print("Failed to click 'OK' on insufficient funds prompt.")
            return "insufficient"
        else:
            print("No insufficient funds prompt detected. Proceeding with purchase confirmation.")
            if sel_gui.find(cls.BUY_ITEM_PROMPT, confidence_value=0.9, timeout=0.25):
                if sel_gui.click(cls.YES_BUTTON, confidence_value=0.9, timeout=0.25):
                    print("Confirmed purchase by clicking 'Yes'.")
                else:
                    print("Failed to click 'Yes' on buy item prompt.")
                    return "unknown_error"
                return "successfully"
            else:
                print("Buy item prompt not detected. Unable to confirm purchase.")
                return "unknown_error"

if __name__ == '__main__':
    # Example Usage: Attempt to purchase 2 wisdom fertilizers
    result = Dave_Store.buy_request('wisdom_fertilizer', quantity=2)
    print(f"\nPurchase result: {result}")