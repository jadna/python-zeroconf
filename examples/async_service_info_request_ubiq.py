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
from zeroconf.asyncio import AsyncServiceInfo, AsyncZeroconf

HAP_TYPE = "_hap._tcp.local."
UBIQ_TYPE = "_ubiq._tcp.local."
SERVICE = UBIQ_TYPE

async def async_watch_services(aiozc: AsyncZeroconf) -> None:
    zeroconf = aiozc.zeroconf
    while True:
        await asyncio.sleep(5)
        infos = []
        for name in zeroconf.cache.names():
            if not name.endswith(SERVICE):
                continue
            infos.append(AsyncServiceInfo(SERVICE, name))
        tasks = [info.async_request(aiozc.zeroconf, 3000) for info in infos]
        await asyncio.gather(*tasks)
        for info in infos:
            print("Info for %s" % (info.name))
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


class AsyncRunner:
    def __init__(self) -> None:

        self.threaded_browser: Optional[ServiceBrowser] = None
        self.aiozc: Optional[AsyncZeroconf] = None

    async def async_run(self) -> None:
        self.aiozc = AsyncZeroconf()
        assert self.aiozc is not None

        def on_service_state_change(zeroconf: Zeroconf, service_type: str, state_change: ServiceStateChange, name: str) -> None:
            """Dummy handler."""

        self.threaded_browser = ServiceBrowser(self.aiozc.zeroconf, [SERVICE], handlers=[on_service_state_change])
        await async_watch_services(self.aiozc)

    async def async_close(self) -> None:
        assert self.aiozc is not None
        assert self.threaded_browser is not None
        self.threaded_browser.cancel()
        await self.aiozc.async_close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    print(f"Services with {SERVICE} will be shown every 5s, press Ctrl-C to exit...")
    loop = asyncio.get_event_loop()
    runner = AsyncRunner()
    try:
        loop.run_until_complete(runner.async_run())
    except KeyboardInterrupt:
        loop.run_until_complete(runner.async_close())
