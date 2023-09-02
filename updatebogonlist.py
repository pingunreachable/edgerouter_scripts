#!/usr/bin/python3
from netmiko import ConnectHandler
from datetime import date
import requests

net_connect = ConnectHandler(
device_type="ubiquiti_edgerouter", host="xxx.xxx.xxx.xxx", username="xxxx", password="xxxx",)

downloadbogonlist = requests.get('https://team-cymru.org/Services/Bogons/bogon-bn-nonagg.txt')
#downloadbogonlist = requests.get('https://team-cymru.org/Services/Bogons/fullbogons-ipv4.txt')
bogonlistfile = open("bogonlistfile.txt",'w')
bogonlistfile.write(downloadbogonlist.text)
bogonlistfile.close()
print (downloadbogonlist.text)

bogonlistfile = open("bogonlistfile.txt",'r')
filedate = date.today()
filedate = filedate.strftime("%d/%m/%Y")
descriptionmsg = "Bogon_list Updated"
fwgroupname = "Bogon_list"

uploadcmd = net_connect.send_config_set(f"set firewall group network-group {fwgroupname} description \'{descriptionmsg} {filedate}\'")

print (uploadcmd)

for bogonip in bogonlistfile:
    uploadcmd =  net_connect.send_config_set(f"set firewall group network-group {fwgroupname} network {bogonip}")
    print (uploadcmd)

print (net_connect.send_command("commit; save"))
