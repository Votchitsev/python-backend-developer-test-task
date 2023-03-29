"""Основной модуль."""

import asyncio

from fetch_data import fetch_data

if __name__ == '__main__':

    async def main(task_list):
        """Запускает асинхронные функции.

        Args:
            task_list (list): None
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

    tasks = ['task1', 'task2', 'task3']

    asyncio.run(main(tasks))
