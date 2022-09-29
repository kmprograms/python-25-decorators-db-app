import sqlite3
from typing import Callable, Any


def update(db_name: str):
    def decorator(fun: Callable[..., str]):
        def wrapper(*args, **kwargs):
            with sqlite3.connect(db_name) as connection:
                sql = fun(*args, **kwargs)
                print(sql)
                connection.execute(sql)
        return wrapper
    return decorator

def query(db_name: str):
    def decorator(fun: Callable[..., str]):
        def wrapper(*args, **kwargs):
            with sqlite3.connect(db_name) as connection:
                sql = fun(*args, **kwargs)
                print(sql)
                cursor = connection.cursor()
                cursor.execute(sql)
                return cursor.fetchall()
        return wrapper
    return decorator


@update('test.db')
def create_table(table: str, *args) -> str:
    return f'''
        create table if not exists {table} (
            id integer primary key autoincrement,
            {", ".join(args)}
        );
    '''

@update('test.db')
def insert(table: str, data: dict[str, Any]) -> str:
    columns = ', '.join(data.keys())
    values = ', '.join([f"'{v}'" if isinstance(v, str) else str(v) for v in data.values()])
    return f'insert into {table} ({columns}) values ({values})'

@query('test.db')
def get_all(table: str) -> str:
    return f'select * from {table}'

@query('test.db')
def get_one(table: str, id: int) -> str:
    return f'select * from {table} where id = {id}'

def main() -> None:
    try:
        create_table('people', 'name varchar(50) not null', 'age integer default 18')
        # insert('people', {'name': 'A', 'age': 20})
        print(get_all('people'))
        print(get_one('people', 1))
    except Exception as e:
        print(e.args[0])

if __name__ == '__main__':
    main()