import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

import CONFIG

if CONFIG.METHOD == 1:
    from Methods.M1.generator import Generator

data, connection, list_gFoo, list_db_field = CONFIG.check_config()
generator = Generator(data,
                      connection,
                      CONFIG.INTEREST,
                      list_gFoo,
                      list_db_field)
try:
    getattr(generator, CONFIG.MODE.lower())()
except:
    print()
    generator.save()

connection.close()
