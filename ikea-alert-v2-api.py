# -*- coding: utf-8 -*-

import json
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.application import MIMEApplication
import pandas as pd 

import time


def main(pid, zipcs):
    while True:
        status = check_product(pid, zipcs)
        
        if status == False:
            break
        
        print("Checking for availability...")
        
        time.sleep(60)
        


def check_product(pid, zipcs):
    for zipc in zipcs:
        url_api = f'https://api.ingka.ikea.com/cia/availabilities/ru/de?itemNos={pid}&zip={zipc}'
        
        headers = {
            'Accept': 'application/json;version=2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'X-Client-ID': 'b6c117e5-ae61-4ef5-b4cc-e0b1e37f0631'
        }
        
        r = requests.get(url_api, headers=headers).json()
        #print(json.dumps(r, indent=4))
        
        
        stock = r["availabilities"][0]["buyingOption"]["homeDelivery"]["availability"]["probability"]["thisDay"]["messageType"]
        print(stock)
        
        if stock != "OUT_OF_STOCK":
            send_mail()
            return False
        
        
def send_mail() -> check_product:
    # Credentials
    user = 'apikey'
    password = 'xxx'

    # Setup
    sent_from = "xxx@hotmail.com"
    #cc = mail_list
    sent_to = ["xxx@gmail.com"]
    
    # Date
    now = pd.to_datetime("now")
    day = now.date()
   
    # E-Mail Layout
    message = "Der Stuhl ist verfügbar!"
    msg = MIMEMultipart() 
    msg['Subject'] = "IKEA Alerts | Verfügbarkeit"
    msg['From'] = sent_from
    msg['To'] = ", ".join(sent_to)
    #msg['Cc'] = ", ".join(cc)

    msg.attach(MIMEText(message, 'plain'))


    # Try to send
    try:
        server = smtplib.SMTP('smtp.sendgrid.net', 587) 
        #server.set_debuglevel(1)
        #server.ehlo()
        server.starttls()
        server.login(user, password)
        server.sendmail(sent_from, sent_to, msg.as_string())
        server.quit()
        print('Email sent!')

    except:
        print('Something went wrong...')
    
if __name__ == "__main__": 
    pid = "89392189"
    zipcs = ["50829", "50997"]
    
    main(pid, zipcs)
