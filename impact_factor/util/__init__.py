import os


def safe_open(filename, mode='r'):
    
    if 'w' in mode:
        dirname = os.path.dirname(filename)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)

    if filename.endswith('.gz'):
        import gzip
        return gzip.open(filename, mode=mode)

    return open(filename, mode=mode)
