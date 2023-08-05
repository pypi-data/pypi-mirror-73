from braviarc import BraviaRC
import json

with open('/home/dave/.homeassistant/.storage/core.config_entries','r') as fh:
    data = json.loads(fh.read()).get('data',{})
    entries = data.get('entries',[])
    for entry in entries:
        if 'XBR-65X900B' == entry.get('title'):
            tv_data = entry.get('data')
    if tv_data:
        tv = tv_data['host'],tv_data['mac']
        # print(tv)


a = BraviaRC('192.168.1.102', '38:B1:DB:11:86:75')

print(a.is_connected())
a.turn_on()
a.connect("6870","deleteMe","delete_me")
#a.turn_off()
print(a.get_power_status())
a._cookies=None
print(a.is_connected())