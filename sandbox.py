from multiprocessing import freeze_support
from pathos.multiprocessing import Pool


def f(vars):
    return vars[0] ** vars[1]


if __name__ == "__main__":
    freeze_support()

    pool = Pool(4)

    result = pool.imap(f, [(1, 5), (2, 8), (3, 9)])
    print (list(result))

