import paho.mqtt.client as mqtt
import random
import mysql.connector
from datetime import datetime 
import time

i = 0
#Muc an toan
SaveMale = 30.2
saveFeMale = 24.3
# Thiết lập địa chỉ, cổng và chủ đề của kết nối MQTT Broker
broker = "103.130.211.150"
port = 10040
topics = ["/patient/+/mornitor/oxi", "/patient/+/mornitor/heartRate",\
           "/patient/+/mornitor/grip","/patient/+/estimate/avg" ]
client_id = f"python-mqtt-{random.randint(0, 1000)}"
username = "phunghx"
password = "nckh"
#Host mySQL
db_host = '103.130.211.150'
db_port = '10039'
db_user = 'nckh'
db_password = 'nckhfit'
db_name = 'mydb'

def TruyVanSQL(sql):
    db = mysql.connector.connect(host=db_host, port=db_port, user=db_user, password=db_password, database=db_name)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    db.close()

def HeSo_TiLeBenh(avg, isMale):
    heso = 0.0
    if isMale == True:
        if float(SaveMale) >= float(avg):
            heso = (float(SaveMale) - float(avg))/5
    elif float(saveFeMale) >= float(avg):
        heso = (float(SaveMale) - float(avg))/5
    return heso

class MQTT:
    def __init__(self, broker, port, username, password, topics):
        self.broker = broker
        self.port = port
        self.username = username
        self.password = password
        self.topics = topics
        self.client = mqtt.Client(client_id)
        self.listuser = []
        self.avg = {}
        self.oxi = {}
        self.heart = {}
        self.grip = {}
    
    def Connect_MQTT(self):
        self.client.username_pw_set(username, password)
        self.client.connect(broker, port)

    def on_connect(self,client, userdata, flags, rc):
        self.client.subscribe([(topic, 0) for topic in self.topics])
        
    def on_message(self,client, userdata, msg):
        userID = msg.topic[9:25]
        if userID not in self.listuser:
            self.listuser.append(userID)

        if "avg" in f"{msg.topic}":      
            self.avg[userID] = msg.payload
            self.Write_Estimate(userID)
        else:
            if "oxi" in f"{msg.topic}":  
                self.oxi[userID] = msg.payload
            elif "heartRate" in f"{msg.topic}":  
                self.heart[userID] = msg.payload
            elif "grip" in f"{msg.topic}":
                self.grip[userID] = msg.payload        

    def Write_Estimate(self, userID):
        heso = HeSo_TiLeBenh(self.avg[userID], True)
        sql = f"INSERT INTO estimate (id_patient, time, AVG, DotQuy, NhoiMau, TimMach) \
                VALUES ('{userID}', '{datetime.now()}', '{float(self.avg[userID])}',\
                      '{float(heso*9)}', '{float(heso*7)}', '{float(heso*17)}')"
        TruyVanSQL(sql)

    def Write_Mornitor(self):
        for userID in self.listuser:
            if userID in self.heart:
                heart = self.heart[userID]
            else: heart = 0
            if userID in self.oxi:
                oxi = self.oxi[userID]
            else: oxi = 0
            if userID in self.grip:
                grip = self.grip[userID]
            else: grip = 0
            sql = f"INSERT INTO mornitor (id_patient, time, heartRate, Oxi, GripStrength) \
                    VALUES ('{userID}', '{datetime.now()}', \
                        '{float(heart)}', '{float(oxi)}', '{float(grip)}')"
            TruyVanSQL(sql)

    def Run(self):
        self.client.loop_start()
        self.client.on_connect = self.on_connect
        time_cur = time.perf_counter()
        while time_cur + 30 > time.perf_counter():
            self.client.on_message = self.on_message

        time_cur = time.perf_counter()
        self.Write_Mornitor()
        self.client.loop_stop()
        self.listuser = []
        self.avg = {}
        self.oxi = {}
        self.heart = {}
        self.grip = {}

client_mor = MQTT(broker,port,username,password,topics)
client_mor.Connect_MQTT()
while True:
    client_mor.Run()
