import numba as nb
import numpy as np
from util_funcs import *


@nb.njit
def get_inv_max_infor(WEIGHT, INDEX, PROFIT, SYMBOL, interest):
    '''
    Output: CtyMax, ProMax, GeoMax, HarMax
    '''
    size = INDEX.shape[0] - 1
    arr_profit = np.zeros(size)
    for i in range(size-1, -1, -1):
        idx = size-1-i
        start, end = INDEX[i], INDEX[i+1]
        temp = WEIGHT[start:end]
        max_ = np.max(temp)
        max_idxs = np.where(temp==max_)[0] + start
        if max_idxs.shape[0] == 1:
            arr_profit[idx] = PROFIT[max_idxs[0]]
            if i == 0: CtyMax = max_idxs[0]
            if PROFIT[max_idxs[0]] <= 0.0:
                if i != 0: CtyMax = -1
                break
        else:
            arr_profit[idx] = interest
            if i == 0: CtyMax = -1

    GeoMax = geomean(arr_profit[:-1])
    HarMax = harmean(arr_profit[:-1])
    ProMax = arr_profit[-1]
    return CtyMax, ProMax, GeoMax, HarMax


@nb.njit
def get_inv_ngn_infor(WEIGHT, INDEX, PROFIT, SYMBOL, interest):
    '''
    Output: Nguong, ProNgn, GeoNgn, HarNgn
    '''
    size = INDEX.shape[0] - 1
    arr_profit = np.zeros(size)
    temp_profit = np.zeros(size)
    max_profit = -1.0

    list_loop = np.zeros((size-1)*10)
    for k in range(size-1, 0, -1):
        start, end = INDEX[k], INDEX[k+1]
        temp_weight = WEIGHT[start:end].copy()
        temp_weight[::-1].sort()
        list_loop[10*(k-1):10*k] = temp_weight[:10]

    list_loop = np.unique(list_loop)
    for v in list_loop:
        C = WEIGHT > v
        temp_profit[:] = 0.0
        for i in range(size-1, -1, -1):
            idx = size-i-1
            start, end = INDEX[i], INDEX[i+1]
            if np.count_nonzero(C[start:end]) == 0:
                temp_profit[idx] = 1.06
            else:
                temp_profit[idx] = PROFIT[start:end][C[start:end]].mean()
        
        new_profit = geomean(temp_profit[:-1])
        if new_profit > max_profit:
            Nguong = v
            max_profit = new_profit
            arr_profit[:] = temp_profit[:]
    
    GeoNgn = max_profit
    HarNgn = harmean(arr_profit[:-1])
    ProNgn = arr_profit[-1]
    return Nguong, ProNgn, GeoNgn, HarNgn


@nb.njit
def get_tf_score(WEIGHT, INDEX, PROFIT, SYMBOL, interest):
    '''
    Output: TrFScr
    '''
    countTrue = 0
    countFalse = 0
    for i in range(1, INDEX.shape[0] - 1):
        start, end = INDEX[i], INDEX[i+1]
        t, f = countTrueFalse(WEIGHT[start:end], PROFIT[start:end])
        countTrue += t
        countFalse += f

    return countTrue / (countFalse + 1e-6)


@nb.njit
def get_ac_score(WEIGHT, INDEX, PROFIT, SYMBOL, interest):
    '''
    Output: AccScr
    '''
    size = INDEX.shape[0]-1
    arr_coef = np.zeros(size-1)

    for i in range(size-1, 0, -1):
        idx = size-1-i
        start, end = INDEX[i], INDEX[i+1]
        weight_ = WEIGHT[start:end]
        profit_ = PROFIT[start:end]
        mask = weight_ != -1.7976931348623157e+308
        weight = weight_[mask]
        profit = profit_[mask]
        weight = weight[np.argsort(profit)[::-1]]
        arr_coef[idx] = calculate_ac_coef(weight)
        if arr_coef[idx] == 0.0: break

    return geomean(arr_coef)
