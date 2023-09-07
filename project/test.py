from sqlalchemy import MetaData, create_engine, text, event
from sqlalchemy.schema import Table
from sqlalchemy.orm import scoped_session, sessionmaker


def get_url(scheme, host, port, user, password, name):
    return f"{scheme}://{user}:{password}@{host}:{port}/{name}"

urls = [
    get_url(
        scheme = "postgresql",
        host = "project_postgres",
        port = 5432,
        user = "project",
        password = "secret",
        name = "test",
    ),
    get_url(
        scheme = "postgresql+psycopg2",
        host = "project_postgres",
        port = 5432,
        user = "project",
        password = "secret",
        name = "test",
    ),
    get_url(
        scheme = "mysql+mysqlconnector",
        host = "project_mysql",
        port = 3306,
        user = "project",
        password = "secret",
        name = "test",
    ),
    # get_url(
    #     scheme = "mysql+aiomysql",
    #     host = "project_mysql",
    #     port = 6603,
    #     user = "project",
    #     password = "secret",
    #     name = "test?charset=utf32_bin",
    # ),
]

for url in urls:
    try:
        print(f">>> {url}")
        metadata = MetaData()

        maker = sessionmaker(autoflush=True)
        session=scoped_session(maker)
        engine = create_engine(url)
        session.configure(bind=engine)

        # import pdb; pdb.set_trace()
        for t in metadata.sorted_tables:
            print(t.name)

        # table = Table("fiche", metadata, autoload_with=engine)
        table = Table("element", metadata, autoload_with=engine)
        print([c.name for c in table.columns])
    except Exception as e:
        print(f"{e!r}")



"""
metadata = MetaData(url)

maker = sessionmaker(autoflush=True)
session=scoped_session(maker)

# def init_search_path(connection, conn_record):
#     import pdb; pdb.set_trace()
#     cursor = connection.cursor()
#     try:
#         cursor.execute('SET search_path TO public;')
#     finally:
#         cursor.close()

engine = create_engine(url)
# event.listen(engine, 'connect', init_search_path)

session.configure(bind=engine)
# event.listen(engine, 'connect', init_search_path)


#  __c=engine.connect()
# (Pdb) __c
# <sqlalchemy.engine.base.Connection object at 0x7f0a04e2e750>
# (Pdb) _r = __c.execute(text("show search_path;"))
# (Pdb) _r.fetchall()
# [('public',)]

# import pdb; pdb.set_trace()
for t in metadata.sorted_tables:
    print(t.name)

table = Table("fiche", metadata, autoload_with=engine)
# table = Table("element", metadata, autoload_with=engine)
[c.name for c in table.columns]

"""