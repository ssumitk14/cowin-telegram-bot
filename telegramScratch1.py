# -*- coding: utf-8 -*-
"""
Created on Sun May  2 19:35:05 2021

@author: Sumit
"""

import requests as requests
import random
import pandas as pd
from datetime import datetime
import json

#url = "https://api.telegram.org/bot1758675742:AAHkbMi_RJXpHYyLXb-MlcoVI_-8M6I_HQ4/"

#url = "https://api.telegram.org/bot1796513787:AAF9d9ZfVj4-2chVqqh--mcrKz0jMyY2k9k/"
#url = "https://api.telegram.org/bot1659054275:AAE4f0ErIEFKvqegxt1jspwKjdJKk3ZKUTs/"
#url = "https://api.telegram.org/bot1577128236:AAGx6eS3-n77ZQlEivoYMVK0i3aR-fZvj1o/"
url = "https://api.telegram.org/bot1728962806:AAEHTOKX825KczBXyxyeH3z9bTxSy76kVtc/"


# create func that get chat id
def get_chat_id(update):
    chat_id = update['message']["chat"]["id"]
    return chat_id


# create function that get message text
def get_message_text(update):
    message_text = update["message"]["text"]
    return message_text


# create function that get last_update
def last_update(req):
    response = requests.get(req + "getUpdates")
    response = response.json()
    result = response["result"]
    total_updates = len(result) - 1
    return result[total_updates]  # get last record message update


# create function that let bot send message to user
def send_message(chat_id, message_text):
    params = {"chat_id": chat_id, "text": message_text}
    response = requests.post(url + "sendMessage", data=params)
    return response

def getDetails(pinCode):
    headers = {'Content-Type': 'application/json',
               'Accept-Language' : 'hi_IN' , 
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
               }
    pinCode = str(pinCode)
    date = datetime.today().strftime('%d-%m-%Y')
    url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=' + pinCode + '&date=' + date
    reques = requests.get(url,headers=headers)
    
    data = reques.json()
    blockName = []
    fee = []
    name = []
    slots = []
    ageLimit = []
    typeOfVaccine = []
    numberOfVaccine = []
    index = 0
    details = ""
    for i in data['centers']:
        blockName.append(i['block_name'])
        name.append(i['name'])
        lower = i['from'].split(":")[0]
        upper = i['to'].split(":")[0]
        if int(lower)>12:
            lower = int(lower) - 12
            lower = str(lower) + "PM"
        elif lower[0]=='0':
            lower = lower[1:] + "AM"
        else:
            lower = lower + "AM"
        if int(upper)>12:
            upper = int(upper) - 12
            upper = str(upper) + "PM"
            
        time = lower + "-" + upper
        slots.append(time)
        try:
            for vac in i['vaccine_fees']:
                typeOfVaccine.append(vac['vaccine'])
                fee.append(vac['fee'])
        except:
            fee.append('FREE')
            typeOfVaccine.append('Information not available')
            
        for j in i['sessions']:
            if j['date']==date:
                numberOfVaccine.append(j['available_capacity'])
                ageLimit.append(j['min_age_limit'])
                details = details + i['name'] +'==>'+str(j['available_capacity'])+'==>'+str(fee[index]) + "==>"+str(j['min_age_limit'])+"+"+"==>"+time+"==>"
                print("{:30} {:5}  {}".format(i['name'],j['available_capacity'],fee[index],j['min_age_limit'],time))
        index +=1

    return details

# create main function for navigate or reply message back
def main():
    df = pd.read_csv('IndiaPincode.csv',encoding='windows-1252')

    pinCodeList = df['Pincode'].values
    pinCodeList = list(set(pinCodeList))
    
    update_id = last_update(url)["update_id"]
    while True:
        update = last_update(url)
        if update_id == update["update_id"]:
            print("Yess")
            if get_message_text(update).lower() == "hi" or get_message_text(update).lower() == "hello" or get_message_text(update)=='/start':
                #print("Insia")
                send_message(get_chat_id(update), 'Hello Welcome to our bot.\nEnter your pincode to get the details.')
            
            elif get_message_text(update).isdigit():
                if int(get_message_text(update)) in pinCodeList:
                    details = getDetails(int(get_message_text(update)))
                    print(details)
                    lst = details.split("==>")
                    final = []
                    for i in lst:
                        if len(i)!=0:
                            final.append(i.strip())
                    
                    d = {}
                    d['Name'] = final[0::5]
                    d['Avaiable Vaccine'] = final[1::5]
                    d['Fee'] = final[2::5]
                    d['Minimum Age'] = final[3::5]
                    d['Slots'] = final[4::5]
                    print(d)
                    df1 = pd.DataFrame(d)
                    total = []
                    
                    for i in range(df1.shape[0]):
                        total.append(df1.iloc[i,:].values)
                    if len(total)==0:
                        send_message(get_chat_id(update), "Data Not Available")
                    for i in total:
                        name = "1. Center Name: " + i[0] + '\n'
                        count = "2. Available vaccines: " + i[1] + '\n'
                        fee = "3. Fee: " + i[2] + "\n"
                        age = "4. Minimum age: " + i[3] + "\n"
                        time = "5. Timings: " + i[4] + "\n"
                        temp = name + count + fee + age + time
                    
                        send_message(get_chat_id(update), temp)
                    send_message(get_chat_id(update), "--------------Thank You--------------")
                else:
                    send_message(get_chat_id(update), "Wrong pincode")
            else:
                send_message(get_chat_id(update), "Please re-enter pincode.\nFor example: 560066")
                    
           
            
                
            update_id += 1


# call the function to make it reply

main()

