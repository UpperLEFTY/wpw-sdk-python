from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
import threading
from wpwithin.WPWithinCallback import Client
from wpwithin.WPWithinCallback import Processor

class CallbackHandler:
    def __init__(self):
        self.log = {}

    def beginServiceDelivery(self, serviceId, serviceDeliveryToken, unitsToSupply):
        try:
            print "event from core - onBeginServiceDelivery()"
            print "ServiceID: {0}\n".format(serviceId)
            print "UnitsToSupply: {0}\n".format(unitsToSupply)
            print "SDT.Key: {0}\n".format(serviceDeliveryToken.key)
            print "SDT.Expiry: {0}\n".format(serviceDeliveryToken.expiry)
            print "SDT.Issued: {0}\n".format(serviceDeliveryToken.issued)
            print "SDT.Signature: {0}\n".format(serviceDeliveryToken.signature)
            print "SDT.RefundOnExpiry: {0}\n".format(serviceDeliveryToken.refundOnExpiry)
        except Exception as e:
            print "doBeginServiceDelivery failed: " + str(e)

    def endServiceDelivery(self, serviceId, serviceDeliveryToken, unitsReceived):
        try:
	        print "event from core - onEndServiceDelivery()"
	        print "ServiceID: {0}\n".format(serviceId)
	        print "UnitsReceived: {0}\n".format(unitsReceived)
	        print "SDT.Key: {0}\n".format(serviceDeliveryToken.key)
	        print "SDT.Expiry: {0}\n".format(serviceDeliveryToken.expiry)
	        print "SDT.Issued: {0}\n".format(serviceDeliveryToken.issued)
	        print "SDT.Signature: {0}\n".format(serviceDeliveryToken.signature)
	        print "SDT.RefundOnExpiry: {0}\n".format(serviceDeliveryToken.refundOnExpiry)
        except Exception as e:
	        print "doEndServiceDelivery failed: " + str(e)

class EventServer:
    server = None

    def startServer(self, server):
    	print "##### STARTING WRAPPER SERVER to receive callbacks #####"
    	print "##### SERVER: " + str(server)
    	server.serve()

    def stop():
        if server != None:
            server.setShouldStop(True)

    def __init__(self, listenerHandler, hostname, port):
        try:
            if(listenerHandler == None):
                print "Using build-in handler"
                theListenerToUse = CallbackHandler()
            else:
                print "Using custom handler"
                theListenerToUse = listenerHandler
            processor = Processor(theListenerToUse)
            transport = TSocket.TServerSocket(host=hostname, port=port)
            tfactory = TTransport.TBufferedTransportFactory()
            pfactory = TBinaryProtocol.TBinaryProtocolFactory()
            #self.server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
            self.server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
            print "Serving the Wrapper listener, port: " + str(port)
            thread = threading.Thread(target=self.startServer, args=([self.server]))
            thread.daemon = True                            # Daemonize thread
            thread.start()                                  # Start the execution
            print "##### SERVER: " + str(self.server)
            print "##### SERVER: SHOULD HAVE STARTED"
            print "Should have started Wrapper listener"
        except Exception as e:
            print "Event server setup failed: " + str(e)


