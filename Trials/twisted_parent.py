from twisted.internet import protocol, reactor

class MyProcessProtocol(protocol.ProcessProtocol):

    def outReceived(self, data):
        print data

proc = MyProcessProtocol()
reactor.spawnProcess(proc, 'child.py',['child.py'])
reactor.run()