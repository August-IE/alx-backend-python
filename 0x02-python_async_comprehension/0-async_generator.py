#!/usr/bin/env python3
"""A coroutine called async_generator that takes no arguments, loops 10 times,
asynchronosly wait 1 second each time, and then yield a random number
between 0 and 10 using the random module"""

import asyncio
import random
import typing


async def async_generator() -> typing.AsyncGenerator[float, None]:
    '''Coroutine that yields a random number between 0 & 10 asynchronously'''
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
