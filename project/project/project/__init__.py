from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    my_session_factory = SignedCookieSessionFactory(
        'itsaseekreet')
    config = Configurator(settings=settings)
    with Configurator(settings=settings, session_factory=my_session_factory) as config:
        config.include('pyramid_jinja2')
        # config.include('pyramid_chameleon')
        config.include('.routes')
        config.include('.models')
        # config.scan('.views')
        config.scan()
    return config.make_wsgi_app()
