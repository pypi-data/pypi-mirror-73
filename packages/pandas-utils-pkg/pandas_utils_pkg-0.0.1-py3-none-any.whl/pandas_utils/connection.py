import mysql.connector as mariadb


def get_connection(env):
    """
    Create the database connection

    Parameters
    ----------
    env: dict
        The mysql database credentials

    Returns
    -------
    connection: sql connection
        The connection to the database
    """
    connection = mariadb.connect(
        user=env.get('user'),
        password=env.get('password'),
        database=env.get('database'),
        host=env.get('host')
    )
    return connection
