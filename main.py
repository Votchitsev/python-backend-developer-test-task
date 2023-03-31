"""Основной модуль."""

import asyncio

from fetch_data import fetch_data
from hash_counter import run


async def start(task_list: list) -> None:
    """Запускает асинхронные функции.

    Args:
        task_list: (list) list of creating dirs
    """
    url = (
        'https://gitea.radium.group/api/v1/repos/' +
        'radium/project-configuration/contents/?ref=HEAD'
    )

    started_tasks = []

    for task in task_list:
        started_tasks.append(asyncio.create_task(fetch_data(url, task)))

    for started_task in started_tasks:
        await started_task

    run(task_list)


asyncio.run(start(['task1', 'task2', 'task3']))
