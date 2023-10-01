import numpy as np
import numba as nb


@nb.njit
def geomean(arr):
    log_sum = 0.0
    for num in arr:
        if num <= 0.0: return 0.0
        log_sum += np.log(num)

    return np.exp(log_sum/len(arr))


@nb.njit
def harmean(arr):
    deno = 0.0
    for num in arr:
        if num <= 0.0: return 0.0
        deno += 1.0/num

    return len(arr)/deno


@nb.njit
def countTrueFalse(a, b):
    countTrue = 0
    countFalse = 0
    len_ = len(a)
    for i in range(len_ - 1):
        for j in range(i+1, len_):
            if a[i] == a[j] and b[i] == b[j]:
                countTrue += 1
            else:
                if (a[i] - a[j]) * (b[i] - b[j]) > 0:
                    countTrue += 1
                else:
                    countFalse += 1

    return countTrue, countFalse


@nb.njit
def calculate_ac_coef(arr):
    sum_ = 0.0
    l = len(arr)
    for i in range(l - 1):
        a = arr[i]
        b = arr[i+1:]
        nume = a - b
        deno = np.abs(a) + np.abs(b)
        deno[deno == 0.0] = 1.0
        sum_ += np.sum(nume/deno)

    result = sum_ / (l*(l-1))
    return max(result, 0.0)
