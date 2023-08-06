from .connection import get_connection
from .utils import connected_request, df_request


def sql_request(query, env, connection=None):
    """
    Effectuate a request using the connection provided
    Effectuate a request using a new connection if no connection provided

    Parameters
    ----------
    query: str
        string containing a sql query
    env: dict
        credentials
    connection: sql connection
        connection to use (if provided)

    Returns
    ----------
    df: DataFrame
        DataFrame containing the result of the query
    """
    if connection is None:
        return df_request(query, env)
    return connected_request(query, connection)


def multiple_requests(queries, env):
    """
    Create a connection, effectuate several requests, and close it

    Parameters
    ----------
    queries: list of str
        list of string containing a sql query

    Returns
    ----------
    dfs: list of DataFrame
        list of DataFrame containing the result of the query
    """
    connection = get_connection(env)

    dfs = [connected_request(query, connection) for query in queries]
    connection.close()

    return dfs
