"""
this module is for reusable sql queries
"""


def select_table(table: str, limit: int = -1) -> str:
    """
    select_all_table is used for returning all the table data.
    :param table:  return stock table data
    :return:
    """
    if limit == -1:
        sql_query = f"SELECT * FROM {table};"
    else:
        sql_query = f"SELECT * FROM {table} limit {limit};"
    return sql_query


def drop_table(table: str) -> str:
    """
    drop_table table is a function used to return the query to drop a table
    :param table:
    :return:
    """
    return f"""DROP TABLE {table}; """
