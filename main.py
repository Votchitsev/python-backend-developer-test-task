from pprint import pprint
import os
import requests
import base64


def fetchData(url, path=''):
    
    response = requests.get(
        url,
        headers = {
        'accept': 'application/json',
        } 
        )

    response = response.json()

    for file in response:
        if file['type'] == 'file':
            blob = requests.get(
                f"https://gitea.radium.group/api/v1/repos/radium/project-configuration/git/blobs/{file['sha']}",
                headers = {
                    'accept': 'application/json',
                }
            )

            blob = blob.json()

            d = blob['content'].encode('utf-8')
            d = base64.decodebytes(d)

            f = open(str('./result/' + f"{path}/" + file['name']), 'wb')
            f.write(d)
            f.close()

        if file['type'] == 'dir':
            os.mkdir(f"./result/{file['path']}")
            fetchData(file['url'], file['path'])



fetchData('https://gitea.radium.group/api/v1/repos/radium/project-configuration/contents/%2F?ref=HEAD')