import socket
import datetime
from time import sleep
from zeroconf import ServiceInfo, Zeroconf


#HOST = '***ENTER IP ADDRESS HERE***'
HOST = '172.21.0.114'
PORT = 1024        # Port to listen on (non-privileged ports are > 1023)
address = ""

def register_service(zeroconf):

    desc = {'service': 'UbiQ Service', 'version': '1.0.0'}
    #servico, nome servico, endereco, porta, propriedades
    info = ServiceInfo('_ubiq._udp.local.',
                        hostName + '._ubiq._udp.local.',
                        addresses=[socket.inet_aton(HOST)], port=PORT, properties=desc)

    try:
        print("Registration of a UbiQ service")
        zeroconf.register_service(info)
        #print("Discoverable service " + str(desc) + " registered:\n" + str(info))
        print("Discoverable UBIQ service")
        if info:
            print("  Name: ", (info.name))
            print("  Type: ", (info.type))
            print(f"  Server: {info.server}")
            if info.properties:
                print("  Properties are:")
                for key, value in info.properties.items():
                    print(f"    {key}: {value}")
            else:
                print("  No properties")
        else:
            print("  No info")
        print('\n')
        
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Unregistering...")
        zeroconf.unregister_service(info)
        zeroconf.close()

if __name__ == '__main__':
    print("####################################################################")
    print("########################### UBIQ SERVICE ###########################")
    print("####################################################################\n")

    print("Press Ctrl-C to exit\n")

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    hostName = socket.gethostname() 
    serverSocket.bind((HOST, PORT))
    #print("serverSocket: ",serverSocket)
    print("Server started on " + socket.gethostname() + ": " + HOST + ":" + str(PORT) + '\n')

    zeroconf = Zeroconf()
    register_service(zeroconf)
    
