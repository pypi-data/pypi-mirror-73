import json
import os
import shutil


def relative_of(base_path: str, relative_path: str) -> str:
    """
    Given a base path and path relative to it, return full path of target.

    :param base_path: Base file path, normally __file__
    :param relative_path: path relative to base_path
    :return: full_path of target file
    """
    return os.path.normpath(os.path.join(os.path.dirname(base_path), relative_path))


def read_file_text(file_path: str, encoding: str = 'utf8') -> str:
    """
    Read content of text file.

    :param file_path: Path of file
    :param encoding: text encoding, default to utf8
    :return: File content
    """
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()


def ensure_parent_folder(file_path: str):
    """Make parent folder for file if not exists"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)


def write_file_bytes(file_path: str, content: bytes, force: bool = False) -> bool:
    """
    Write data to file, and ensure parent path exists.

    :param file_path: Path of file
    :param content: File content
    :param force: if true, overwrite target file if exists.
                  if false and target file exists then return false.
    :return: Whether write successful.
    """
    if os.path.exists(file_path):
        os.unlink(file_path)
    ensure_parent_folder(file_path)
    with open(file_path, 'wb') as f:
        f.write(content)


def read_file_json(file_path: str):
    """
    Read data from json file.

    :param file_path: File path
    :return: data read
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def write_file_json(file_path: str, data, indent=2):
    """
    Write data as json file.

    :param file_path: File path
    :param data: json data
    :param indent: no indent if None, or >0 for indent chars
    """
    ensure_parent_folder(file_path)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def purge_folder(dir_path: str):
    """

    Delete all files under specified folder, but keep folder itself.

    :param dir_path: folder to purge
    :return:
    """
    for file_name in os.listdir(dir_path):
        full_path = os.path.join(dir_path, file_name)
        if os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            os.unlink(full_path)
