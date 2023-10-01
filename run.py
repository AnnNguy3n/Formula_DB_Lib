import CONFIG
# if CONFIG.METHOD == 1:
#     from Methods.method_1 import Generator

data, connection, list_get_data_func, list_db_field = CONFIG.check_config()
print(list_get_data_func, list_db_field)