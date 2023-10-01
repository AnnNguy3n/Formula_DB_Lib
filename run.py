import CONFIG
if CONFIG.METHOD == 1:
    from Methods.method_1 import Generator


data, connection, list_get_data_func, list_db_field = CONFIG.check_config()
generator = Generator(data, connection, CONFIG.INTEREST, list_get_data_func, list_db_field)
try:
    getattr(generator, CONFIG.MODE.lower())()
except:
    generator.save()

connection.close()