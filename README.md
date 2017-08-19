# WorldpayWithin Python SDK

The Python implementation for the Worldpay Within IoT payment SDK. This SDK enables smart devices to discover each other, negogiate a price for services, make a payment (through the Worldpay payments gateway) for services, and then consume services via a 'trusted trigger'. For more information see our documentation website here: http://www.worldpaywithin.com

![The Worldpay Within puzzle piece](http://wptechinnovation.github.io/worldpay-within-sdk/images/architecture/worldpayWithinFig1.png)

## Get started
1. Download this repo
2. Download apache thrift 0.10.0 (latest version)
3. Extract it and change to the lib/py/ directory
4. Run the following command "sudo python setup.py install"
5. Try the examples...

## Run the examples
To try the examples in two different console windows, or if installed on two devices (make sure on same network):
* python runConsumerOWP.py - in one window
* python runProducerOWP.py OR python runProducerCallbacksOWP.py - in the other window
* The two smart devices should communicate with each other and make a payment

## See the payments:
1. Sign up to https://online.worldpay.com if you haven't already done so
2. Got to settings > API keys and get your test keys
3. Replace the keys in the runConsumerOWP.py and producer python files
4. Re-run the examples and you should see the payments coming through on the WPOP (Worldpay Online) payments dashboard

## Debugging:
* If you get some odd error messages talking about a 'rpc-agent'
* Try typing the following command: 'ps -e | grep rpc' to get the pid(s) of rpc-agents that are running. 
* Then do kill <pid> e.g. kill 13249234 to kill these processes.
* Try re-running the examples - if this fails then please contact us at innovation@worldpay.com or on our slack channel or raise an issue in github.
  
## So what does it do:

![The Worldpay Within Flows sequence diagram](http://wptechinnovation.github.io/worldpay-within-sdk/images/architecture/serviceOverview.png)

You can see there are four phases; discover, negotiation, payment and then service delivery, for more information visit our website at http://www.worldpaywithin.com.

## Want to contribute:

Want to contribute, then please clone the repo and create a branch, once you've made your changes create a pull request, we will review your code, and if accepted it will be merged into the code base. You can also raise issues here on github, or contact us direct at innovation@worldpay.com or alternatively join our slack channel at iotpay.slack.com.


  
