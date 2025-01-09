import os
import hashlib

def hash_file(filename):
    h = hashlib.md5()
    with open(filename, 'rb') as file:
        while chunk := file.read(4096):
            h.update(chunk)
    return h.hexdigest()

def find_duplicates(folder):
    hashes = {}
    duplicados = []
    for dirpath, _, filenames in os.walk(folder):
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            file_hash = hash_file(full_path)
            if file_hash in hashes:
                duplicados.append((full_path, hashes[file_hash]))
            else:
                hashes[file_hash] = full_path
    return duplicados

def delete_file(file):
    try:
        os.remove(file)
        return True
    except Exception as e:
        return False