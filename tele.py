# -*- coding: utf-8 -*-
"""
Created on Sun May  2 17:39:56 2021

@author: Sumit
"""

from telegram import *
from telegram.ext import *
import pandas as pd


df = pd.read_csv('IndiaPincode.csv',encoding='windows-1252')
pinCodeList = df['Pincode'].values
pinCodeList = list(set(pinCodeList))

    

bot = Bot("1758675742:AAE9QyajzyG5EOkr3GQpWmBGUXXKS98P_s4")
#print(bot.get_me())

updater = Updater("1758675742:AAE9QyajzyG5EOkr3GQpWmBGUXXKS98P_s4",use_context=True)

dispatcher = updater.dispatcher

def getDetails(update:Update,context:CallbackContext):
    pin = update.MESSAGE
    bot.send_message(
            chat_id = update.effective_chat.id,
            text="pin",
            )
    

def test_function(update:Update,context:CallbackContext):
    bot.send_message(
            chat_id = update.effective_chat.id,
            text="Please enter pincode",
            )
    pin = update.MESSAGE.text
    bot.send_message(
            chat_id = update.effective_chat.id,
            text=pin,
            )

start = CommandHandler('pincode',test_function)

dispatcher.add_handler(start)

updater.start_polling()