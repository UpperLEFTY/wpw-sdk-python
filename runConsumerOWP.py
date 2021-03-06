import wpwithinpy.WPWithinWrapperImpl as WPWithinWrapperImpl
import wpwithinpy.WWTypes as WWTypes
import time
import os
import signal
import jsoncfg


def killTheRpcAgent():
    print "Will attempt to kill the rpc-agent - this will now be handled by the SDK"

def discoverDevices(): # throws WPWithinGeneralException {
    devices = wpw.deviceDiscovery(8000)
    if devices != None and len(devices) > 0: 
        print "{0} services found:\n".format(len(devices))
        for svcMsg in devices:
            print "Device Description: {0}\n".format(svcMsg.getDeviceDescription())
            print "Hostname: {0}\n".format(svcMsg.getHostname())
            print "Port: {0}\n".format(svcMsg.getPortNumber())
            print "URL Prefix: {0}\n".format(svcMsg.getUrlPrefix())
            print "ServerId: {0}\n".format(svcMsg.getServerId())
            print "Scheme: {0}\n".format(svcMsg.getScheme()) # debb kev this has gone missing...?
            print "--------"
    else:
        if devices != None:
            print "No services found... devices was None"
        else:
            print "No services found... devices length: " + len(devices)
    return devices

def connectToDevice(svcMsg): # throws WPWithinGeneralException {

    card = WWTypes.WWHCECard()
    card.setFirstName(config.hceCard.firstName())
    card.setLastName(config.hceCard.lastName())
    card.setCardNumber(config.hceCard.cardNumber())
    card.setExpMonth(config.hceCard.expMonth())
    card.setExpYear(config.hceCard.expYear())
    card.setType(config.hceCard.type())
    card.setCvc(config.hceCard.cvc())

    wpw.initConsumer("http://", svcMsg.getHostname(), svcMsg.getPortNumber(), svcMsg.getUrlPrefix(), svcMsg.getServerId(), card, config.pspConfig())

def getAvailableServices(): #throws WPWithinGeneralException {
    services = wpw.requestServices()
    print "{0} services found\n".format(len(services))
    if services != None and len(services) > 0:
        for svc in services:
            print "Service:"
            print "Id: {0}\n".format(svc.getServiceId())
            print "Description: {0}\n".format(svc.getServiceDescription())
            print "------"
    return services

def getServicePrices(serviceId): # throws WPWithinGeneralException {
    prices = wpw.getServicePrices(serviceId)
    print "{1} prices found for service id {1}\n".format(len(prices), serviceId)
    if prices != None and len(prices) > 0:
        for price in prices:
            print "Price: {0:.2f}".format(float(price.pricePerUnit.amount) / float(100))
            print "CurrencyCode: " + price.pricePerUnit.currencyCode
            print "Id: {0}\n".format(price.getId())
            print "Description: {0}\n".format(price.getDescription())
            print "UnitId: {0}\n".format(price.getUnitId())
            #print "UnitDescription: {0}\n".format(price.getUnitDescription()) #not likey this some reason
            #print "Unit Price Amount: {10.2f}\n".format(price.getPricePerUnit().getAmount()) #not likey this... :(
            #print "Unit Price CurrencyCode: {0}\n".format(price.getPricePerUnit().getCurrencyCode()) #not likey this either...
            print "------"
    return prices

def getServicePriceQuote(serviceId, numberOfUnits, priceId): # throws WPWithinGeneralException {
    tpr = wpw.selectService(serviceId, numberOfUnits, priceId)
    if tpr != None:
            print "Did retrieve price quote:"
            print "Merchant client key: {0}\n".format(tpr.getMerchantClientKey())
            print "Payment reference id: {0}\n".format(tpr.getPaymentReferenceId())
            print "Units to supply: {0}\n".format(tpr.getUnitsToSupply())
            #print "Currency code: {0}\n".format(tpr.getCurrencyCode()) #TODO fix this
            print "Total price: {0:.2f}\n".format(float(tpr.getTotalPrice())/float(100))
    else:
        print "Result of select service is None"
    return tpr

