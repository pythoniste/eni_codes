from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from sqlalchemy.exc import SQLAlchemyError

import transaction

from ..models import (
    MyModel,
    Subject,
    Contact,
    )


@view_config(route_name='home', request_method='GET', renderer='project:templates/mytemplate.jinja2')
def contact_get(request):
    """Display the contact form"""
    # Original code
    import pdb; pdb.set_trace()
    try:
        query = request.dbsession.query(MyModel)
        one = query.filter(MyModel.name == 'one').one()
    except SQLAlchemyError:
        return Response(db_err_msg, content_type='text/plain', status=500)

    subjects = request.dbsession.query(Subject).all()
    infos = request.session.pop_flash('infos')
    return {'one': one, 'subjects': subjects, 'project': 'contact', 'infos': infos}


@view_config(route_name='home', request_method='POST', renderer='project:templates/mytemplate.jinja2')
def contact_post(request):
    """Process contact datas"""
    import pdb; pdb.set_trace()

    email, subject_id, text = map(request.POST.get, ('email', 'subject_id', 'text'))

    with transaction.manager:
        request.dbsession.add(Contact(email=email, subject_id=subject_id, text=text))

    request.session.flash("Your submission has been registered", 'infos')

    return HTTPFound(location=request.route_url('home'))


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
