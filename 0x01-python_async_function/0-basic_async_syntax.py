#!/usr/bin/env python3
'''An asynchronous coroutine that takes in an integer argument named
`wait_random` waits for a random delay for seconds and eventually returns it.
'''

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    '''Waits for a random delay between 0 and max_delay seconds.'''
    wait_seconds = random.uniform(0, max_delay)
    await asyncio.sleep(wait_seconds)
    return wait_seconds
