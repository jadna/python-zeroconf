#!/usr/bin/env python3
"""Example of perodic dump of homekit services.
This example is useful when a user wants an ondemand
list of HomeKit devices on the network.
"""
import argparse
import asyncio
import logging
from typing import Any, Optional, cast
from zeroconf import IPVersion, ServiceBrowser, ServiceStateChange, Zeroconf
from zeroconf.asyncio import AsyncServiceInfo, AsyncZeroconf, AsyncServiceBrowser,  AsyncZeroconfServiceTypes

#HAP_TYPE = "_hap._tcp.local."
#HAP_TYPE = "_airplay._tcp.local."

async def async_watch_services(aiozc: AsyncZeroconf, HAP_TYPE) -> None:
    zeroconf = aiozc.zeroconf
    while True:
        await asyncio.sleep(5)
        infos = []
        for name in zeroconf.cache.names():
            if not name.endswith(HAP_TYPE):
                continue
            infos.append(AsyncServiceInfo(HAP_TYPE, name))
        tasks = [info.async_request(aiozc.zeroconf, 3000) for info in infos]
        await asyncio.gather(*tasks)
        for info in infos:
            print("Info for %s" % (info.name))
            if info:
                addresses = ["%s:%d" % (addr, cast(int, info.port)) for addr in info.parsed_addresses()]
                print("  Addresses: %s" % ", ".join(addresses))
                print("  Weight: %d, priority: %d" % (info.weight, info.priority))
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


class AsyncRunner:
    
    def __init__(self) -> None:

        self.threaded_browser: Optional[ServiceBrowser] = None
        self.aiozc: Optional[AsyncZeroconf] = None

    async def async_run(self) -> None:
        self.aiozc = AsyncZeroconf()
        assert self.aiozc is not None

        def on_service_state_change(zeroconf: Zeroconf, service_type: str, state_change: ServiceStateChange, name: str) -> None:
            """Dummy handler."""

        HAP_TYPES = list( await AsyncZeroconfServiceTypes.async_find(aiozc=self.aiozc))
        print(HAP_TYPES)

        for HAP_TYPE in HAP_TYPES:
            self.threaded_browser = ServiceBrowser(self.aiozc.zeroconf, [HAP_TYPE], handlers=[on_service_state_change])
            await async_watch_services(self.aiozc, HAP_TYPE)

    async def async_close(self) -> None:
        assert self.aiozc is not None
        assert self.threaded_browser is not None
        self.threaded_browser.cancel()
        await self.aiozc.async_close()


if __name__ == '__main__':
    
    #print(f"Services with {HAP_TYPES} will be shown every 5s, press Ctrl-C to exit...")
    print(f"Services will be shown every 5s, press Ctrl-C to exit...")
    loop = asyncio.get_event_loop()
    runner = AsyncRunner()
    try:
        loop.run_until_complete(runner.async_run())
    except KeyboardInterrupt:
        loop.run_until_complete(runner.async_close())
