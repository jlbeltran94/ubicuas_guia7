from flask import Flask, render_template
import dbFunctions
import time
import csv

app = Flask(__name__)
beaconsList = []
input_file = csv.DictReader(open("beaconsRelations.csv"))
for row in input_file:
    beaconsList.append(row)

@app.route("/")
def main():
    events = dbFunctions.getAllEvents()    
    dates(events)
    return render_template('index.html', events=events)

@app.route("/equipo/<beacon>") # Get <beacon> as input variable for the function sensor
def sensor(beacon):
    equipo = changeString(beacon)
    events = dbFunctions.getAllEventsFrom(equipo)
    dates(events)
        
    return render_template('index.html', events=events)

@app.route("/lastEvent/equipo/<beacon>") # Get <beacon> as input variable for the function sensor
def lastSensor(beacon):
    equipo = changeString(beacon)
    events = dbFunctions.getLastFrom(equipo)
    dates(events)
        
    return render_template('index.html', events=events)

@app.route("/presentes") # Get <beacon> as input variable for the function sensor
def presents():    
    ban = 0      
    nombre = []
    presents = []
    for beacon in beaconsList:
        nombre = dbFunctions.getLastFrom(beacon["Equipo"])        
        if len(presents) > 0:
            if nombre[0]['event'] == "Entrada":
                for p in presents:
                    if(nombre[0]['name'] == p['name']):
                        ban = 1
            else:
                ban = 1
        
            if(ban == 0):
                presents.append(nombre[0])
            else:
                ban = 0                        
        else:
            if nombre[0]['event'] == "Entrada":            
                presents.append(nombre[0])
    print(len(presents))        
    dates(presents)    
    return render_template('index.html', events=presents)

@app.route("/ausentes") # Get <beacon> as input variable for the function sensor
def ausentes():
    ban = 0      
    nombre = []
    presents = []
    for beacon in beaconsList:
        nombre = dbFunctions.getLastFrom(beacon["Equipo"])        
        if len(presents) > 0:
            if nombre[0]['event'] == "Salida":
                for p in presents:
                    if(nombre[0]['name'] == p['name']):
                        ban = 1
            else:
                ban = 1
        
            if(ban == 0):
                presents.append(nombre[0])
            else:
                ban = 0                        
        else:
            if nombre[0]['event'] == "Salida":            
                presents.append(nombre[0])
    print(len(presents))        
    dates(presents)    
    return render_template('index.html', events=presents)

@app.route("/fecha/<fecha>") # Get <beacon> as input variable for the function sensor
def fechas(fecha):
    dateb = changeStringDate(fecha)
    events = dbFunctions.getAllEvents()
    fechas = []
    dates(events)
    for event in events:
        if event['date'] == dateb:
            fechas.append(event)

    return render_template('index.html', events=fechas)

def dates(events):
    for event in events:
        time1 = event['date']
        event['date'] = time.strftime("%Y/%m/%d", time.localtime(time1))

def changeString(name):
    l = list(name)
    for i in range(0, len(l)):
        if l[i] == '_':
            l[i] = ' '                    
    s = "".join(l)    
    return s

def changeStringDate(name):
    l = list(name)
    for i in range(0, len(l)):
        if l[i] == '_':
            l[i] = '/'                    
    s = "".join(l)    
    return s

if __name__ == "__main__":
    app.run()