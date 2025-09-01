import pyautogui
import keyboard
import pygame
import time
import sys

from colorama import Fore, init
from typing import Optional

init(autoreset=True)


# --- SETTINGS ---
ENCHANT_IMAGE = "image/pic.png"
CONFIDENCE_LEVEL = 0.8
KEYBOARD_CLICK_DELAY = 0.5
LOOP_DELAY = 0.2
SWITCH_GAME_DELAY = 8

# In-game controls
BREAK_BLOCK_KEY = 'left'
PLACE_BLOCK_KEY = 'right'
INVENTORY_KEY = 'e'
LEFT_MOVE = 'd'
RIGHT_MOVE = 'a'

# Axes dictionary + 0.2
AXE_DICT = {
            "WAE0H0": 2.10, "WAE0H1": 1.80, "WAE0H2": 1.55,
            "WAE1H0": 1.15, "WAE1H1": 1.00, "WAE1H2": 0.90,
            "WAE2H0": 0.75, "WAE2H1": 0.65, "WAE2H2": 0.60,
            "WAE3H0": 0.55, "WAE3H1": 0.50, "WAE3H2": 0.45,
            "WAE4H0": 0.40, "WAE4H1": 0.40, "WAE4H2": 0.35,
            "WAE5H0": 0.35, "WAE5H1": 0.35, "WAE5H2": 0.30,

            "SAE0H0": 1.15, "SAE0H1": 1.00, "SAE0H2": 0.90,
            "SAE1H0": 0.85, "SAE1H1": 0.75, "SAE1H2": 0.65,
            "SAE2H0": 0.65, "SAE2H1": 0.55, "SAE2H2": 0.50,
            "SAE3H0": 0.50, "SAE3H1": 0.45, "SAE3H2": 0.40,
            "SAE4H0": 0.40, "SAE4H1": 0.35, "SAE4H2": 0.35,
            "SAE5H0": 0.35, "SAE5H1": 0.35, "SAE5H2": 0.30,

            "IAE0H0": 0.85, "IAE0H1": 0.75, "IAE0H2": 0.65,
            "IAE1H0": 0.70, "IAE1H1": 0.60, "IAE1H2": 0.55,
            "IAE2H0": 0.55, "IAE2H1": 0.50, "IAE2H2": 0.45,
            "IAE3H0": 0.45, "IAE3H1": 0.40, "IAE3H2": 0.40,
            "IAE4H0": 0.40, "IAE4H1": 0.35, "IAE4H2": 0.35,
            "IAE5H0": 0.35, "IAE5H1": 0.30, "IAE5H2": 0.30,

            "DAE0H0": 0.70, "DAE0H1": 0.60, "DAE0H2": 0.55,
            "DAE1H0": 0.60, "DAE1H1": 0.55, "DAE1H2": 0.50,
            "DAE2H0": 0.50, "DAE2H1": 0.45, "DAE2H2": 0.45,
            "DAE3H0": 0.45, "DAE3H1": 0.40, "DAE3H2": 0.35,
            "DAE4H0": 0.35, "DAE4H1": 0.35, "DAE4H2": 0.35,
            "DAE5H0": 0.35, "DAE5H1": 0.30, "DAE5H2": 0.30,

            "NAE0H0": 0.65, "NAE0H1": 0.55, "NAE0H2": 0.50,
            "NAE1H0": 0.55, "NAE1H1": 0.50, "NAE1H2": 0.45,
            "NAE2H0": 0.50, "NAE2H1": 0.45, "NAE2H2": 0.40,
            "NAE3H0": 0.40, "NAE3H1": 0.40, "NAE3H2": 0.35,
            "NAE4H0": 0.35, "NAE4H1": 0.35, "NAE4H2": 0.35,
            "NAE5H0": 0.35, "NAE5H1": 0.30, "NAE5H2": 0.30,

            "GAE0H0": 0.55, "GAE0H1": 0.50, "GAE0H2": 0.45,
            "GAE1H0": 0.50, "GAE1H1": 0.45, "GAE1H2": 0.40,
            "GAE2H0": 0.45, "GAE2H1": 0.40, "GAE2H2": 0.40,
            "GAE3H0": 0.40, "GAE3H1": 0.35, "GAE3H2": 0.35,
            "GAE4H0": 0.35, "GAE4H1": 0.35, "GAE4H2": 0.30,
            "GAE5H0": 0.30, "GAE5H1": 0.30, "GAE5H2": 0.30
            }


