import hashlib


def get_file_sha1(file_path: str) -> str:
    """
    Get sha1 checksum of file

    :param file_path: File path
    :return: sha1 checksum
    """
    sha1 = hashlib.sha1()
    block_size = 1024 * 1024
    with open(file_path, 'rb') as f:
        while block := f.read(block_size):
            sha1.update(block)
    return sha1.hexdigest()
