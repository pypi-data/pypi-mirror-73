"""
This module is used for abstracted uses of the multiprocess library.
"""



import multiprocessing as mp
from typing import Callable, Optional


def multiprocess_me(size: int,
                    func: Callable,
                    data: list,
                    output: bool = True) -> Optional[list]:
    """
    multiprocess_me is used to multiprocess across a list of dicts.

    :param size:  The amount of parallelism.
    :param func: the function to use on each dict
    :param data: a list of dicts.
    :param output: Should multiprocess_me return a list of Dict?
    :return: if output is true the return will be a list of the output from the function
    """
    if not isinstance(data, list):
        raise NotDict("Data must be a a dict")
    pool = mp.Pool(size)
    updated_data: list = pool.map(func, data)
    pool.close()
    pool.join()
    if output:
        return updated_data
    return None


class NotDict(Exception):
    pass

