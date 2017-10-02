from bluetooth.ble import BeaconService

import Beacon
import time
import csv
import dbFunctions

dbFunctions.createTable()
input_file = csv.DictReader(open("beaconsRelations.csv"))
beaconsList = []
beaconsRead = []

for row in input_file:
    beaconsList.append(row)
for beacon in beaconsList:
    beacon["state"] = True
    beacon["read"] = False

DISCOVER_TIME = 10 # In seconds, scan interval duration.
service = BeaconService() # Start the service object as beacon service


while True:
    devices = service.scan(DISCOVER_TIME)
    # Scan the devices inside the beacon service
    for address, data in list (devices.items()): # Run for loop for the scanned beacons
        b = Beacon.Beacon(data, address) # Create the object b from class Beacon
        beaconsRead.append(b)
        for beacon in beaconsList:
            if(beacon['BeaconMAC']==b._address ):
                beacon['read'] = True
                if not beacon['state'] and b._rssi>=-70:
                    event = {}
                    event['name'] = beacon['Equipo']
                    event['event'] = 'Entrada'
                    event['date'] = time.time()
                    beacon['state'] = True
                    dbFunctions.insertDeviceEvent(event)
                    print("Entrada leyendo")
                elif  beacon['state'] and b._rssi<=-70:
                    event = {}
                    event['name'] = beacon['Equipo']
                    event['event'] = 'Salida'
                    event['date'] = time.time()
                    beacon['state'] = False
                    dbFunctions.insertDeviceEvent(event)
                    print("Salida leyendo")
    
    for beacon in beaconsList:
        if not beacon['read']:
            if beacon['state']:
                event = {}
                event['name'] = beacon['Equipo']
                event['event'] = 'Salida'
                event['date'] = time.time()
                beacon['state'] = False
                dbFunctions.insertDeviceEvent(event)
                print("Salida no leyendo")
            
        
        
                    
            
        
#index = int(beaconsList.index(filter(lambda n: n.get('BeaconMAC') == str(b._address), beaconsList)[0]))         
 