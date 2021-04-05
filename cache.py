import pickle
from pathlib import Path
from functools import lru_cache


@lru_cache(maxsize=9999)
def _read(path):
    with open(path, 'rb') as fl:
        data = pickle.loads(fl.read())
    return data


def disk_cache(path):
    def w(f):
        def _f(x):
            文件名 = f'{x}_{f.__name__}.disk_cache'
            p = Path(path) / 文件名
            if p.is_file():
                return _read(str(p))
            else:
                a = f(x)
                with open(p, 'wb') as fl:
                    fl.write(pickle.dumps(a))
                return a
        return _f
    return w
