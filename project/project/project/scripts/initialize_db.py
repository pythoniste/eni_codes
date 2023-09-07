import argparse
import sys

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from ..models import MyModel, Subject, Contact
from ..models.meta import Base


def setup_models(dbsession):
    """
    Add or update models / fixtures in the database.

    """
    # Base.metadata.drop_all(dbsession.engine)
    # Base.metadata.create_all(dbsession.engine)
    model = MyModel(name='one', value=1)
    dbsession.add(model)

    for subject_name in ('Python', 'Pyramid', 'Pygame'):
        model = Subject(name=subject_name)
        dbsession.add(model)
    model = Contact(email='me@example.com', text='Why 42 is the answer ?')
    dbsession.add(model)


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')
