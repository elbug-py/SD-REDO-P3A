# Mover todos los prints a este archivo

class UIPrinter:
    def print_menu(self):
        print("\n ♦♦ ------------------------------------ ♦♦ \n")
        print(" ♫♪ Welcome to the UI console for CleverHome ♪♫ \n")
        print(" Please select one of the options: \n")
        print("     1. Check sensor status ")
        print("     2. Change sensor status ")
        print("     3. Exit \n")

    def print_invalid_input_menu(self):
        print("\n ►►► ------------------------------------ ◄◄◄ \n")
        print(" Invalid input, please write a number from 1 to 3 \n")
        print(" ►►► ------------------------------------ ◄◄◄ \n")

    def print_submenu_check_status(self):
        print(" ♦♦ ------------------------------------ ♦♦ \n")
        print(" Please write the sensors/devices you want to check ")
        print("\n  ########  ######## \n")
        print("  The format of the devices you want to check should be like the following:")
        print("    - ALL;  → To get the status of all devices of the cleverhub selected")
        print("    - DS0;LS0;LS1;PS0;HS;CS;TR;  → Example of the listing of devices names")
        print("    - RETURN;   → To return to the main menu")
        print("\n  ########  ######## \n ")

    def print_submenu_change_status(self):
        print(" ♦♦ ------------------------------------ ♦♦ \n")
        print(" Please write the sensors/devices you want to change ")
        print("\n  ########  ######## \n")
        print("  The format of the devices you want to change should be like the following:")
        print("    - DS0=1;LS1=1;AS=0;HS=1;CS=0;  → Example of the listing of devices names with their status")
        print("    - RETURN;   → To return to the main menu")
        print("\n  ########  ######## \n ")

    def print_invalid_input_submenu_check_status(self):
        print("\n ►►► ------------------------------------ ◄◄◄ \n")
        print(" Invalid input, rememeber that your sensors/devices should be write like this: \n")
        print("     ALL;  or  DS0;LS0;LS1;PS0;HS;CS;TR;  or RETURN; \n")
        print(" Also remember that TR,CS,HS,AS,AO aren't follow by a number.")
        print(" While DS, LS and PS are always follow by a number \n")
        print(" ►►► ------------------------------------ ◄◄◄ \n")

    def print_invalid_input_submenu_change_status(self):
        print("\n ►►► ------------------------------------ ◄◄◄ \n")
        print(" Invalid input, rememeber that your sensors/devices should be write like this: \n")
        print("     DS0=1;LS1=1;AS=0;HS=1;CS=0;   or RETURN; \n")
        print(" Also remember that CS,HS,AS aren't follow by a number.")
        print(" That TR,AO and PS are readonly sensors.")
        print(" While DS, LS and PS are always follow by a number")
        print(" And that you can only set the status to 0 or 1 for the wanted devices \n")
        print(" ►►► ------------------------------------ ◄◄◄ \n")

    def print_exit(self):
        print(" ♦♦ ------------------------------------ ♦♦ \n")
        print(" Exiting ... ")
        print(" Bye bye  ♫ ♫ \n")

    def print_device_status(self, devices, hub_name):
        print("\n ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ \n")

        print(f"\n ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿  {hub_name} ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ \n")
        print(" Device Status:")
        for device in devices:
            device_name, status = device
            print(f"    {device_name}: {status}")

        print(f"\n ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿  {hub_name} ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ ✿ \n")

    def print_select_cleverhub(self, cleverhub_list):
        print("\n ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ \n")
        print(" Please select a CleverHub:")
        for i, name in enumerate(cleverhub_list, start=1):
            print(f"    {i}. {name}")

        print()

    def print_invalid_cleverhub_option(self):
        print("\n ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ - ✦ \n")

        print("\n ►►► ------------------------------------ ◄◄◄ \n")
        print(" Invalid cleverhub option, please write the number asociated to the wanted cleverhub \n")
        print(" ►►► ------------------------------------ ◄◄◄ \n")

    def print_no_cleverhub(self):
        print("\n ►►► ------------------------------------ ◄◄◄ \n")
        print(" No cleverhub connected to implement this method.")
        print(" Please check you have the cleverhub connected and restart this program \n")
        print(" ►►► ------------------------------------ ◄◄◄ \n")

    def print_setting_errors(self, error_message):
        print("\n ►►► ------------------------------------ ◄◄◄ \n")
        print(error_message)
        print("\n ►►► ------------------------------------ ◄◄◄ \n")
