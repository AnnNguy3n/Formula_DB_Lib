def get_list_table():
    return '''
SELECT name FROM sqlite_master WHERE type='table';
'''


def create_table(num_operand, list_field):
    temp = "\n    "
    return f'''
CREATE TABLE "F{num_operand}" (
    {temp.join([f'"E{i}" INTEGER NOT NULL,' for i in range(num_operand)])}
    {temp.join([f'"{field[0]}" {field[1]},' for field in list_field])}
    PRIMARY KEY ({", ".join([f'"E{i}"' for i in range(num_operand)])})
);
'''


def get_last_row_of_table(table_name):
    return f'''
SELECT * FROM "{table_name}" ORDER BY ROWID DESC LIMIT 1;
'''


def insert_row(table_name, list_field, list_list_value):
    if len(list_field) == 0:
        text_1 = ""
    else:
        text_1 = f'''({", ".join([f'"{field}"' for field in list_field])})'''

    text_2 = ""
    for list_value in list_list_value:
        text = ""
        for value in list_value:
            if type(value) == str:
                text += f'"{value}",'
            else:
                text += f"{value},"

        text_2 += f"({text[:-1]}),\n"

    return f'''
INSERT INTO "{table_name}"{text_1} VALUES {text_2[:-2]};
'''