# Enchantments dictionary
ENCHANT_DICT = {
                "aqua affinity": 1,
                "bane of arthropods": 5,
                "blast protection": 4,
                "breach": 4,
                "channeling": 1,
                "curse of binding": 1,
                "curse of vanishing": 1,
                "density": 5,
                "depth strider": 3,
                "efficiency": 5,
                "feather falling": 4,
                "fire aspect": 2,
                "fire protection": 4,
                "flame": 1,
                "fortune": 3,
                "frost walker": 2,
                "impaling": 5,
                "infinity": 1,
                "knockback": 2,
                "looting": 3,
                "loyalty": 3,
                "luck of the sea": 3,
                "lure": 3,
                "mending": 1,
                "multishot": 1,
                "piercing": 4,
                "power": 5,
                "projectile protection": 4,
                "protection": 4,
                "punch": 2,
                "quick charge": 3,
                "respiration": 3,
                "riptide": 3,
                "sharpness": 5,
                "silk touch": 1,
                "smite": 5,
                "sweeping edge": 3,
                "thorns": 3,
                "unbreaking": 3,
                }

UNOBTAINABLE_ENCHANTS = {"wind burst", "soul speed", "swift sneak"}

# Minecraft slots list
MINECRAFT_SLOTS = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


# ------------------- UTILITIES -------------------

def get_axe_delay(axe_code: str) -> Optional[float]:
    """Get breaking delay based on axe and haste level."""
    delay = AXE_DICT.get(axe_code)
    if delay is None:
        print(Fore.RED + f"❌ Axe code '{axe_code}' not found in AXE_DICT.")
        return None
    return delay


def image_found(image_path):
    """Locate an image on screen, return location or None."""
    try:
        return pyautogui.locateOnScreen(image_path, confidence=CONFIDENCE_LEVEL)
    except FileNotFoundError:
        print(Fore.RED + f"Error: Image file not found at '{image_path}'")
        sys.exit()
    except Exception:
        return None


def image_exists(image_path):
    """Check if image exists on screen."""
    return image_found(image_path) is not None


def click_mouse(button, delay):
    pyautogui.mouseDown(button=button)
    time.sleep(delay)
    pyautogui.mouseUp(button=button)


def click_keyboard(key, delay):
    pyautogui.keyDown(key)
    time.sleep(delay)
    pyautogui.keyUp(key)


def stop_if_requested():
    if keyboard.is_pressed('esc'):
        print(Fore.YELLOW + "\n⛔ Script stopped by user request.")
        sys.exit()


# ------------------- ENCHANT CHECK -------------------

def enchant_found(enchant_dict):
    """Check if desired enchantments are found in villager trades."""
    location = image_found(ENCHANT_IMAGE)
    if not location:
        return False

    pyautogui.moveTo(pyautogui.center(location), duration=0.25)

    for enchant, lvl in enchant_dict.items():
        path_ = f"image/{enchant}/{enchant}.png"

        if ENCHANT_DICT[enchant] > 1:
            if image_exists(path_):
                level_path = f"image/{enchant}/lvl/lvl_{lvl}.png"
                if image_exists(level_path):
                    pygame.mixer.init()
                    pygame.mixer.music.load("sound/success.mp3")
                    pygame.mixer.music.play()

                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)

                    print(Fore.GREEN + f"\n✅ Found enchantment: {enchant.title()} {lvl}")
                    return True
        else:
            if image_exists(path_):
                pygame.mixer.init()
                pygame.mixer.music.load("sound/success.mp3")
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)

                print(Fore.GREEN + f"\n✅ Found enchantment: {enchant.title()}")
                return True

    return False


