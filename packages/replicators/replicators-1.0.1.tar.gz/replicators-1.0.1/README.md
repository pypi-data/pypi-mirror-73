![Python](https://github.com/bclipp/replicators/workflows/Python/badge.svg)

# replicator


### description
This is a personal package used to hold code patterns used for multithreading and multiprocessing.

### usage
```pip install replicator```

```import replicant.multiprocess as mult

data_frame: pd.DataFrame = pd.DataFrame(
        columns=["This",
                 "is",
                 "a",
                 "test",
                 "to",
                 "check",
                 "a_function"],
        data=[[5, 2, "b", 3, 4, 5, 3],
              [7, 2, "b", 3, 4, 5, 3],
              [8, 2, "b", 3, 4, 5, 3],
              [3, 2, "b", 3, 4, 5, 3],
              [2, 2, "b", 3, 4, 5, 3],
              [8, 2, "b", 3, 4, 5, 3],
              [2, 2, "b", 3, 4, 5, 3],
              [8, 2, "b", 3, 4, 5, 3],
              [19, 2, "b", 3, 4, 5, 3],
              [53, 2, "b", 3, 4, 5, 3],
              [11, 2, "b", 3, 4, 5, 3],
              [16, 2, "b", 3, 4, 5, 3]])
    data: list = list(data_frame.T.to_dict().values())
    mult.multiprocess_me(1, print, data, False)

```
