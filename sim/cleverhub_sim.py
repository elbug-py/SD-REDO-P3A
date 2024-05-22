import socket
import traceback
import sys
import threading
import time
import random
import os

random.seed(121)

NUM_DOORS = 3
NUM_LIGHTS = 5
NUM_PROXIMITY = 2

RANDOM_ERROR_ENABLED = False


class HouseState(object):
    """
    Model the house state
    """

    def __init__(self, user, password, home_name):
        """
        Initialize the house state
        """
        self.__doors = [True] * NUM_DOORS
        self.__lights = [True] * NUM_DOORS
        self.__proximity = [True] * NUM_PROXIMITY
        self.__alarm_state = False
        self.__alarm_sounding = False
        self.__heater_state = True
        self.__chiller_state = False
        self.__temperature = 65

        self.__user = user
        self.__password = password
        self.__home = home_name
        self.__target_temp = 68

        self.__param = ";"
        self.__end = "."

    def update_simulation(self):
        """
        Update the house simulation. This is really very simple
        """
        if self.__heater_state:
            self.__temperature += 1
        if self.__chiller_state:
            self.__temperature -= 1

    def set_state(self, new_state):
        """
        Handle set state requests
        """
        print("Received state update {0}:".format(new_state[3:-1]))
        params = new_state[3:-1].split(";")

        for par in params:
            if len(par) == 0:
                continue
            k, v = par.split("=")
            if k[:2] == "LS":
                idx_light = int(k[2])
                if v == "1":
                    self.set_light(idx_light, True)
                else:
                    self.set_light(idx_light, False)
            elif k[:2] == "DS":
                idx_door = int(k[2])
                if v == "1":
                    self.set_door(idx_door, True)
                else:
                    self.set_door(idx_door, False)
            elif k == "AS":
                if v == "1":
                    self.set_alarm_state(True)
                else:
                    self.set_alarm_state(False)
                    self.set_alarm_sounding(False)
            elif k == "AO":
                if v == "1":
                    self.set_alarm_sounding(True)
            elif k == "HS":
                if v == "1":
                    self.set_heater_state(True)
                else:
                    self.set_heater_state(False)
            elif k == "CS":
                if v == "1":
                    self.set_chiller_state(True)
                else:
                    self.set_chiller_state(False)

    # Getters and setters for house properties
    def get_temperature(self):
        return self.__temperature

    def set_door(self, idx, value):
        self.__doors[idx] = value

    def get_door(self, idx):
        if self.__doors[idx]:
            return "1"
        return "0"

    def set_light(self, idx, value):
        self.__lights[idx] = value

    def get_light(self, idx):
        if self.__lights[idx]:
            return "1"
        return "0"

    def set_proximity(self, idx, value):
        self.__proximity[idx] = value

    def get_proximity(self, idx):
        if self.__proximity[idx]:
            return "1"
        return "0"

    def set_alarm_state(self, a):
        self.__alarm_state = a

    def get_alarm_state(self):
        if self.__alarm_state:
            return "1"
        return "0"

    def set_alarm_sounding(self, a):
        self.__alarm_sounding = a

    def get_alarm_sounding(self):
        if self.__alarm_sounding:
            return "1"
        return "0"

    def set_heater_state(self, h):
        self.__heater_state = h

    def get_heater_state(self):
        if self.__heater_state:
            return "1"
        return "0"

    def set_chiller_state(self, h):
        self.__chiller_state = h

    def get_chiller_state(self):
        if self.__chiller_state:
            return "1"
        return "0"

    def get_user(self):
        return self.__user

    def get_password(self):
        return self.__password

    def get_home(self):
        return self.__home

    def get_target_temperature(self):
        return self.__target_temp

    def get_hello_message(self):
        """
        Connect to the house and say hello
        """
        return (
            f"HL:"
            f"USR={self.get_user()};"
            f"PWD={self.get_password()};"
            f"HOM={self.get_home()};"
            f"TT={self.get_target_temperature()}."
        )

    def get_state(self):
        """
        Handle get state requests
        """
        state = ""
        for door_idx in range(0, len(self.__doors)):
            state = state + "DS{0}={1};".format(
                door_idx, self.get_door(door_idx)
            )

        for light_idx in range(0, len(self.__lights)):
            state = state + "LS{0}={1};".format(
                light_idx, self.get_light(light_idx)
            )

        for prox_idx in range(0, len(self.__proximity)):
            state = state + "PS{0}={1};".format(
                prox_idx, self.get_proximity(prox_idx)
            )

        state = (
            state + f"TR={self.get_temperature()};"
            f"AS={self.get_alarm_state()};"
            f"AO={self.get_alarm_sounding()};"
            f"HS={self.get_heater_state()};"
            f"CS={self.get_chiller_state()};"
        )
        return state