# ------------------- MAIN LOGIC -------------------

def get_user_enchants():
    """Get desired enchantments from user input."""
    job_block_hotbar = input("Which hotbar slot is your lectern in? (1-9): ").lower()
    tool_hotbar = input("Which hotbar slot is your axe in? (1-9): ").lower()
    if job_block_hotbar not in MINECRAFT_SLOTS or tool_hotbar not in MINECRAFT_SLOTS:
        print("Valid Minecraft slots are 1, 2, 3, ..., 9.")
        return {}, None, None, None

    if job_block_hotbar == tool_hotbar:
        print("Your lectern slot cannot be the same as your axe slot!")
        return {}, None, None, None

    axe_input = input("Enter your axe code (e.g., WAE0H0): ")
    delay = get_axe_delay(axe_input)
    if delay is None:
        return {}, None, None, None

    enchant_dict_input = {}
    try:
        number_enchant = int(input("Enter the number of enchantments: "))
    except ValueError:
        print(Fore.RED + "❌ Error: Please enter a valid integer.")
        return {}, None, None, None

    for i in range(number_enchant):
        enchant_name = input(f"Enter enchantment #{i+1} (or type 'exit' to quit): ").lower()
        if enchant_name == "exit":
            break

        if enchant_name in UNOBTAINABLE_ENCHANTS:
            print(Fore.RED + "❌ This enchantment cannot be obtained from villagers.")
            continue

        if enchant_name not in ENCHANT_DICT:
            print(Fore.RED + f"❌ Enchantment '{enchant_name}' not found in dictionary.")
            continue

        if ENCHANT_DICT[enchant_name] != 1:
            try:
                lvl = int(input(f"Enter the desired level for {enchant_name}: "))
            except ValueError:
                print(Fore.RED + "❌ Invalid level input.")
                continue

            max_lvl = ENCHANT_DICT[enchant_name]
            if lvl < 1 or lvl > max_lvl:
                print(Fore.RED + f"❌ Level must be between 1 and {max_lvl}.")
                continue
        else:
            lvl = 1

        enchant_dict_input[enchant_name] = lvl

    return enchant_dict_input, delay, job_block_hotbar, tool_hotbar


def automation_loop(enchant_dict, actions_delay, lectern_hotbar, axe_hotbar):
    """Main automation loop."""
    print(Fore.CYAN + f"\n🔍 Starting search for: {enchant_dict}")
    print(Fore.CYAN + f"You have {SWITCH_GAME_DELAY} seconds to switch to the game...")
    print(Fore.YELLOW + "Press ESC anytime to stop.")
    time.sleep(SWITCH_GAME_DELAY)

    click_keyboard(axe_hotbar, 0.2)

    while True:
        stop_if_requested()

        # Replace lectern
        click_keyboard(LEFT_MOVE, KEYBOARD_CLICK_DELAY)
        click_mouse(BREAK_BLOCK_KEY, actions_delay)
        click_keyboard(lectern_hotbar, 0.05)
        click_mouse(PLACE_BLOCK_KEY, 0.05)
        click_keyboard(RIGHT_MOVE, KEYBOARD_CLICK_DELAY)

        time.sleep(1.00)

        click_mouse(PLACE_BLOCK_KEY, 0.05)

        # Check enchantments
        if enchant_found(enchant_dict):
            print(Fore.GREEN + "\n🎉 Desired enchantment found! Stopping script.")
            return

        # Reset inventory
        click_keyboard(INVENTORY_KEY, 0.05)
        click_keyboard(axe_hotbar, 0.05)

        time.sleep(LOOP_DELAY)


def main():
    enchant_dict, actions_delay, lectern_hotbar, axe_hotbar = get_user_enchants()
    if not enchant_dict:
        print(Fore.YELLOW + "⚠️ No valid enchantments entered. Exiting.")
        return
    automation_loop(enchant_dict, actions_delay, lectern_hotbar, axe_hotbar)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⛔ Program interrupted by user.")
    except Exception as e:
        print(Fore.RED + f"\n❌ Unexpected error: {e}")
