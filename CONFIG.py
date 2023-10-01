#
DB_PATH = "/home/nguyen/Desktop/Formula_DB_Lib/Formula_DB"

#
DATA_PATH = "/home/nguyen/Desktop/Formula_DB_Lib/HOSE_File3_2023_Field.xlsx"

# Data label, vi du: "VN_Y" - data Viet Nam, chu ky nam
#                    "VN_Q" - data Viet Nam, chu ky quy
#                    "JP_Y" - data Nhat Ban, chu ky nam
LABEL = "VN_Y"

# Lai suat moi chu ky khi khong dau tu
INTEREST = 1.06

# Sinh CT cho chu ky nao, cat data tu chu ky nao
CYCLE = 2023
MIN_CYC = 2007

# Phuong phap sinh
# 1: Sinh cong thuc gom cac cum con dong bac
METHOD = 1

# Mode: "Generate" hoac "Update"
# '''
MODE = "generate"
N_UPDATE = None
# '''
'''
MODE = "update"
N_UPDATE = 3
'''


# ===========================================================================
import os
import pandas as pd
import json
import sqlite3
from base import Base
import get_data_funcs


def check_data_operands(op_name_1: dict, op_name_2: dict):
    if len(op_name_1) != len(op_name_2): return False

    op_1_keys = list(op_name_1.keys())
    op_2_keys = list(op_name_2.keys())
    for i in range(len(op_name_1)):
        if op_name_1[op_1_keys[i]] != op_name_2[op_2_keys[i]]:
            return False

    return True


def check_config():
    folder_data = f"{DB_PATH}/{LABEL}"
    os.makedirs(folder_data, exist_ok=True)

    data = pd.read_excel(DATA_PATH)
    data = data[data["TIME"] <= CYCLE]
    data = data[data["TIME"] >= MIN_CYC]
    base = Base(data)

    if not os.path.exists(folder_data + "/operand_names.json"):
        with open(folder_data + "/operand_names.json", "w") as fp:
            json.dump(base.operand_name, fp, indent=4)
        operand_name = base.operand_name
    else:
        with open(folder_data + "/operand_names.json", "r") as fp:
            operand_name = json.load(fp)

    if not check_data_operands(base.operand_name, operand_name):
        raise Exception("Sai data operands, kiem tra lai ten truong, thu tu cac truong trong data")

    folder_cycle_method = folder_data + f"/CYC_{CYCLE}/MET_{METHOD}"
    os.makedirs(folder_cycle_method, exist_ok=True)
    connection = sqlite3.connect(f"{folder_cycle_method}/formula.db")

    with open("database_fields.json", "r") as fp:
        db_fields = json.load(fp)

    if MODE == "generate":
        list_get_data_func = [getattr(get_data_funcs, key) for key in db_fields.keys()]
        list_db_field = []
        for key in db_fields.keys():
            list_db_field += db_fields[key]
    elif MODE == "update":
        list_key = list(db_fields.keys())
        list_get_data_func = [getattr(get_data_funcs, key) for key in list_key[-N_UPDATE:]]
        list_db_field = []
        for key in list_key[-N_UPDATE:]:
            list_db_field += db_fields[key]
    else:
        raise

    return data, connection, list_get_data_func, list_db_field
