import os
import sys
import subprocess
import platform
import psutil
import ctypes
import winreg

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def display_menu():
    print("Welcome to the Command Menu!")
    print("1. FPS Tweak")
    print("2. Keyboard and Mouse Delay Tweak")
    print("3. Controller Delay Tweak")
    print("4. Vibrant Color Settings")
    print("5. Exit")
    print()

def handle_input(choice):
    if choice == '1':
        fps_tweak()
    elif choice == '2':
        keyboard_mouse_delay_tweak()
    elif choice == '3':
        controller_delay_tweak()
    elif choice == '4':
        vibrant_color_settings()
    elif choice == '5':
        print("Exiting the program. Goodbye!")
        exit()
    else:
        print("Invalid choice, please try again.")
        input("Press Enter to continue...")

def fps_tweak():
    print("Running FPS Tweak...")
    print("This will adjust system settings to help increase FPS.")
    user_input = input("Press 'Enter' to continue or 'q' to cancel: ").strip().lower()
    if user_input == 'q':
        print("Exiting FPS Tweak.")
        return

    set_high_performance_power_plan()
    disable_visual_effects()
    disable_startup_programs()

    print("\nFPS Tweak Complete!")
    input("Press Enter to return to the menu...")

def set_high_performance_power_plan():
    print("\nAdjusting Power Settings to High Performance...")
    if platform.system() == "Windows":
        try:
            # Use the GUID for the High Performance power plan.
            high_performance_guid = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
            subprocess.run(["powercfg", "/setactive", high_performance_guid], check=True)
            print("Power plan set to High Performance.")
        except subprocess.CalledProcessError:
            print("Failed to change power plan to High Performance. Try running 'powercfg /l' to see available schemes.")
    else:
        print("Power plan tweak is only supported on Windows.")

def disable_visual_effects():
    print("\nDisabling Visual Effects for better performance automatically...")
    if platform.system() == "Windows":
        try:
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects"
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
            winreg.SetValueEx(key, "VisualFXSetting", 0, winreg.REG_DWORD, 2)
            winreg.CloseKey(key)
            print("Registry updated: 'VisualFXSetting' set to '2' (best performance).")
        except Exception as e:
            print(f"Failed to update registry for visual effects: {e}")

        try:
            SPI_SETANIMATION = 0x0049
            class ANIMATIONINFO(ctypes.Structure):
                _fields_ = [("cbSize", ctypes.c_uint), ("iMinAnimate", ctypes.c_int)]
            animation_info = ANIMATIONINFO(ctypes.sizeof(ANIMATIONINFO), 0)  # 0 disables animations
            result = ctypes.windll.user32.SystemParametersInfoA(
                SPI_SETANIMATION,
                animation_info.cbSize,
                ctypes.byref(animation_info),
                0
            )
            if result:
                print("System API updated: Window animations disabled.")
            else:
                print("Failed to disable window animations via SystemParametersInfo.")
        except Exception as e:
            print(f"Error disabling window animations: {e}")

        print("Visual effects now set for best performance. (A restart of Explorer or a logoff/logon may be required.)")
    else:
        print("Visual effects tweak is only supported on Windows.")

def disable_startup_programs():
    print("\nDisabling unnecessary startup programs...")
    # Placeholder: customize by adding process names you want to terminate.
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'SomeUnnecessaryApp.exe':
            try:
                proc.terminate()
                print(f"Terminated {proc.info['name']} from startup.")
            except psutil.NoSuchProcess:
                print(f"Could not terminate {proc.info['name']} as it no longer exists.")
    print("Checked startup programs (customize this function as needed).")

def keyboard_mouse_delay_tweak():
    print("\nTweaking Keyboard and Mouse Delays for better responsiveness...")
    try:
        kb_key_path = r"Control Panel\Keyboard"
        kb_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, kb_key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(kb_key, "KeyboardDelay", 0, winreg.REG_SZ, "0")
        winreg.SetValueEx(kb_key, "KeyboardSpeed", 0, winreg.REG_SZ, "31")
        winreg.CloseKey(kb_key)
        print("Keyboard settings updated: Delay set to 0, Speed set to 31.")
    except Exception as e:
        print(f"Failed to update keyboard settings: {e}")

    try:
        mouse_key_path = r"Control Panel\Mouse"
        mouse_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, mouse_key_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(mouse_key, "DoubleClickSpeed", 0, winreg.REG_SZ, "200")
        winreg.CloseKey(mouse_key)
        print("Mouse settings updated: DoubleClickSpeed set to 200 ms.")
    except Exception as e:
        print(f"Failed to update mouse settings: {e}")

    print("\nKeyboard and Mouse Delay Tweak Complete!")
    input("Press Enter to return to the menu...")

def is_controller_connected():
    """Check for a connected controller using XInput."""
    xinput = None
    # Try multiple common XInput DLLs.
    for dll in ["xinput1_4", "xinput1_3", "xinput9_1_0"]:
        try:
            xinput = ctypes.windll.LoadLibrary(dll + ".dll")
            break
        except Exception:
            continue
    if xinput is None:
        return False
    class XINPUT_STATE(ctypes.Structure):
        _fields_ = [("dwPacketNumber", ctypes.c_uint),
                    ("Gamepad", ctypes.c_ubyte * 16)]
    state = XINPUT_STATE()
    # Check all possible controller slots (0-3)
    for i in range(4):
        if xinput.XInputGetState(i, ctypes.byref(state)) == 0:
            return True
    return False

def controller_delay_tweak():
    print("\nChecking for controller...")
    if not is_controller_connected():
        print("No controller detected.")
    else:
        print("Controller detected. Tweaking controller delay...")
        try:
            controller_key_path = r"Control Panel\GameController"
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, controller_key_path)
            winreg.SetValueEx(key, "ControllerDelay", 0, winreg.REG_SZ, "0")
            winreg.CloseKey(key)
            print("Controller delay setting updated: Delay set to 0.")
        except Exception as e:
            print(f"Failed to update controller settings: {e}")
    input("Press Enter to return to the menu...")

def vibrant_color_settings():
    print("\nApplying Vibrant Color Settings...")
    nvidia_path = input("Enter the full path to the NVIDIA Control Panel executable (nvcplui.exe): ").strip()
    if not os.path.exists(nvidia_path):
        print("The provided path does not exist. Please verify the path and try again.")
        input("Press Enter to return to the menu...")
        return
    print("NVIDIA Control Panel found.")
    try:
        key_path = r"SOFTWARE\NVIDIA Corporation\Global\NVTweak"
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
        winreg.SetValueEx(key, "VibrantColor", 0, winreg.REG_SZ, "1")
        winreg.CloseKey(key)
        print("NVIDIA Color Settings adjusted: Vibrant and balanced colors applied.")
    except Exception as e:
        print(f"Failed to adjust NVIDIA Color Settings: {e}")
    input("Press Enter to return to the menu...")

def main():
    while True:
        clear_screen()
        display_menu()
        choice = input("Enter your choice (1-5): ")
        handle_input(choice)

if __name__ == "__main__":
    main()
