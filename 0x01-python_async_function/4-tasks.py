#!/usr/bin/env python3
'''Modifying the code from wait_n into a new version task_wait_n.
'''
import asyncio
from typing import List


task_wait_random = __import__('3-tasks').task_wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    '''Calculates task_wait_random n times.'''
    wait_times_tasks = [task_wait_random(max_delay) for _ in range(n)]
    wait_times = await asyncio.gather(*wait_times_tasks)
    return sorted(wait_times)
