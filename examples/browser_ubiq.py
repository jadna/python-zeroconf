import argparse
import logging
from time import sleep
from typing import cast
from zeroconf import IPVersion, ServiceBrowser, ServiceStateChange, Zeroconf, ZeroconfServiceTypes

# _find._tcp.local. encontra todos os serviços disponiveis
HOMESHARING_SERVICE: str = "_appletv-v2._tcp.local."
DEVICE_SERVICE: str = "_touch-able._tcp.local."
MEDIAREMOTE_SERVICE: str = "_mediaremotetv._tcp.local."
AIRPLAY_SERVICE: str = "_airplay._tcp.local."
COMPANION_SERVICE: str = "_companion-link._tcp.local."
RAOP_SERVICE: str = "_raop._tcp.local."
AIRPORT_ADMIN_SERVICE: str = "_airport._tcp.local."
DEVICE_INFO_SERVICE: str = "_device-info._tcp.local."
HTTP_SERVICE: str = "_http._tcp.local."
HAP_SERVICE: str = "_hap._tcp.local."
FIND_SERVICE: str = "_find._tcp.local."
UBIQ_SERVICE: str = "_ubiq._udp.local."

ALL_SERVICES = [
    HOMESHARING_SERVICE,
    DEVICE_SERVICE,
    MEDIAREMOTE_SERVICE,
    AIRPLAY_SERVICE,
    COMPANION_SERVICE,
    RAOP_SERVICE,
    AIRPORT_ADMIN_SERVICE,
    DEVICE_INFO_SERVICE,
    HTTP_SERVICE,
    HAP_SERVICE,
    FIND_SERVICE,
    UBIQ_SERVICE,
]

def browser_services(zeroconf):

    #Busca uma lista com os serviços disponiveis
    #services = list(ZeroconfServiceTypes.find(zc=zeroconf))
    services = ALL_SERVICES

    print("Found %d service(s)" % len(services))
    print(f"Services: {services}" + "\n")

    browser = ServiceBrowser(zeroconf, services, handlers=[on_service_state_change])


def on_service_state_change(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange) -> None:

    print(f"Service {name} of type {service_type} state changed: {state_change}")

    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        #print("Info from zeroconf.get_service_info: %r\n" % (info))

        if info:
            addresses =['%s:%d' % (addr, cast(int, info.port)) for addr in info.parsed_scoped_addresses()]
            print("  -> Name: ", (info.name))
            print("  -> Type: ", (info.type))
            print("  -> Addresses: %s" % ", ".join(addresses))
            print("  -> Weight: %d, priority: %d" % (info.weight, info.priority))
            print(f"  -> Server: {info.server}")
            if info.properties:
                print("  -> Properties are:")
                for key, value in info.properties.items():
                    print(f"    ->> {key}: {value}")
            else:
                print("  No properties")
        else:
            print("  No info")
        print('\n')

if __name__ == '__main__':

    print("####################################################################")
    print("##################### FINDING THE UBIQ SERVICE #####################")
    print("####################################################################\n")
    print("Press Ctrl-C to exit\n")

    zeroconf = Zeroconf()
    try:
        browser_services(zeroconf)
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()
    
