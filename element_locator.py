import pyautogui
import pygetwindow as gw
import time
from typing import Optional, Tuple, Union

class ElementNotFound(Exception):
    """Exception raised when a UI element is not found within the specified timeout."""
    pass

class SelGui:
    def __init__(self, window_title: str, strict: bool = True):
        """
        Initialize with the title of the target application window.
        
        Parameters:
            window_title (str): The title of the target window.
            strict (bool): If True, methods will raise exceptions on failure.
                            If False, methods will return False on failure.
                            Defaults to True.
        """
        self.window_title = window_title
        self.strict = strict
        self.window = self.get_window()
        if not self.window:
            if self.strict:
                raise ValueError(f"Window with title '{self.window_title}' not found.")
            else:
                # Handle the case where window is not found
                pass  # You might want to log this or handle it as needed
    
    def get_window(self) -> Optional[gw.Window]:
        """
        Retrieve the window object based on the title.
        """
        windows = gw.getWindowsWithTitle(self.window_title)
        if windows:
            return windows[0]  # Assuming the first match is the target
        return None
    
    def get_window_region(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Get the current region of the window as (left, top, width, height).
        """
        self.window = self.get_window()
        if self.window and self.window.isActive:
            return (self.window.left, self.window.top, self.window.width, self.window.height)
        return None
    
    def activate_window(self) -> bool:
        """
        Bring the target window to the foreground.
        
        Returns:
            bool: True if the window was activated successfully, False otherwise.
        """
        if self.window:
            try:
                self.window.activate()
                time.sleep(0.5)  # Wait for the window to become active
                return True
            except Exception as e:
                if self.strict:
                    raise e
                else:
                    print(f"Failed to activate window '{self.window_title}': {e}")
                    return False
        else:
            if self.strict:
                raise ValueError(f"Window '{self.window_title}' not found.")
            else:
                print(f"Window '{self.window_title}' not found.")
                return False

    def click_in_place(self, clicks: int, interval: float = 0.0) -> None:
        """
        Perform a click at the current mouse position.
        
        Parameters:
            
            clicks (int): The number of clicks to perform.
            interval (float): The time delay between clicks.
            
        Returns:
            None
        """
        pyautogui.click(clicks=clicks, interval=interval)
    
    def click(self, element: str, confidence_value: float = 0.9, timeout: float = 5.0) -> Union[Tuple[int, int], bool]:
        """
        Locate the element within the window region and perform a click.
        Returns False if the element is not found within the timeout and `strict` is False.
        
        Parameters:
            element (str): The image file of the UI element to locate.
            confidence_value (float): Confidence level for image matching.
            timeout (float): Time to wait for the element to appear.
        
        Returns:
            None if clicked successfully, False otherwise.
        """
        if not self.activate_window():
            return False if not self.strict else None  # If strict, exceptions are already handled
        
        region = self.get_window_region()
        if not region:
            if self.strict:
                raise ElementNotFound(f"Window '{self.window_title}' is not active or not found.")
            else:
                print(f"Window '{self.window_title}' is not active or not found.")
                return False
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            location = pyautogui.locateCenterOnScreen(element, confidence=confidence_value, region=region)
            if location:
                pyautogui.moveTo(location)
                pyautogui.click()
                print(f"Clicked element '{element}' at coordinates {location}.")
                return location
            time.sleep(0.5)  # Wait before retrying
        
        if self.strict:
            raise ElementNotFound(f"Element '{element}' not found within the timeout period.")
        else:
            print(f"Element '{element}' not found within the timeout period.")
            return False
    
    def find(self, element: str, confidence_value: float = 0.9, timeout: float = 5.0) -> Union[Tuple[int, int], bool]:
        """
        Locate the element within the window region and return its coordinates.
        Returns False if the element is not found within the timeout and `strict` is False.
        
        Parameters:
            element (str): The image file of the UI element to locate.
            confidence_value (float): Confidence level for image matching.
            timeout (float): Time to wait for the element to appear.
        
        Returns:
            Tuple[int, int] with the coordinates if found, False otherwise.
        """
        
        if not self.activate_window():
            return False if not self.strict else None  # If strict, exceptions are already handled
        
        region = self.get_window_region()
        if not region:
            if self.strict:
                raise ElementNotFound(f"Window '{self.window_title}' is not active or not found.")
            else:
                print(f"Window '{self.window_title}' is not active or not found.")
                return False
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            location = pyautogui.locateCenterOnScreen(element, confidence=confidence_value, region=region)
            if location:
                print(f"Element '{element}' found at coordinates {location}.")
                return location
            time.sleep(0.5)  # Wait before retrying
        
        if self.strict:
            raise ElementNotFound(f"Element '{element}' not found within the timeout period.")
        else:
            print(f"Element '{element}' not found within the timeout period.")
            return False
    
    def current_coords(self) -> Tuple[int, int]:
        """
        Get the current mouse coordinates.
        """
        return pyautogui.position()
    
    def goto_coords(self, x: int, y: int, duration: float = 0.5) -> bool:
        """
        Move the mouse to the specified (x, y) screen coordinates.
        
        Parameters:
            x (int): The x-coordinate on the screen.
            y (int): The y-coordinate on the screen.
            duration (float): Time taken to move the mouse to the coordinates.
        
        Returns:
            bool: True if the mouse moved successfully, False otherwise.
        """
        try:
            pyautogui.moveTo(x, y, duration=duration)
            print(f"Moved mouse to coordinates ({x}, {y}).")
            return True
        except Exception as e:
            if self.strict:
                raise e
            else:
                print(f"Failed to move mouse to ({x}, {y}): {e}")
                return False
