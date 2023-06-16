import paho.mqtt.client as mqtt
import random
import mysql.connector
from datetime import datetime 
import time

i = 0
#Muc an toan
SaveMale = 30
saveFeMale = 24.5
# Thiết lập địa chỉ, cổng và chủ đề của kết nối MQTT Broker
broker = "118.69.218.59"
port = 1893
topics = ["/patient/1111/mornitor/oxi", "/patient/1111/mornitor/heartRate",\
           "/patient/1111/mornitor/grip","/patient/1111/estimate/avg" ]
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
        self.avg = 0
        self.oxi = 0
        self.heart = 0
        self.grip = 0
    
    def Connect_MQTT(self):
        self.client.username_pw_set(username, password)
        self.client.connect(broker, port)

    def on_connect(self,client, userdata, flags, rc):
        self.client.subscribe([(topic, 0) for topic in self.topics])
        
    def on_message(self,client, userdata, msg):
        if f"{msg.topic}" == "/patient/1111/estimate/avg":
            self.avg = msg.payload
            self.Write_Estimate()
        else:
            if f"{msg.topic}" == "/patient/1111/mornitor/oxi":
                self.oxi = msg.payload
            elif f"{msg.topic}" == "/patient/1111/mornitor/heartRate":
                self.heart = msg.payload
            elif f"{msg.topic}" == "/patient/1111/mornitor/grip":
                self.grip = msg.payload 
            

    def Write_Estimate(self):
        heso = HeSo_TiLeBenh(self.avg, True)
        sql = f"INSERT INTO estimate (id_patient, time, AVG, DotQuy, NhoiMau, TimMach) \
                VALUES ('{1111}', '{datetime.now()}', '{float(self.avg)}',\
                      '{float(heso*9)}', '{float(heso*7)}', '{float(heso*17)}')"
        TruyVanSQL(sql)

    def Write_Mornitor(self):
        sql = f"INSERT INTO mornitor (id_patient, time, heartRate, Oxi, GripStrength) \
                VALUES ('{1111}', '{datetime.now()}', \
                    '{float(self.heart)}', '{float(self.oxi)}', '{float(self.grip)}')"
        TruyVanSQL(sql)

    def Run(self):
        self.client.loop_start()
        self.client.on_connect = self.on_connect
        time_cur = time.perf_counter()
        while time_cur + 10 > time.perf_counter():
            self.client.on_message = self.on_message

        time_cur = time.perf_counter()
        self.Write_Mornitor()
        self.client.loop_stop()
        

client_mor = MQTT(broker,port,username,password,topics)
client_mor.Connect_MQTT()
while True:
    client_mor.Run()
