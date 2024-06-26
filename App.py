'''
Hello, simply run this program to start and help by adding to the source or reporting bugs. 
To help, there is a plotting function which is called by ctrl + alt + p (for Plot) to show the profit and losses that have occured.
This is still being worked on so any help will be greatly apprecieated escpecially as I am not a great coder
'''

import os
import requests
import json
import datetime
import time
import matplotlib.pyplot as plt
import threading
import keyboard


bid = False #it works and the headache is over

def price(): #dolla dolla bill yall
    outputJson = os.path.join(os.path.dirname(__file__), 'output.json')
    url = 'https://api.coinlore.net/api/tickers/'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        eth_data = next((item for item in data['data'] if item["symbol"] == "ETH"), None)
        if eth_data:
            ethusdVal = eth_data['price_usd']
            percent_change_1h = eth_data['percent_change_1h']
            volume24a = eth_data['volume24a']
            timeToday = datetime.datetime.now().isoformat()
            
            print(f"ETH Price: {ethusdVal}")
            print(f"Percent Change (1h): {percent_change_1h}")
            print(f"Volume (24h): {volume24a}")
            print(f"Time: {timeToday}")
        else:
            print("Ethereum data not found in the response.")
            return
    else:
        print(f"Error: {response.status_code} - {response.reason}")
        return
#Cash rules everything around me, C.R.E.A.M get the $
    existing_data = []
    if os.path.exists(outputJson):
        with open(outputJson, 'r') as json_file:
            existing_data = json.load(json_file)

    # Get the last ID and increment it by one
    if existing_data:
        last_id = existing_data[-1].get("id", 0)
        new_id = last_id + 1
    else:
        new_id = 1  # Start with ID 1 if the file is empty

    output = {
        "id": new_id,
        "ethusd": ethusdVal,
        "percent_change_1h": percent_change_1h,
        "volume24a": volume24a,
        "Time": timeToday
    }
    existing_data.append(output)

    with open(outputJson, 'w') as json_file:
        json.dump(existing_data, json_file, indent=1)
    #dump it just like all my exes
    return existing_data


def moneyBot(): #MoneyTrees
    outputJson = os.path.join(os.path.dirname(__file__), 'output.json')
    PLJson = os.path.join(os.path.dirname(__file__), 'profLoss.json')
   
    existing_data = []
    os.path.exists(outputJson)
    with open(outputJson, 'r') as json_file:
        existing_data = json.load(json_file)
#pick your poison tell me what you doing
    if existing_data:
        if os.path.exists(outputJson):
            if len(existing_data) >= 2:
                dataUse = []
                dataUse = existing_data[-2:]
                #print(dataUse[1])
                percent1hrNew = float(dataUse[1]['percent_change_1h'])
                percent1hrOld = float(dataUse[0]['percent_change_1h'])               
                diffPer = percent1hrNew - percent1hrOld
                print(f"differences in Percent over 1h: {diffPer}")
                priceNow = float(dataUse[1]['ethusd'])
                volNew = float(dataUse[1]['volume24a'])
                volOld = float(dataUse[0]['volume24a'])
                diffVol = (volNew - volOld) / volOld
                print(f"differences in trading Volume in 24hr: {diffVol}")
#but the one in front of the gun lives forever
    weightVol = 15
    weightPer = 1
        
    weightVol = weightVol * diffVol
    weightPer = weightPer * diffPer
   
    global bid
    global stake


    if bid == False:
        if weightVol + weightPer >= 1:
            print("buy")
            stake = priceNow
            bid = True
            print(stake)
            return
        else:
            print("Wait")
            return
    if bid == True: 
        if weightVol + weightPer >= 1:
            print("Hold")
            return
        else:
            print("Sell")
            bid = False
            profLoss = priceNow - stake 
            print(f"Profit/Loss: {profLoss}")

            if os.path.exists(PLJson):
                with open(PLJson, 'r') as json_file:
                    plData = json.load(json_file)
            else:
                plData = []

            profData = {
                "Prof/Loss": profLoss
            }
            plData.append(profData)

            with open(PLJson, 'w') as json_file:
                json.dump(plData, json_file, indent=1)
            return

            #check whether to sell or hold, if sell check to see how much was made or lost and track into a json file with weights /// need to do weights maybe
    #need to save the weight values as well maybe  (WIP)
def plotting():

    PLJson = os.path.join(os.path.dirname(__file__), 'profLoss.json')
    PlData = []
    with open(PLJson, 'r') as json_file:
        PlData = json.load(json_file)
    profLoss_values = [float(entry.get('Prof/Loss', 0.0)) for entry in PlData]

    plt.plot(profLoss_values)
    plt.xlabel('# of Sells')
    plt.ylabel('Profit/Loss [usd]')
    plt.show()

def mainProg():
    while True: #Don't know how to loop  ¯\_(ツ)_/¯
        price()
        moneyBot()
        time.sleep(60)

def listen_for_hotkey():
    keyboard.add_hotkey('ctrl+alt+p', plotting)  



if __name__ == "__main__":
    main_thread = threading.Thread(target=mainProg)
    main_thread.daemon = True
    main_thread.start()

    hotkey_thread = threading.Thread(target=listen_for_hotkey)
    hotkey_thread.daemon = True
    hotkey_thread.start()

    main_thread.join()
    hotkey_thread.join()
