import os
import base64
import asyncio
import time
from aiohttp import ClientSession


async def fetchData(url, dir='', path=''):
    if (dir):
        try:
            os.mkdir('result/' + dir)
        except FileExistsError:
            pass

        repo_dir = dir
    
    async with ClientSession() as session:
        async with session.get(url, headers={'accept': 'application/json'}) as response:

            response = await response.json()

            for file in response:
                if file['type'] == 'file':
                    async with session.get(
                        f"https://gitea.radium.group/api/v1/repos/radium/project-configuration/git/blobs/{file['sha']}",
                        headers = {
                            'accept': 'application/json',
                        }
                    ) as blob:

                        blob = await blob.json()

                        d = blob['content'].encode('utf-8')
                        d = base64.decodebytes(d)

                        f = open(str(f"./result/{repo_dir}/" + f"{path}/" + file['name']), 'wb')
                        f.write(d)
                        f.close()

                if file['type'] == 'dir':
                    try:
                        os.mkdir(f"./result/{repo_dir}/{file['path']}")
                        await fetchData(file['url'], repo_dir, file['path'])

                    except FileExistsError:
                        print(f"Файл {file['path']} существует.")


if __name__ == '__main__':

    async def main():

        url = 'https://gitea.radium.group/api/v1/repos/radium/project-configuration/contents/%2F?ref=HEAD'

        task1 = asyncio.create_task(fetchData(url, 'task1'))
        task2 = asyncio.create_task(fetchData(url, 'task2'))
        task3 = asyncio.create_task(fetchData(url, 'task3'))

        start = time.time()

        print('Старт ->')

        await task1
        await task2
        await task3

        print('время выполнения скрипта: ', time.time() - start)

    asyncio.run(main())
