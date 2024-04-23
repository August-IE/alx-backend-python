#!/usr/bin/env python3
'''Importing async_generator from the previous task and then write
a coroutine called async_comprehension that takes no arguments.
'''

import typing

async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> typing.List[float]:
    '''Coroutine to collect 10 random numbers using async comprehension.'''
    return [rand async for rand in async_generator()]
