#! /usr/bin/python
'''
抓取lazyengineers 的DL 資料,它是免費的MQTT borker賬戶
'''
__author__ = "Marty Chao"
__version__ = "1.0.2"
__maintainer__ = "Marty Chao"
__email__ = "marty@browan.com"
__status__ = "Production"
# Change log 1.0.1, support paho-mqtt 1.2

import paho.mqtt.client as mqtt
import json
import sys
from optparse import OptionParser

usage = "usage: %prog [options] [host]\n\
  host: a MQTT broker IP \n\
  e.g.: '%prog --ip 192.168.1.1' will sub server and print data."

parser = OptionParser(usage)
parser.add_option("-d", "--display-lcd", action="store_true",
                  help="print message to raspberry LCD")
parser.add_option("-l", "--long-detail", action="store_true",
                  help="print detail JSON message")
parser.add_option("-t", "--topic", action="store",
                  dest="topic", default="GIOT-GW/#",
                  help="provide connection topic")
parser.add_option("-i", "--ip", action="store",
                  dest="host", default="mqtt.lazyengineers.com",
                  help="sub from MQTT broker's IP ")
parser.add_option("-u", "--user", action="store",
                  dest="username", default="lazyengineers",
                  help="sub from MQTT broker's username ")
parser.add_option("-P", "--pw", action="store",
                  dest="password", default="lazyengineers",
                  help="sub from MQTT broker's password ")
parser.add_option("-p", action="store",
                  dest="port", default=1883,
                  help="sub from MQTT broker's Port ")
parser.add_option("-R","--downlink", action="store_true",
                  help="If payload is 'FF' print out Downlink Command")
(options, args) = parser.parse_args()

print ("MQTT broker is:" + options.host + ":" + str(options.port))
print ("MQTT Topic is:" + options.topic)

# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    '''
    GIoT Module Json UpLink Example
    GIOT-GW/UL/xxxx [{"channel":923125000, "sf":10,
    "time":"2017-03-13T03:59:29", "gwip":"10.6.1.49",
    "gwid":"0000f835dde7de2e", "repeater":"00000000ffffffff",
    "systype":10, "rssi":-118.0, "snr":0.5, "snr_max":3.8, "snr_min":-4.5,
    "macAddr":"000000000a000158", "data":"015dff017b81ed0736767c",
    "frameCnt":26920, "fport":2}]
    '''
    # client.subscribe(Topic)
    # client.subscribe("GIOT-GW/UL/+")
    # client.subscribe("GIOT-GW/UL/1C497B4321AA")
    client.subscribe(options.topic)
    # GIOT-GW/DL/1C497B499010 [{"macAddr":"0000000004000476","data":"5678","id":"998877ffff0001","extra":{"port":2, "txpara":6}}]
    # GIOT-GW/DL-report/1C497B499010 {"dataId":"16CBD520C19162013CD6436CB330565E", "resp":"2016-11-30T15:02:40Z", "status":-1}


def on_message(client, userdata, msg):
    json_data = msg.payload.decode()
    #print(msg.payload)
    print(json_data)
    print(msg.topic)
    #print("-------------")
    #print("data type:" + str(type(json_data)))
    #print(type(msg.topic))
    #print (" msg.topic 0-11 is:" + msg.topic[:11] )
    #print (" msg.topic 0-17 is:" + msg.topic[:17] )
    #print ("+++++++++++++")

    print(type(msg.topic[:11]))
    print(type("GIOT-GW/DL/"))

    #if msg.topic[:11] == "GIOT-GW/DL/":
    if msg.topic.startswith("GIOT-GW/DL/"):
        print ("Topic is GIOT-GW/DL/ or not:" + msg.topic[:11])
        sensor_mac = json.loads(json_data)[0]['macAddr']
        sensor_data = json.loads(json_data)[0]['data']
        #sensor_value = bytes.fromhex(sensor_data).decode("utf-8")
        sensor_id = json.loads(json_data)[0]['id']
        sensor_txpara = json.loads(json_data)[0]['extra']['txpara']

    elif msg.topic[:11] == "GIOT-GW/UL/":
        print ("Topic is GIOT-GW/UL/ or not:" + msg.topic[:11])
        sensor_mac = json.loads(json_data)[0]['macAddr']
        sensor_data = json.loads(json_data)[0]['data']
        #sensor_value = bytes.fromhex(sensor_data).decode("utf-8")
        gwid_data = json.loads(json_data)[0]['gwid']
        sensor_snr = json.loads(json_data)[0]['snr']
        sensor_rssi = json.loads(json_data)[0]['rssi']
        sensor_count = json.loads(json_data)[0]['frameCnt']
        print ('Type:' + sensor_type + '\tMac:' + str(sensor_mac)[8:]
              + '\tCount:' + str(sensor_count).rjust(6)
              + '\tSNR:' + str(sensor_snr).rjust(4)
              + '\tRSSI:' + str(sensor_rssi).rjust(4)
              + '\tGWID:' + str(gwid_data).rjust(8))
    else:
        # print (msg.topic+" "+str(msg.payload))
        sensor_mac = '0000000000000000'
        sensor_data = '0000000000000000'

    if msg.topic[:11] == 'GIOT-GW/UL/':
        if str(sensor_mac)[8:] == '0a010068' or str(sensor_mac)[8:] == '14011c65' :
            print('Type:' + sensor_type + '\tMac:' + str(sensor_mac)[8:]
                + '\tCount:' + str(sensor_count).rjust(6)
                + '\tSNR:' + str(sensor_snr).rjust(4)
                + '\tRSSI:' + str(sensor_rssi).rjust(4)
                + '\tGWID:' + str(gwid_data).rjust(8))
    elif msg.topic[:11] == 'GIOT-GW/DL/':
        print('Type:' + sensor_type + '\tMac:' + str(sensor_mac)[8:] + '\tMID:' + str(sensor_id) + '\tTXPara:' + str(sensor_txpara))
    elif msg.topic[:17] == 'GIOT-GW/DL-report':
        print('Response:' + msg.topic[18:] + '\tStatus:' + str(json.loads(json_data)['status']) + '\tID:' + json.loads(json_data)['dataId'])
    else:
        #print (msg.topic + msg.payload)
        print (" msg.topic 0-11 is:" + msg.topic[:11] )
    #if options.display_lcd:
    #    lcd.clear()
    #    lcd.message(str(sensor_mac)[8:]+'C:'+str(sensor_count))
    #    lcd.message('\nS/RSSI' + str(sensor_snr) + '/' + str(sensor_rssi))

    print (" msg.topic 0-11 is:" + msg.topic[:11] )
    print (" msg.topic 0-17 is:" + msg.topic[:17])
    if msg.topic[:11] == 'GIOT-GW/DL/' : #and msg.topic[:17] != 'GIOT-GW/DL-report':
        print("sssssssssssssssssssssssssssssssssss")
        try:
            print ('option --R is worked')
            print ('topic:' + msg.topic)
            print (sensor_data.decode("hex") + str(sensor_mac)[8:].upper())
            if sensor_data.decode("hex") == str(sensor_mac)[8:].upper() and options.downlink:
                print('\x1b[6;30;42m' + 'pub_dl_local.py -i ' + options.host +' -m '+ str(sensor_mac)[8:]+ ' -g ' + str(gwid_data) + ' -c A' +'\x1b[0m')
                lora_restart = raw_input('Stop MQTT subscribe?[Y/n]:') or "y"
                if lora_restart == 'Y' or lora_restart == 'y':
                    sys.exit()
            print('     Payload: ' + sensor_data + ' \x1b[6;30;42m' + 'HEX2ASCII:' + '\x1b[0m' + bytes.fromhex(sensor_data).decode("utf-8"))
        except UnicodeDecodeError:
            print('     Payload: ' + sensor_data)
    if options.long_detail:
        print(json_data)


client = mqtt.Client(protocol=mqtt.MQTTv31)
try:
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(options.username, options.password)
    #print("username/password"+ options.username + options.password)
# 這裏第三個參數可以調整，每個多少時間檢查MQTT 連線狀態，通常60秒已經算短的了，
# 爲了實驗，可以用60秒。2-5分鐘都算合理，google 的 GCM 都28分鐘檢查一次了，
# 在實際量產部署時，要重新考慮這個值，頻寬及Server Load 不是免費啊。

    #print("connect to:" + options.host + str(options.port))
    try:
        client.connect(options.host, options.port, 60)
    except:
        print ('Can not connect to Broker')
        print ('Specify a IP address with option -i.')
        sys.exit()
    client.loop_forever()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("W: interrupt received, stopping...")
#   pass
