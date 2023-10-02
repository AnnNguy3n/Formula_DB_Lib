def get_list_table():
    return "SELECT name FROM sqlite_master WHERE type='table';"


def create_table(num_operand, list_field):
    temp = "\n    "
    return f'''CREATE TABLE "F{num_operand}" (
    "id" INTEGER,
    {temp.join([f'"E{i}" INTEGER NOT NULL,' for i in range(num_operand)])}
    {temp.join([f'"{field[0]}" {field[1]},' for field in list_field])}
    PRIMARY KEY ("id" AUTOINCREMENT)
)'''


def get_last_row_of_table(table_name):
    return f'SELECT * FROM "{table_name}" ORDER BY "id" DESC LIMIT 1;'


def create_table_update(num_operand, list_field):
    temp = "\n    "
    return f'''CREATE TABLE "T{num_operand}" (
    "id" INTEGER,
    {temp.join([f'"{field[0]}" {field[1]},' for field in list_field])}
    PRIMARY KEY ("id" AUTOINCREMENT)
)'''


def insert_rows(table_name, list_list_value, list_field):
    if len(list_field) == 0:
        text_1 = ""
    else:
        list_field_name = [f_[0] for f_ in list_field]
        if table_name.startswith("F"):
            num_op = int(table_name[1:])
            list_field_name = [f"E{ii}" for ii in range(num_op)] + list_field_name
        text_1 = f'''({", ".join([f'"{field}"' for field in list_field_name])})'''

    text_2 = ""
    for list_value in list_list_value:
        text = ""
        for value in list_value:
            if type(value) == str:
                text += f'"{value}",'
            else:
                text += f"{value},"

        text_2 += f"({text[:-1]}),\n"

    return f'''INSERT INTO "{table_name}"{text_1} VALUES {text_2[:-2]};'''


def count_rows_of_table(table_name):
    return f'SELECT COUNT(*) FROM "{table_name}"'


def select_row_by_id(table_name, id):
    return f'SELECT * FROM "{table_name}" WHERE "id" = {id}'
