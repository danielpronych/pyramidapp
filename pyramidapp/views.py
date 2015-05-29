from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

import cStringIO

import logging
log = logging.getLogger(__name__)

from .models import (
    DBSession,
    MyModel,
    )

@view_config(route_name='view_test_svg')
def test_svg_view(request):
    # Full module import is not allowed by Pyramid
    #from pylab import *
    # Do individual required imports instead
    from pylab import figure, axes, pie, title, savefig
    log.debug('In test_svg_view')
    figure(1, figsize=(6,6))
    ax = axes([0.1, 0.1, 0.8, 0.8])
    labels = ['Frogs', 'Hogs', 'Dogs', 'Logs']
    fracs = [15, 30, 45, 10]
    explode=(0, 0.05, 0, 0)
    pie(fracs, explode=explode, labels=labels,
                                autopct='%1.1f%%', shadow=True, startangle=90)
    title('Raining Hogs and Dogs', bbox={'facecolor':'0.8', 'pad':5})
    imgdata = cStringIO.StringIO()
    savefig(imgdata, format='svg')
    imgdata.seek(0)
    svg_dta = imgdata.getvalue()
    # Close the StringIO buffer
    imgdata.close()
    return Response(svg_dta, content_type='image/svg+xml')

@view_config(route_name='view_test2_svg')
def test2_svg_view(request):
    # Full module import is not allowed by Pyramid
    #from pylab import *
    # Do individual required imports instead
    from pylab import figure, axes, pie, title, savefig
    log.debug('In test2_svg_view')
    figure(1, figsize=(6,6))
    ax = axes([0.1, 0.1, 0.8, 0.8])
    labels = ['Bats', 'Cats', 'Lats', 'Mats']
    fracs = [15, 30, 45, 70]
    explode=(0, 0.05, 0, 0)
    pie(fracs, explode=explode, labels=labels,
                                autopct='%1.1f%%', shadow=True, startangle=90)
    title('Raining Bats and Cats', bbox={'facecolor':'0.8', 'pad':5})
    imgdata = cStringIO.StringIO()
    savefig(imgdata, format='svg')
    imgdata.seek(0)
    svg_dta = imgdata.getvalue()
    # Close the StringIO buffer
    imgdata.close()
    return Response(svg_dta, content_type='image/svg+xml')

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    try:
        one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'one': one, 'project': 'pyramidapp'}


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pyramidapp_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

