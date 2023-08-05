__MYSQL_URL_KEY = "MYSQL_URL"


class MySQLConfig:
    default_host = "localhost"
    default_port = 3306

    def __init__(self, url=None, host=None, port=None, database=None, param=None, user=None, password=None):
        import re
        if url:
            result = re.search(
                "^(mysql://){0,1}([^:/]+)(:(\d+)){0,1}(/([^?]+)){0,1}(\?(.*)){0,1}", url)
            groups = result.groups()
            if not host:
                host = groups[1] if groups[1] else self.default_host
            if not port:
                port = int(groups[3]) if groups[3] else self.default_port
            if not database:
                database = groups[5] if groups[5] else None
            if not param:
                param = dict([it.split('=')
                              for it in groups[7].split('&')]) if groups[7] else {}
            if not user:
                user = param.get("user")
            if not password:
                user = param.get("password")

        self.url = url
        self.host = host
        self.port = port
        self.database = database
        self.param = param if param else {}
        self.user = user
        self.password = password

    def __eq__(self, value):
        return self.host == value.host and self.port == value.port and self.database == value.database and self.param == value.param and self.user == value.user and self.password == value.password


def mysql_connect(url=None, autocommit=True):
    if not url:
        from .zconfig import get_param
        url = get_param(__MYSQL_URL_KEY)
    assert url

    import pymysql
    conf = MySQLConfig(url)

    client = pymysql.Connect(
        host=conf.host, port=conf.port, database=conf.database, user=conf.user, password=conf.password)
    client.autocommit(autocommit)
    return client


def mysql_query_one_value(client, sql):
    cursor = client.cursor()
    cursor.execute(sql)
    return cursor.fetchall()[0][0]


def mysql_query(client, sql):
    cursor = client.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def mysql_execute(client, sql):
    cursor = client.cursor()
    return cursor.execute(sql)


def mysql_insert(client, sql):
    cursor = client.cursor()
    res = cursor.execute(sql)
    return cursor.lastrowid if res else 0


class ZMySQL:
    def __init__(self, url=None):
        self.client = mysql_connect(url=url)

    def execute(self, sql):
        return mysql_execute(self.client, sql)

    def insert(self, sql):
        return mysql_insert(self.client, sql)

    def query(self, sql):
        return mysql_query(self.client, sql)

    def query_one_value(self, sql):
        return mysql_query_one_value(self.client, sql)
