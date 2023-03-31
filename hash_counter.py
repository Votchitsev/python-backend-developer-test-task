"""Reads the hash amount for each file and writes it in hash.txt."""

import hashlib
import os


def run_hash_counter(dirs_list: list) -> None:
    """Launch the module.

    Args:
        dirs_list: list
    """
    for directory in dirs_list:
        sub_dirs_list = os.listdir(
            './result/{directory}/'.format(
                directory=directory,
            ),
        )

        sub_dir_handle(sub_dirs_list, directory)


def sub_dir_handle(dir_content: list, target_dir: str) -> None:
    """Check the contents of the directory for other directories and files.

    Args:
        dir_content: list of directories or files in main directory
        target_dir: name of main directory (str)
    """
    for content_item in dir_content:

        checking_dir = '{base_dir}/result/{direct}/{content}'.format(
            base_dir=os.getcwd(),
            direct=target_dir,
            content=content_item,
        )

        if os.path.isdir(checking_dir):
            sub_dir_handle(
                os.listdir(checking_dir),
                '{dir}/{content}'.format(content=content_item, dir=target_dir),
            )
        else:
            write_hash_sum(checking_dir)


def write_hash_sum(file_path: str) -> None:
    """Read the hash amount of the file and writes it in hash.txt.

    Args:
        file_path: path to file to read hash (str)
    """
    with open(
        '{base_dir}/result/hash.txt'.format(base_dir=os.getcwd()),
        'a+',
    ) as hash_data_file:

        with open(file_path, 'rb') as handled_file:
            bytes_data = handled_file.read()
            hash_data = hashlib.sha256(bytes_data).hexdigest()
            hash_data_file.write(
                '{path} {hash_string} \n'.format(
                    path=file_path, hash_string=hash_data,
                ),
            )
