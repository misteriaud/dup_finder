import os
import logging
import argparse
import hashlib

# BUF_SIZE is totally arbitrary, change for your app!
# BUF_SIZE = 4294967296  # lets read stuff in 64kb chunks!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
files_set = {}

def get_hash(path):
    md5 = hashlib.md5()

    with open(path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)

    logging.info(f'Hashing file {path}: {md5.hexdigest()}')
    return (md5.digest())

def add_to_set(path):
    hash = get_hash(path)
    if hash not in files_set:
        files_set[hash] = path
    else:
        logging.warning(f'the file {path} already exist at {files_set[hash]}')

def record_hash_of_files_in_dir(directory):
    """Returns the `directory` size in bytes."""
    try:
        for entry in os.scandir(directory):
            if entry.is_file():
                add_to_set(entry.path)
            elif entry.is_dir():
                try:
                    record_hash_of_files_in_dir(entry.path)
                except FileNotFoundError:
                    pass
    except NotADirectoryError:
        add_to_set(directory)
    except PermissionError:
        logging.error(f'Permission denied for {directory}')
        return

def main():
    parser = argparse.ArgumentParser(
        prog = 'Utilitaire d\'analyse de fichier dupliqué',
        description = 'Permet de deplacer tous les fichiers et dossiers présents du dossier source au dossier destination, en verifiant que les elements ne sois pas en cours de dépot.'
    )
    parser.add_argument('scan_path', help='emplacement du dossier source')
    args = parser.parse_args()

    logging.basicConfig(filename='log.txt', level=logging.WARNING, format='%(levelname)s - %(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())
    record_hash_of_files_in_dir(args.scan_path)


if __name__ == "__main__":
    main()

# to send email from synology nas: https://swisstechiethoughts.wordpress.com/2014/01/20/howto-send-mail-from-synology-nas-commandline-using-google-mail-relay/
