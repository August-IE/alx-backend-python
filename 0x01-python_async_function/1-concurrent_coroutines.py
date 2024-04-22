#!/usr/bin/env python3

'''An async routine called wait_n that takes in 2 int arguments in a given
order, spawn wait_random n times with the specified max_delay.
wait_n returns the list of all the delays (float values) which should be in
ascending order without using sort() because of concurrency.
'''

import asyncio
from typing import List
from random import random


async def wait_random(max_delay: int = 10) -> float:
    '''Waits for a random delay between 0 and max_delay seconds.'''
    return random() * max_delay


async def wait_n(n: int, max_delay: int) -> List[float]:
    '''Return the list of all the delays (float values)'''
    tasks = [wait_random(max_delay) for _ in range(n)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    delays = [result for result in results if not
              isinstance(result, Exception)]
    return sorted(delays)
