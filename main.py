"""Main module."""

import asyncio

from fetch_data import run_fetch_data
from hash_counter import run_hash_counter


async def start(task_list: list) -> None:
    """Run the script.

    Args:
        task_list: (list) list of creating dirs
    """
    url = (
        'https://gitea.radium.group/api/v1/repos/' +
        'radium/project-configuration/contents/?ref=HEAD'
    )

    started_tasks = []

    for task in task_list:
        started_tasks.append(asyncio.create_task(run_fetch_data(url, task)))

    for started_task in started_tasks:
        await started_task

    run_hash_counter(task_list)


asyncio.run(start(['task1', 'task2', 'task3']))
