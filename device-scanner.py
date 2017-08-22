from wpwithinpy import WPWithinWrapperImpl
from wpwithinpy import WWTypes
import os
import json
import time


global data2
data2 = []

def killRpcAgent():
    killCommand = "ps aux | grep -i 'rpc-agent.*port.*8778' | awk '{print $2}' | xargs kill -9"
    # Finding the process based on the port number is safer than relying on the pid number that it was started on
    os.system(killCommand)

def resetJson():
    data3 = []
    try:
        with open('/Library/WebServer/Documents/worldpaywithin/device-scanner.json', 'w') as outfile:
            json.dump(data3, outfile)
    except Exception:
        print "You need to configure the webserver path if you want to output json"

def outputJson(svcMsg):
    global data2
    data2 = data2 + [{    'serverid' : svcMsg.getServerId(),
                            'devicedescription' : svcMsg.getDeviceDescription(),
                            'hostname' : svcMsg.getHostname(),
                            'portnumber' : svcMsg.getPortNumber(),
                            'urlprefix' : svcMsg.getUrlPrefix()
                            }]
    try:
        with open('/Library/WebServer/Documents/worldpaywithin/device-scanner.json', 'w') as outfile:
            json.dump(data2, outfile)
    except Exception:
        print "You need to configure the webserver path if you want to output json"


def scanOnce():
    global data2
    data2 = []
    #resetJson()
    flagScanTimeout = 5000
    print 'Starting Device Scanner Written in Python.'
    global wpw
    wpw = WPWithinWrapperImpl.WPWithinWrapperImpl('127.0.0.1', 8778, False)
    try:
        wpw.setup("kevingwp-pi", "Kevin Gordons Raspberry Pi - DEVICE SCANNER")
        wpwDevice = wpw.getDevice()
        print "::" + wpwDevice.getUid() + ":" + wpwDevice.getName() + ":" + wpwDevice.getDescription() + ":" + str(wpwDevice.getServices()) + ":" + wpwDevice.getIpv4Address() + ":" + wpwDevice.getCurrencyCode()
        print "Scanning network for devices now..."
        print "Will scan for " + str(flagScanTimeout) + " milliseconds\n"

        if wpwDevice != None:
            devices = wpw.deviceDiscovery(flagScanTimeout)    
            if devices != None:

                if len(devices) > 0:

                    print "------------------------------------------------------------"
                    print "Found " + str(len(devices)) + " devices\n"

                    for svcMsg in devices:
                       print "[" + svcMsg.getServerId() + "] " + svcMsg.getDeviceDescription() + " @ " + svcMsg.getHostname() + ":" + str(svcMsg.getPortNumber()) + "" + svcMsg.getUrlPrefix() + "\n"					
                       outputJson(svcMsg)

                    print "------------------------------------------------------------"
                else:
                    resetJson();
            else:
                resetJson();
                         
        wpw.stopRPCAgent()
    except WWTypes.WPWithinGeneralException as wpge:
        killRpcAgent()
        print wpge
    except Exception as wpge2:
        killRpcAgent()
        print wpge2
 
def run():
    while True:
        scanOnce()
        time.sleep(3)

run()
