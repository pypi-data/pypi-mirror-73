import multiprocessing as mp
from typing import Callable, Optional


def multiprocess_me(size: Optional[int],
                    func: Callable,
                    data: list,
                    output: bool = True) -> Optional[list]:
    pool = mp.Pool(size)
    updated_data: list = pool.map(func, data)
    pool.close()
    if output:
        pool.join()
        return updated_data