def purchaseService(serviceId, pReq): # throws WPWithinGeneralException {
    pResp = wpw.makePayment(pReq)
    sdt = pResp.getServiceDeliveryToken()
    if pResp != None:

            print 'Payment response:'
            print "Total paid: {0:.2f}\n".format(float(pResp.getTotalPaid())/float(100))
            print "ServiceDeliveryToken.issued: {0}\n".format(sdt.getIssued()) #not coming through right
            print "ServiceDeliveryToken.expiry: {0}\n".format(sdt.getExpiry())
            print "ServiceDeliveryToken.key: %{0}\n".format(sdt.getKey())
            print "ServiceDeliveryToken.signature: {0}\n".format(sdt.getSignature())
            print "ServiceDeliveryToken.refundOnExpiry: {0}\n".format(sdt.getRefundOnExpiry())
            beginServiceDelivery(serviceId, sdt, 5)
    else:
        print 'Result of make payment is None..'
    return pResp

def beginServiceDelivery(serviceID, token, unitsToSupply): # throws WPWithinGeneralException {
    print 'Calling beginServiceDelivery()'
    print str(token)
    if token == None:
        print "Token empty at runConsumer side"
    else:
        print "Token not empty at runConsumer side"
    wpw.beginServiceDelivery(serviceID, token, unitsToSupply)
    print 'Sleeping 10 seconds..'
    try:
        time.sleep(10)
    except IOError:
        pass
    endServiceDelivery(serviceID, token, unitsToSupply)

def endServiceDelivery(serviceID, token, unitsReceived): # throws WPWithinGeneralException {
    print 'Calling endServiceDelivery()'
    wpw.endServiceDelivery(serviceID, token, unitsReceived)

def run():

    print 'Starting Consumer Example Written in Python.'
    global wpw
    global config

    print 'Load configuration.'
    config = jsoncfg.load_config('config/consumerOWP.json')

    wpw = WPWithinWrapperImpl.WPWithinWrapperImpl(config.host(), config.port(), False)
    try:
        wpw.setup("my-device", "an example consumer device")
        wpwDevice = wpw.getDevice()
        print "::" + wpwDevice.getUid() + ":" + wpwDevice.getName() + ":" + wpwDevice.getDescription() + ":" + str(wpwDevice.getServices()) + ":" + wpwDevice.getIpv4Address() + ":" + wpwDevice.getCurrencyCode()
        if wpwDevice != None:
            print "Successfully got a device"
            devices = discoverDevices()
            if devices != None:
                onlyRunOnce = 0
                for svcMsg in devices:
                    # Should pick the first device discovered
                    onlyRunOnce = onlyRunOnce + 1
                    connectToDevice(svcMsg)
                    svcDetails = getAvailableServices()
                    onlyRunOnce2 = 0
                    if svcDetails != None:
                        for svcDetail in svcDetails:
                            onlyRunOnce2 = onlyRunOnce2 + 1
                            svcPrices = getServicePrices(svcDetail.getServiceId())
                            if svcPrices != None:
                                onlyRunOnce3 = 0
                                for svcPrice in svcPrices:
                                    onlyRunOnce3 = onlyRunOnce3 + 1
                                    #Select the first price in the list
                                    tpr = getServicePriceQuote(svcDetail.getServiceId(), 6, svcPrice.getId())
                                    print 'Client ID: {0}\n'.format(tpr.getClientId())
                                    print 'Server ID: {0}\n'.format(tpr.getServerId())
                                    paymentResponse = purchaseService(svcDetail.getServiceId(), tpr)
                                if onlyRunOnce3 != 0:
                                    break
                        if onlyRunOnce2 != 0:
                            break
                    if onlyRunOnce != 0:
                        break
        else:
            print "Could not get device"
        wpw.stopRPCAgent()
    except WWTypes.WPWithinGeneralException as wpge:
        # killTheRpcAgent()
        print wpge
    except Exception as wpge2:
        # killTheRpcAgent()
        print wpge2
run()