class UserThread(threading.Thread):
    """
    Thread to mimic user behavior
    """

    def __init__(self, house):
        """
        Set up the stop event
        """
        super().__init__()
        self.__stop = threading.Event()
        self.daemon = True
        self.house = house

    def stop(self):
        """
        Terminate this thread
        """
        self.__stop.set()

    def run(self):
        """
        Run the user simulation thread
        """
        try:
            while not self.__stop.is_set():
                print("Current state: {}".format(self.house.get_state()))

                cmd = input(
                    "\nEnter a command: d=[toggle door], l=[toggle light], p=[toggle proximity], RET=[show current status]: "
                )

                if cmd == "d":
                    idx = int(input("Enter the door number: "))
                    if self.house.get_door(idx) == "1":
                        self.house.set_door(idx, False)
                    else:
                        self.house.set_door(idx, True)
                    print("door is now {}".format(self.house.get_door(idx)))
                elif cmd == "l":
                    idx = int(input("Enter the light number: "))
                    if self.house.get_light(idx) == "1":
                        self.house.set_light(idx, False)
                    else:
                        self.house.set_light(idx, True)
                    print("light is now {}".format(self.house.get_light(idx)))
                elif cmd == "p":
                    idx = int(input("Enter the proximity sensor number: "))
                    if self.house.get_proximity(idx) == "1":
                        self.house.set_proximity(idx, False)
                    else:
                        self.house.set_proximity(idx, True)
                    print(
                        "proximity is now {}".format(
                            self.house.get_proximity(idx)
                        )
                    )
        except:
            print("\nAborting simulation!")
            os._exit(1)

        return


class TimeThread(threading.Thread):
    """
    Thread to mimic passage of time in the house environment.
    """

    def __init__(self, house):
        super().__init__()
        self.__stop = threading.Event()
        self.daemon = True
        self.house = house

    def stop(self):
        """
        Terminate this thread
        """
        self.__stop.set()

    def run(self):
        """
        Run the time simulation thread
        """
        curr_time = 0
        time_interval = 5
        while not self.__stop.is_set():
            print("\nTime since start: {} s".format(curr_time))
            self.house.update_simulation()
            time.sleep(time_interval)
            curr_time = curr_time + time_interval

        return


class CleverHubProtocolConnection:
    """
    Handles CleverHub Protocol requests through TCP.
    """

    def __init__(self, house):
        self.connection = None
        self.house = house

    def connect(self, server_address):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect(server_address)

    def send_hello(self):
        # ! TEST ADD SOMETHING HERE
        self.connection.sendall("ClvrHb".encode())
        msg = self.connection.recv(1024).decode()
        print(f"Received: {msg}")
        hello_message = self.house.get_hello_message()
        self.connection.sendall(hello_message.encode())

    def generate_random_error(self):
        if RANDOM_ERROR_ENABLED:
            return random.randint(0, 5) == 4
        else:
            return False

    def handle_next_request(self):
        print("\nWaiting for message from platform...", flush=True)
        data = self.connection.recv(1024).decode("ascii")
        print(f"Received (len: {len(data)}): {data}", flush=True)

        if data:
            if data[:3] == "ACC":
                print("Connection was succesful!")
            elif data[:3] == "REF":
                print("Connection was declined!")
                raise Exception(
                    "Connection was refused; check if user/password are correct, or if there is already a Hub with the same HOM name connected."
                )
            elif data[:2] == "GS":
                su = "SU:{}.".format(self.house.get_state())
                print("Reply: " + su, flush=True)
                self.connection.sendall(su.encode())
            elif data[:2] == "SS":
                is_random_error = self.generate_random_error()
                if not is_random_error:
                    self.house.set_state(data)
                    print("Reply: OK", flush=True)
                    self.connection.sendall("OK.".encode())
                else:
                    print("Could not set state!", flush=True)
                    print("Reply: ERR", flush=True)
                    self.connection.sendall("ERR.".encode())
            else:
                print("Error, unknown request: {}".format(data), flush=True)
        else:
            print("Platform closed connection")
            return False

        return True

    def close(self):
        if self.connection:
            self.connection.close()


def setup_connection(server_address, house):
    client = CleverHubProtocolConnection(house)
    client.connect(server_address)
    client.send_hello()
    return client


def reconnect(server_address, house):
    max_attempts = 3
    curr_attempt = 1
    while curr_attempt <= max_attempts:
        try:
            print("Attempting reconnection")
            client = setup_connection(server_address, house)
            print("Reconnection successful")
            return client
        except Exception as e:
            print("Error reconnecting: %s" % str(e))
            time.sleep(2)
        curr_attempt += 1

    raise Exception("Could not reconnect")


def main_sim():
    """
    Wait for incoming connections and run the simulation
    """
    print("Starting CleverHub Simulator", flush=True)

    server_address = (sys.argv[1], int(sys.argv[2]))
    username = sys.argv[3]
    password = sys.argv[4]
    home_name = sys.argv[5]

    print(
        "Will connect to {0}:{1}".format(server_address[0], server_address[1]),
        flush=True,
    )
    print(
        "Will use user and pass {0}:{1}".format(username, password), flush=True
    )
    print("Will use house name {0}".format(home_name), flush=True)

    house = HouseState(username, password, home_name)

    user_thread = UserThread(house)
    user_thread.start()

    time_thread = TimeThread(house)
    time_thread.start()

    client = None
    try:
        client = setup_connection(server_address, house)
        while True:
            still_connected = client.handle_next_request()
            if not still_connected:
                client = reconnect(server_address, house)
    except Exception as e:
        print("Error: %s" % str(e))
        traceback.print_exc()
    finally:
        print("Stopping simulator!")
        user_thread.stop()
        time_thread.stop()
        if client:
            client.close()
        sys.exit(1)


if __name__ == "__main__":
    main_sim()
