"""Getting files."""
import base64
import os

from aiohttp import ClientSession


async def get_file(session, file_to_retrieve):
    """Retrieve file.

    Args:
        session: class aiohttp.ClientSession
        file_to_retrieve: dict
    Returns:
        dict
    """
    async with session.get(
        'https://gitea.radium.group/'
        + 'api/v1/repos/radium/project-configuration/'
        + 'git/blobs/{sha}'.format(sha=file_to_retrieve["sha"]),
            headers={'accept': 'application/json'},
            ) as blob:

        return await blob.json()


def write_file(directory, file_content, file_meta_data, path):
    """Create a file and write data to it

        Args:
            directory: str
            file_content: dict
            file_meta_data: dict
            path: str
        Returns:
            None
    """
    utf8content = file_content['content'].encode('utf-8')
    bytes = base64.decodebytes(utf8content)

    with open(
        './result/{directory}/{path}/{name}'.format(
            directory=directory,
            path=path,
            name=file_meta_data["name"],
            ), 'wb',
        ) as file:

        file.write(bytes)


def add_dir(directory):
    """Creates a directory if it doesn't exists.

        Args
            directory(String): None
    """
    if (directory):
        try:
            os.mkdir('result/{dir}'.format(dir=directory))
        except FileExistsError:
            return


async def file_iteration(files, callback, session, path, directory):
    """Identifies files and directories from the request response.

    Args:
        files: list
        callback: function fetchData
        session: aiohttp.client.ClientSession
        path: string
        directory: string
    Returns:
        None
    """
    for file_data in files:
        if file_data['type'] == 'file':

            fl = await get_file(session, file_data)

            write_file(directory, fl, file_data, path)

        if file_data['type'] == 'dir':
            try:
                add_dir(
                    '/{dir}/{path}'.format(
                        dir=directory,
                        path=file_data['path'],
                        ),
                    )
            except FileExistsError:
                print('Файл {path} существует.'.format(path=file_data['path']))

            await callback(file_data['url'], directory, file_data['path'])


async def fetch_data(url, dir='', path=''):
    """Get.

    Args:
        url: str
        dir: str
        path: str
    Returns:
        None
    """
    add_dir(dir)

    async with ClientSession() as session:
        headers = {'accept': 'application/json'}

        async with session.get(url, headers=headers) as response:

            response = await response.json()

            await file_iteration(response, fetch_data, session, path, dir)
