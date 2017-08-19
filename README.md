# WorldpayWithin Python SDK

The Python implementation for the Worldpay Within IoT payment SDK. This SDK enables smart devices to discover each other, negogiate a price for services, make a payment (through the Worldpay payments gateway) for services, and then consume services via a 'trusted trigger'. For more information see our documentation website here: http://www.worldpaywithin.com

Get stared
1. Download this repo
2. Download apache thrift 0.10.0 (latest version)
3. Extract it and change to the lib/py/ directory
4. Run the following command "sudo python setup.py install"
5. Try the examples...

To try the examples in two different console windows, or if installed on two devices (make sure on same network):
* python runConsumerOWP.py - in one window
* python runProducerOWP.py OR python runProducerCallbacksOWP.py - in the other window
* The two smart devices should communicate with each other and make a payment

See the payments:
1. Sign up to https://online.worldpay.com if you haven't already done so
2. Got to settings > API keys and get your test keys
3. Replace the keys in the runConsumerOWP.py and producer python files
4. Re-run the examples and you should see the payments coming through on the WPOP (Worldpay Online) payments dashboard

Debugging:
* If you get some odd error messages talking about a 'rpc-agent'
* Try typing the following command: 'ps -e | grep rpc' to get the pid(s) of rpc-agents that are running. 
* Then do kill <pid> e.g. kill 13249234 to kill these processes.
* Try re-running the examples - if this fails then please contact us at innovation@worldpay.com or on our slack channel or raise an issue in github.
  
