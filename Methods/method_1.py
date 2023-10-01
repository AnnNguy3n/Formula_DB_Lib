import pandas as pd
from base import Base
from sqlite3 import Connection
import json
import numpy as np
import numba as nb
import query_funcs as qf
import get_data_funcs
from Methods import gm1


def decode_formula(f, len_):
    len_f = len(f)
    rs = np.full(len_f*2, 0)
    check = False
    n = 1
    for i in range(len_f):
        rs[2*i] = f[i] // len_
        rs[2*i+1] = f[i] % len_
        if i != 0 and not check:
            if f[i] >= len_*2:
                n += 1
            else:
                check = True

    return rs, n


@nb.njit
def encode_formula(f, len_):
    len_f = len(f)
    rs = np.full(len_f//2, 0)
    for i in range(len(rs)):
        rs[i] = f[2*i]*len_ + f[2*i+1]

    return rs


class Generator(Base):
    def __init__(self,
                 data: pd.DataFrame,
                 connection: Connection,
                 interest: float,
                 list_get_data_func: list,
                 list_db_field: list) -> None:
        super().__init__(data)
        self.connection = connection
        self.interest = interest
        self.list_get_data_func = list_get_data_func
        self.list_db_field = list_db_field

        self.cursor = connection.cursor()
        self.number_data_operand = len(self.operand_name.keys())
        