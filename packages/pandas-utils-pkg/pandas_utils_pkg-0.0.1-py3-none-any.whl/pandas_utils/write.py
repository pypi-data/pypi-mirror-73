from .connection import get_connection
from .utils import get_iidk_query


def insert_duplicate(df, table, dimensions, duplicates, env, date=[True, True],
                     c=None):
    """
    Effectuate an insert into duplicate key update query

    Parameters
    ----------
    df: DataFrame
        data to insert in table
    table: str
        name of the table to write into
    dimensions: list or dict
        if list : name of columns to write in tables and of columns to read
        in df
        if dict : keys are name of columns to write in tables,
            values are name of columns to read in df
    duplicates: list
        columns and values to duplicate key
    env: dict
        credentials
    date: list of bool
        whetther to add a date_creation and date_last_update respectively
    c: sql cursor
        sql cursor on which execute the query

    Returns
    ----------
    None
    """
    # Define date variables
    dc = [[], ['date_creation']][date[0]]
    dlu = [[], ['date_last_update']][date[1]]
    now = sum(date) * ['NOW()']

    # Create new connection and cursor if not provided
    created = False
    if c is None:
        created = True
        conn = get_connection(env)
        c = conn.cursor()

    # Write each row in table
    for _, row in df.fillna('NULL').iterrows():
        if isinstance(dimensions, dict):
            columns = list(dimensions.keys())
            values = [row.get(value, value)
                      for value in list(dimensions.values())]
        if isinstance(dimensions, list):
            columns = dimensions
            values = [row.get(value, value) for value in dimensions]

        columns_values = dict(zip(columns + dc + dlu, values + now))
        query = get_iidk_query(table, columns_values, duplicates + dlu)
        c.execute(query)

    if created:
        conn.commit()
        conn.close()
