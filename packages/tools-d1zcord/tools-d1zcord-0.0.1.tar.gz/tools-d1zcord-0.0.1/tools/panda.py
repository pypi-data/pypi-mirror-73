#! python3
# -*- coding: utf-8 -*-

import os
from typing import List, Tuple, Union, Iterable, Callable, Optional
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from tools.general import walk

base_xl_suffixes: Tuple[str, ...] = ('.xls', '.xlsx', '.xlsm', '.xlsb')


def xl_files(folder: Union[str, bytes, os.PathLike, Path],
             xl_suffixes: Union[str, Tuple[str, ...]] = base_xl_suffixes) -> Iterable[Path]:
    """
    Walk excel files in folder and subfolders

    """
    for file in walk(folder):
        if file.name.endswith(xl_suffixes) and not file.name.startswith('~$'):
            yield file


def basic_reader(file: Union[str, bytes, os.PathLike, Path],
                 base_row: int = 9,
                 header: Optional[int] = None,
                 index_col: Union[int, List[int], None] = None,
                 **kwargs) -> pd.DataFrame:
    """
    Basic reader of Excel file

    """
    return pd.read_excel(file, skiprows=base_row, header=header, index_col=index_col, **kwargs)


def read_all_rep(folder: Union[str, bytes, os.PathLike, Path],
                 reader: Callable[..., pd.DataFrame] = basic_reader,
                 verbose: bool = True,
                 **kwargs) -> pd.DataFrame:
    """
    Read all excel files in folder and subfolders into single dataframe using reader

    """
    frames = (reader(file, **kwargs) for file in xl_files(folder))

    if verbose:
        total: int = sum(1 for _ in xl_files(folder))
        frames = tqdm(frames, total=total)

    if 'index_col' in kwargs and kwargs['index_col']:
        ignore_index: bool = False
    else:
        ignore_index: bool = True

    return pd.concat(frames, ignore_index=ignore_index)
