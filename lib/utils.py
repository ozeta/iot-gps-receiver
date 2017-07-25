from machine import I2C
import _thread
import time
from machine import UART
from machine import Timer

import struct
import socket
from network import Bluetooth
import gc

I2C16= const(16)
_GPS_=const(2)
_BT_=const(1)
_START_=const(1)
_CR_=const(2)
_LF_=const(3)
_STOP_=const(0)






GPS_Is_Fixed=False
StartGPS=_STOP_
StopGPS=0
sentence=''
GPSlat=[0, 0, 'N']
GPSlon=[0, 0, 'S']
GPSDEBUG=False


#############################################
#  Fonction DecodeGPS // decode les infos utiles dans les trames GPS
#############################################    
def DecodeGPS(sentence):
    
    
    global GPSlat
    global GPSlon
    global GPSDEBUG
    global GPS_Is_Fixed
    index_lat=0
    index_lon=0    
    tosplit=False
    Array=sentence.split(',')
    if Array[0]=='$GPGGA' and len(Array)>6 and (Array[3]=='N' or Array[3]=='S' ) and (Array[5]=='E' or Array[5]=='W') :
                        if Array[6]=='1':
                            index_lat=2
                            index_lon=4
                            tosplit=True
                            
                            if GPSDEBUG==True:
                                print ('Valid data on GPGGA')
                        
    if  (Array[0]=='$GNGLL' or Array[0]=='$GPGLL') and len(Array)>6 and (Array[2]=='N' or Array[2]=='S' )  and (Array[4]=='E' or Array[4]=='W') :
                        if Array[6]=='A':
                            index_lat=1
                            index_lon=3
                            tosplit=True
                            
                            if GPSDEBUG==True:
                                print ('Valid data on ..GLL')
                            
    if (Array[0]=='$GNRMC' or Array[0]=='$GPRMC') and len (Array)>8   and (Array[4]=='N' or Array[4]=='S')  and (Array[6]=='E' or Array[6]=='W') :
                        if Array[2]=='A':
                            index_lat=3
                            index_lon=5
                            tosplit=True
                            
                            if GPSDEBUG==True:
                                print ('Valid data on ..RMC')
                    
    if tosplit==True:
                        coord=Array[index_lat].split('.')
                        GPSlat[0]=int(coord[0][:len(coord[0])-2])
                        GPSlat[1]=int(coord[0][-2:])+float('0.'+coord[1])
                        GPSlat[2]=Array[index_lat+1]
                        coord=Array[index_lon].split('.')
                        GPSlon[0]=int(coord[0][:len(coord[0])-2])
                        GPSlon[1]=int(coord[0][-2:])+float('0.'+coord[1])
                        GPSlon[2]=Array[index_lon+1]    
                        GPS_Is_Fixed=True
    
    
    
#############################################
#  Fonction Thread du GPS TYPE  G76_L   pytrack
#############################################
def th_G76_L(id):
        global StopGPS
        global StartGPS
        global GPSDEBUG
        sentence=''
        i2c = I2C(0, baudrate=100000, pins=('P22', 'P21'))    
        
        while True:
            data=i2c.readfrom(I2C16, 1)

            if data==b'$':  
                gc.collect()
                sentence='$'                
                StartGPS=_START_

    
            while StartGPS==_START_:
#        my_gps.update(chr(data)) 
                data=i2c.readfrom(I2C16, 1)
                for x in data:
                    if x!=13 and x!=10:                                            
                        if StopGPS==1:
                            StopGPS=0
                        sentence=sentence+chr(x)
        
#        SUR CR ON AMMORCE L ARRET DE STRING
                if x==13:
                    StopGPS=1
            
#            SUR LF APRES UN CR ON STOP la phrase ou supérieure a 82 char
                if x==10 and StopGPS==1: 
                    StartGPS=_STOP_
                    if GPSDEBUG==True:                    
                        print(sentence)
                    DecodeGPS(sentence)
                    
#                    on as un cr/lf ,  on lache un peut de temps au autre process
                    time.sleep_ms(300)
                    
  #############################################
#  Fonction Thread du GPS TYPE  ublox Neo 6  ( doit fonctionner avec tous les GPS serie
#############################################

def th_M6N(id):
    tempsen=''
    sentence=''
    com = UART(1,pins=('P12', 'P11'),  baudrate=9600) 
    while True:
        gc.collect()
        if com.any():
            tempsen=com.readline()           
            for x in tempsen:
                if chr(x)=='$':
                    if len(sentence)>15:   #$GPGGA,,,,,,
                        if GPSDEBUG==True:
                            print(sentence)                    
                        DecodeGPS(sentence)            
                        sentence=''
                                
#                    début de la sentence                
                if x!=13 and x!=10:
                    sentence=sentence+chr(x)                    
        time.sleep_ms(300)
                    
#############################################
#  DEMARAGE du GPSSTART avec deux type 'M6N' et 'G76-L' ( serie et I2C)
#############################################                    
def GPSstart(GPSTYPE):
       # Initialize the I2C bus
    if GPSTYPE=='M6N':
         _thread.start_new_thread(th_M6N,(12, ))   
    if GPSTYPE=='G76-L':
        _thread.start_new_thread(th_G76_L,(12, ))
        
