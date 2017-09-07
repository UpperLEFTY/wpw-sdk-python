import launcher
import os
import logging
import sys

def startRPC(self, port, eventListenerPort):
  
  logging.basicConfig(filename='worldpay-within-wrapper.log',level=logging.DEBUG)
  reqOS = ["darwin", "win32", "windows", "linux"]
  reqArch = ["x64", "ia32"]
  cfg = launcher.Config(reqOS, reqArch);
  launcherLocal = launcher.launcher()
  # define log file name for rpc agent, so e.g
  # for "runConsumerOWP.py" it will be: "rpc-wpwithin-runConsumerOWP.log"
  logfilename = os.path.basename(sys.argv[0])
  logfilename = "rpc-wpwithin-" + logfilename.rsplit(".", 1)[0] + ".log"
  if eventListenerPort > 0:
      callbackPortString = " -callbackport=" + str(eventListenerPort)
  else:
  	  callbackPortString = ""
  
  logging .debug(str(os.getcwd()) + "" + "-port " + str(port) + " -logfile " + logfilename + " -loglevel debug,warn,error,fatal,info" + str(callbackPortString))
  process = launcherLocal.launch(cfg, os.getcwd() + "", "-port " + str(port) + " -logfile " + logfilename + " -loglevel debug,warn,error,fatal,info" + str(callbackPortString))
  
  return process

def stopRPC(self, process):
  print "Will try and stop RPC service"
  process.kill()