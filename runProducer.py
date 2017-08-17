import WPWithinWrapperImpl
import WWTypes
import time
import os

# Handy method to kill any rpc-agent that still exists
def clearDownRpc():
   os.system('killall rpc-agent') 

def run():
	try:
		print "WorldpayWithin Sample Producer..."
		global wpw
		wpw = WPWithinWrapperImpl.WPWithinWrapperImpl('127.0.0.1', 9090, False)
		wpw.setup("Producer Example", "Example WorldpayWithin producer")		
		svc = WWTypes.WWService();
		svc.setName("Car charger")
		svc.setDescription("Can charge your hybrid / electric car")
		svc.setId(1)
		ccPrice = WWTypes.WWPrice()
		ccPrice.setId(1)
		ccPrice.setDescription("Kilowatt-hour")
		ccPrice.setUnitDescription("One kilowatt-hour")
		ccPrice.setUnitId(1)
		ppu = WWTypes.WWPricePerUnit()
		ppu.setAmount(25)
		ppu.setCurrencyCode("GBP")
		ccPrice.setPricePerUnit(ppu)
		prices = {}
		prices[ccPrice.getId()] = ccPrice
		svc.setPrices(prices)
		print "WorldpayWithin Sample Producer: About to init the producer with crendentials"
		# [ CLIENT KEY, SERVICE KEY] : From online.worldpay.com
		wpw.initProducer({"psp_name":"securenet","developer_id":"12345678", "secure_key": "<secure_key>", "api_endpoint":"https://gwapi.demo.securenet.com/api/", "public_key": "<public_key>", "secure_net_id":"<secure_net_id>", "app_version":"0.1", "merchant_client_key": "<public_key>", "merchant_service_key": "<secure_key>","hte_public_key":"<public_key>", "hte_private_key": "<secure_key>"})
		print "WorldpayWithin Sample Producer: Adding service"
		wpw.addService(svc)
		broadcastDuration = 20000
		durationSeconds = broadcastDuration / 1000
		print "WorldpayWithin Sample Producer: Starting broadcast..."		
		wpw.startServiceBroadcast(broadcastDuration) #20000
		repeat = 0
		while repeat < durationSeconds:
		    print "Producer Waiting " + str(durationSeconds - repeat) + " seconds to go..."
		    time.sleep(1)
		    repeat = repeat + 1
		print "Stopped broadcasting, RPC still running"
		repeat2 = 0
		while repeat2 < 99999999999:
		    print "Producer keeping alive (to receive callbacks...)"
		    time.sleep(1)
		    repeat2 = repeat2 + 1        
	except WWTypes.WPWithinGeneralException as e:
		print e

clearDownRpc()
run()
