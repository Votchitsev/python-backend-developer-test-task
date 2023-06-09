"""Tests."""
import asyncio
import os
import shutil

from hash_counter import run_hash_counter
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
    run_hash_counter(['task1', 'task2', 'task3'])
    equal_lines_number = 30

    with open('./result/hash.txt', 'r') as hash_file:
        lines = sum(1 for _ in hash_file)

        assert lines == equal_lines_number

    shutil.rmtree('./result/task1')
    shutil.rmtree('./result/task2')
    shutil.rmtree('./result/task3')

    os.remove('./result/hash.txt')
