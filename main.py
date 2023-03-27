import os
import base64
import asyncio
import time
from aiohttp import ClientSession

from pprint import pprint
import hashlib


async def fetchData(url, dir='', path=''):

    result = []

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

                        result.append({
                            'repo': dir,
                            'file': file['path'],
                            'hash': hashlib.sha256(blob['content'].encode()).hexdigest(),
                        })

                if file['type'] == 'dir':
                    try:
                        os.mkdir(f"./result/{repo_dir}/{file['path']}")
                        response = await fetchData(file['url'], repo_dir, file['path'])
                        
                        for i in response:
                            result.append(i)

                    except FileExistsError:
                        print(f"Файл {file['path']} существует.")

    return result


if __name__ == '__main__':

    async def main(tasks_):

        url = 'https://gitea.radium.group/api/v1/repos/radium/project-configuration/contents/%2F?ref=HEAD'

        hash = [] 

        start = time.time()

        print('Старт ->')

        for task in tasks_:
            hash.append(asyncio.create_task(fetchData(url, task)))
        
        result = await asyncio.gather(*hash)

        hash_list = []

        for i in result:
            hash_list.extend(i)
        
        pprint(hash_list)

        print('время выполнения скрипта: ', time.time() - start)
        
    
    tasks = ['task1', 'task2', 'task3']

    asyncio.run(main(tasks))
