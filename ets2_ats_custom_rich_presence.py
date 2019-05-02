from pypresence import Presence
import requests as req
import json
import time
import logging

print("\n"
      "\n"
      "    ##############################################################\n"
      "    # ETS 2 Custom Discord Rich Presence script by Ashish Shetty #\n"
      "    ##############################################################\n"
      "\n"
      "  please make sure that ETS2/ATS telemetry server is running\n"
      "  before you opened this file..\n"
      "\n"
      "  https://github.com/Shetty073/ets2-ats-custom-discord-rich-presence\n")


def get_data():
    try:
        response = req.get("http://localhost:25555/api/ets2/telemetry")
        raw_data = json.loads(response.content)
        return raw_data
    except Exception as e:
        logging.basicConfig(filename='error.log', level=logging.INFO)
        logging.error(f"\nFatal error: \n{str(e)}\n")
        print("\nFatal error: Please make sure that the ETS 2 / ATS Telemetry server is open before "
              "running this application.\n")
        input("Press enter key to exit....")
        exit(1)


def start():
    raw_data = get_data()
    game_data = raw_data["game"]
    if game_data["gameName"]:
        if game_data["gameName"] == "ETS2":
            client_id = "ETS2_client_id"  # App client ID from discord developer portal
        elif game_data["gameName"] == "ATS":
            client_id = "ATS_client_id"  # App client ID from discord developer portal
        print(f'{game_data["gameName"]} connected...')
        run(client_id)
    else:
        print("Waiting for game to connect...")
        time.sleep(3.5)
        start()


def get_details():
    raw_data = get_data()
    game_data = raw_data["game"]
    truck_data = raw_data["truck"]

    if not game_data["connected"]:
        details = "Simulation not started"
    else:
        if game_data["paused"]:
            details = "Simulation paused"
        else:
            if truck_data["engineOn"]:
                engine = "On"
            else:
                engine = "Off"
            details = f'Driving: {truck_data["make"]} {truck_data["model"]}, Engine: {engine}'
    return details


def get_state():
    raw_data = get_data()
    game_data = raw_data["game"]
    truck_data = raw_data["truck"]

    if not game_data["connected"]:
        state = "Waiting for simulator to load"
    else:
        if game_data["paused"]:
            state = "Driver drinking coffee"
        else:
            speed = int(truck_data["speed"])
            rpm = int(truck_data["engineRpm"])
            if speed < 0:
                speed = 0
            if int(truck_data["displayedGear"]) <= 0:
                if int(truck_data["displayedGear"]) < 0:
                    gear = "R"
                else:
                    gear = "N"
            else:
                gear = truck_data["displayedGear"]
            fuel = (int(truck_data["fuel"]) / int(truck_data["fuelCapacity"]) * 100)
            state = f'{speed} Km/hr {rpm} RPM Gear: {gear} Fuel: {int(fuel)}% left'
    return state


def run(client_id):
    try:
        RPC = Presence(client_id)
        RPC.connect()
        print("Running...\n"
              "NOTE:\n"
              "If you are playing ETS 2 and want to start playing ATS (or vice-versa) then "
              "after closing ETS 2 and before starting ATS you must RESTART this application ALONG WITH the ETS 2 "
              "TELEMETRY SERVER also.\n"
              "Close this window once you are done playing the game...")
        while True:
            # Image section needs to be updated
            RPC.update(state=get_state(), details=get_details(), large_image="Euro Truck Simulator 2",
                       large_text="Large Text Here!",
                       small_image="small-image", small_text="Small Text Here!")
            time.sleep(0.1)
    except Exception as e:
        logging.basicConfig(filename='error.log', level=logging.INFO)
        logging.error(f"\nFatal error: \n{str(e)}\nPlease make sure that Discord is open and running...")
        print("\nFatal error: Please make sure that Discord is open before "
              "running this application.\n")
        input("Press enter key to exit....")
        exit(1)


start()
