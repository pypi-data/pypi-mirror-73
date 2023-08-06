import pandas as pd

from .connection import get_connection


# Read Utils
def df_request(query, env):
    """
    Create a connection to the database, execute the query and then close the
    connection

    Parameters
    ----------
    query: str
        string containing a sql query
    env: dict
        credentials

    Returns
    ----------
    df: DataFrame
        DataFrame containing the result of the query
    """
    connection = get_connection(env)

    df = pd.read_sql_query(query, connection)
    connection.close()

    return pd.DataFrame(df)


def connected_request(query, connection):
    """
    Effectuate a request with an already created connection
    """
    return pd.DataFrame(pd.read_sql_query(query, connection))


# Write Utils
def parse_ids_string_to_list(value):
    """
    Transform comma separated values string into list
    """
    if value:
        return list(map(int, value.split(",")))
    return value


def to_sql_string(value, quote=False, sql_kw=['NOW()', 'NULL']):
    """
    Transform value into string and
    eventually insert quotes around string values
    (except from sql keywords used as variables)
    """
    if quote and isinstance(value, str) and not value.startswith('"') and value not in sql_kw:
        return '"' + value + '"'
    return str(value)


def parse_tuple_to_sql(l, quote=False):
    """
    Convert a list to a sequence of values readable in an SQL 'IN'
    """
    if len(l):
        return ','.join([to_sql_string(ele, quote) for ele in l])
    return 'NULL'


def get_iidk_query(table, dimensions, duplicates):
    """
    Get a string containing an insert into duplicate key update query

    Parameters
    ----------
    table: str
        name of the table to write into
    dimensions: dict
        {columns names: values to write into columns}
    duplicates: list
        columns and values to duplicate key

    Returns
    ----------
    query: str
        sql query to execute to do an insert into duplicate key update
    """
    dku_col = [to_sql_string(col) for col in list(
        dimensions.keys()) if col in duplicates]
    dku_val = [to_sql_string(dimensions[col], True) for col in dku_col]

    duplicate_key_update = parse_tuple_to_sql(
        [ele[0] + '=' + ele[1] for ele in zip(dku_col, dku_val)])

    columns = parse_tuple_to_sql(list(dimensions.keys()))
    values = parse_tuple_to_sql(list(dimensions.values()), True)

    return f"""
        INSERT INTO {table} (
            {columns}
                )
        VALUES (
            {values}
        )
        ON DUPLICATE KEY UPDATE
            {duplicate_key_update}
    """
