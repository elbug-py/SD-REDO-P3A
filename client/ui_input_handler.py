class UIInputHandler:

    def menu_input(self):
        selected_option = input("     ")
        if self.check_menu_input(selected_option):
            return int(selected_option)
        return False

    def check_menu_input(self, menu_input):
        return menu_input in ["1", "2", "3"]

    def cleverhub_input(self, all_cleverhub):
        selected_option = input("    - ")
        return self.check_cleverhub_input(selected_option, all_cleverhub)

    def check_cleverhub_input(self, menu_input, cleverhub_names):
        try:
            index = int(menu_input) - 1
            if 0 <= index < len(cleverhub_names):
                return cleverhub_names[index]
        except ValueError:
            pass
        return False

    def device_input(self, device_process):
        devices = input("     - ")
        formated_devices = self.check_device_input(devices, device_process)
        if formated_devices is False:
            return False

        return formated_devices

    def check_device_input(self, devices_string, device_process):

        if not devices_string or devices_string[-1] != ";":
            return False

        devices = devices_string.strip(";").split(";")

        if device_process == "CHECK":
            if devices == ["ALL"] or devices == ["RETURN"]:
                return devices

            for device in devices:
                if not self.check_device_starting_name(device, device_process):
                    return False
            return devices

        elif device_process == "CHANGE":
            if devices == ["RETURN"]:
                return devices

            formatted_devices = []
            for item in devices:
                if "=" in item:
                    key, status = item.split("=")
                    if self.check_device_starting_name(
                        key, device_process
                    ) and self.check_status(status):
                        formatted_devices.append({key: int(status)})
                    else:
                        return False
                else:
                    return False
            return formatted_devices

        return False

    def check_device_starting_name(self, device_name, device_process):
        if device_name.isalnum():
            if device_name[0:2] in ("DS", "LS"):
                if len(device_name) < 3 or not device_name[2:].isdigit():
                    return False
                return True
            elif device_name[0:2] in ("AS", "HS", "CS"):
                if len(device_name) > 2:
                    return False
                return True
            elif (
                device_name[0:2] in ("TR", "AO") and device_process == "CHECK"
            ):
                if len(device_name) > 2:
                    return False
                return True
            elif device_name[0:2] in ("PS") and device_process == "CHECK":
                if len(device_name) < 3 or not device_name[2:].isdigit():
                    return False
                return True
            else:
                return False
        return False

    def check_status(self, status):
        if status not in ["0", "1"]:
            return False
        return True
