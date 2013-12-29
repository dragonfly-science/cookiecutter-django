import os
import urlparse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.config.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')

from configurations.management import execute_from_command_line
from configurations import importer


def before_all(context):
    ### Take a TestRunner hostage.
    from django.test.simple import DjangoTestSuiteRunner
    # We'll use thise later to frog-march Django through the motions
    # of setting up and tearing down the test environment, including
    # test databases.
    importer.install(check_options=True)
    context.runner = DjangoTestSuiteRunner()

    ## If you use South for migrations, uncomment this to monkeypatch
    ## syncdb to get migrations to run.
    from south.management.commands import patch_for_test_db_setup
    patch_for_test_db_setup()

    from wsgi_intercept import requests_intercept
    import wsgi_intercept
    
    from django.core.handlers.wsgi import WSGIHandler
    from django.conf import settings
    
    host = context.host = '{{ cookiecutter.domain_name }}'
    port = context.port = getattr(settings, 'TESTING_INTERCEPT_PORT', 80)
    # NOTE: Nothing is actually listening on this port. wsgi_intercept
    # monkeypatches the networking internals to use a fake socket when
    # connecting to this port.
    requests_intercept.install()
    wsgi_intercept.add_wsgi_intercept(host, port, WSGIHandler)

    def browser_url(url):
        """Create a URL for the virtual WSGI server.

        e.g context.browser_url('/'), context.browser_url(reverse('my_view'))
        """
        return urlparse.urljoin('http://%s:%d/' % (host, port), url)

    context.browser_url = browser_url
    context.runner.setup_test_environment()
    context.old_db_config = context.runner.setup_databases()
    from django.core.management import call_command
    call_command('createsuperuser',
                 interactive=False,
                 username="risto",
                 email="risto@test.com")
    call_command('migrate')

def after_all(context):
    from wsgi_intercept import requests_intercept
    requests_intercept.uninstall()
    context.runner.teardown_databases(context.old_db_config)
    context.runner.teardown_test_environment()


def before_scenario(context, scenario):
    pass
    # Set up the scenario test environment
    # We must set up and tear down the entire database between
    # scenarios. We can't just use db transactions, as Django's
    # TestClient does, if we're doing full-stack tests with Mechanize,
    # because Django closes the db connection after finishing the HTTP
    # response.


def after_scenario(context, scenario):
    pass
    # Tear down the scenario test environment.
    # Bob's your uncle.

