from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

import transaction

from .models import (
    DBSession,
    Subject,
    Contact,
    )


@view_config(route_name='home', request_method='GET', renderer='templates/mytemplate.pt')
def contact_get(request):
    """Display the contact form"""
    subjects = DBSession.query(Subject).all()
    infos = request.session.pop_flash('infos')
    return {'subjects': subjects, 'project': 'contact', 'infos': infos}


@view_config(route_name='home', request_method='POST', renderer='templates/mytemplate.pt')
def contact_post(request):
    """Process contact datas"""

    email, subject_id, text = map(request.POST.get, ('email', 'subject_id', 'text'))

    with transaction.manager:
        DBSession.add(Contact(email=email, subject_id=subject_id, text=text))

    request.session.flash("Your submission has been registered", 'infos')

    return HTTPFound(location=request.route_url('home'))

conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_contact_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

