"""Getting files."""
import base64
import os

from aiohttp import ClientSession


async def get_file(session: object, file_to_retrieve: dict) -> dict:
    """Retrieve file.

    Args:
        session: class aiohttp.ClientSession
        file_to_retrieve: dict

    Returns:
        dict
    """
    async with session.get(
        'https://gitea.radium.group/' +
        'api/v1/repos/radium/project-configuration/' +
        'git/blobs/{sha}'.format(sha=file_to_retrieve['sha']),
            headers={'accept': 'application/json'},
    ) as blob:

        return await blob.json()


def write_file(
    directory: str,
    file_content: dict,
    file_meta_data: dict,
    path: str,
) -> None:
    """Create a file and write data to it.

    Args:
        directory: str
        file_content: dict
        file_meta_data: dict
        path: str
    """
    utf8content = file_content['content'].encode('utf-8')
    bytes_data = base64.decodebytes(utf8content)

    with open(
        './result/{directory}/{path}/{name}'.format(
            directory=directory,
            path=path,
            name=file_meta_data['name'],
        ),
            'wb',
    ) as writing_file:

        writing_file.write(bytes_data)


def add_dir(directory: str) -> None:
    """Create a directory if it doesn't exists.

    Args:
        directory(str): None
    """
    if (directory):
        try:
            os.mkdir('result/{dir}'.format(dir=directory))
        except FileExistsError:
            return


async def file_iteration(
    files: list,
    callback: object,
    session: object,
    path: str,
    directory: str,
) -> None:
    """Identify files and directories from the request response.

    Args:
        files: list
        callback: function fetchData
        session: aiohttp.client.ClientSession
        path: string
        directory: string
    """
    for file_data in files:
        if file_data['type'] == 'file':

            fl = await get_file(session, file_data)

            write_file(directory, fl, file_data, path)

        if file_data['type'] == 'dir':

            add_dir(
                '/{dir}/{path}'.format(
                    dir=directory,
                    path=file_data['path'],
                ),
            )

            await callback(file_data['url'], directory, file_data['path'])


async def fetch_data(url: str, directory: str = '', path: str = '') -> None:
    """Get.

    Args:
        url: str
        directory: str
        path: str
    """
    add_dir(directory)

    async with ClientSession() as session:
        headers = {'accept': 'application/json'}

        async with session.get(url, headers=headers) as response:

            response = await response.json()

            await file_iteration(
                response, fetch_data, session, path, directory,
            )
