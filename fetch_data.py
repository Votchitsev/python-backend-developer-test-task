"""Getting files."""
import base64
import os

from aiohttp import ClientSession


async def get_file_data(session: object, file_to_retrieve: dict) -> dict:
    """Retrieve file.

    Args:
        session: instance of class aiohttp.ClientSession
        file_to_retrieve: dict

    Returns:
        dict
    """
    async with session.get(
        'https://gitea.radium.group/' +
        'api/v1/repos/radium/project-configuration/' +
        'git/blobs/{sha}'.format(sha=file_to_retrieve['sha']),
            headers={'accept': 'application/json'},
    ) as http_response:

        return await http_response.json()


def write_file(
    directory: str,
    file_content: dict,
    file_meta_data: dict,
    path: str,
) -> None:
    """Create a file and write data to it.

    Args:
        directory: (str) main directory name
        file_content: (dict) includes base64 content
        file_meta_data: (dict) includes file name
        path: (str) path to directory for put file
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
        directory: (str) main directory name
    """
    if (directory):
        try:
            os.mkdir('result/{dir}'.format(dir=directory))
        except FileExistsError:
            return


async def response_handler(
    file_system_elements: list,
    directory: str,
    path: str,
    session: object,
    callback: object,
) -> None:
    """Iterate on file_system_elements to get element types.

    If element is file - call write_file function.
    If element is directory - call add_dir and
    callback functions.

    Args:
        file_system_elements: list
        directory: (str) main directory name
        path: (str) path to directory for put file
        session: instance of aiohttp.client.ClientSession
        callback: function fetchData
    """
    for element in file_system_elements:
        if element['type'] == 'file':

            fl = await get_file_data(session, element)

            write_file(directory, fl, element, path)

        if element['type'] == 'dir':

            add_dir(
                '/{dir}/{path}'.format(
                    dir=directory,
                    path=element['path'],
                ),
            )

            await callback(element['url'], directory, element['path'])


async def run_fetch_data(
    url: str,
    directory: str = '',
    path: str = '',
) -> None:
    """Run task handler.

    Args:
        url: (str) url for to make get repository request
        directory: (str) main directory name
        path: (str) path to directory for put file
    """
    add_dir(directory)

    async with ClientSession() as session:
        headers = {'accept': 'application/json'}

        async with session.get(url, headers=headers) as response:

            response = await response.json()

            await response_handler(
                response, directory, path, session, run_fetch_data,
            )
