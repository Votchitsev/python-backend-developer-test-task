"""Tests."""
import asyncio
import os

from hash_counter import run_fetch_data
from main import start


def test_main():
    asyncio.run(start(['task1', 'task2', 'task3']))

    assert os.path.exists('./result/task1')
    assert os.path.exists('./result/task1/README.md')
    assert os.path.exists('./result/task2')
    assert os.path.exists('./result/task2/nitpick')
    assert os.path.exists('./result/task3/nitpick/all.toml')

    os.remove('./result/hash.txt')


def test_hash_counter():
    run_fetch_data(['task1', 'task2', 'task3'])
    equal_lines_number = 30

    with open('./result/hash.txt', 'r') as hash_file:
        lines = sum(1 for _ in hash_file)

        assert lines == equal_lines_number
