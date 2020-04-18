from multiprocess import freeze_support
from multiprocessing import Pool


def f(x):
    return x**x


if __name__ == "__main__":
    freeze_support()

    pool = Pool(4)

    for x in pool.imap(f, [(1,2), 2, 3, 4]):
        print("...")
        print (x)