from twisted.application import service, internet
from twisted.internet import reactor
from twisted.internet import task
from twisted.internet.protocol import ProcessProtocol

class Process(ProcessProtocol):
    def __init__(self):
        self.data = ''
        self.pid = None
    def connectionMade(self):
        self.pid = self.transport.pid
        print "opened processes %s..." % self.pid
        self.transport.closeStdin()
    def outReceived(self, data):
        print "received data from process %d (%d bytes)" % (self.pid, len(data))
        self.data = self.data + data
    def processEnded(self, status_object):
        print "process %d complete (status %d)" % (self.pid, status_object.value.exitCode)
        print self.data
    def errReceived(self, data): pass
    def outConnectionLost(self): pass
    def errConnectionLost(self): pass

class TextEchoClient(Process):
    def processEnded(self, status_object):
        self.data

def getProcessMonitors(count):
    processes = []
    for i in range(0, count+1):
        command = '/bin/echo'
        params = 'data: yes'
        binary = 'echo'
        process = TextEchoClient()
        options = [command, params]
        processes.append((process, binary, options))
    #print processes
    return processes

INTERVAL = 20

def runTest():
  [ reactor.spawnProcess(*x) for x in getProcessMonitors(30) ]

application = service.Application("pymon")
pymonServices = service.IServiceCollection(application)
server = internet.TimerService(INTERVAL, runTest)
server.setServiceParent(pymonServices)