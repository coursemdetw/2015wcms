#@+leo-ver=5-thin
#@+node:2014spring.20140628104046.1751: * @file openshiftstaticfiles.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:2014spring.20140628104046.1752: ** openshiftstaticfiles declarations
#!/usr/bin/env python
import static

from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.core.handlers.base import get_path_info
from django.contrib.staticfiles.handlers import StaticFilesHandler as DebugHandler

try:
    from urllib.parse import urlparse
except ImportError:     # Python 2
    from urlparse import urlparse
from django.contrib.staticfiles import utils

#@+node:2014spring.20140628104046.1753: ** class Cling
class Cling(WSGIHandler):
    """WSGI middleware that intercepts calls to the static files
    directory, as defined by the STATIC_URL setting, and serves those files.
    """
    #@+others
    #@+node:2014spring.20140628104046.1754: *3* __init__
    def __init__(self, application, base_dir=None):
        self.application = application
        if not base_dir:
            base_dir = self.get_base_dir()
        self.base_url = urlparse(self.get_base_url())

        self.cling = static.Cling(base_dir)
        self.debug_cling = DebugHandler(base_dir)

        super(Cling, self).__init__()

    #@+node:2014spring.20140628104046.1755: *3* get_base_dir
    def get_base_dir(self):
        return settings.STATIC_ROOT

    #@+node:2014spring.20140628104046.1756: *3* get_base_url
    def get_base_url(self):
        utils.check_settings()
        return settings.STATIC_URL

    #@+node:2014spring.20140628104046.1757: *3* debug
    @property
    def debug(self):
        return settings.DEBUG

    #@+node:2014spring.20140628104046.1758: *3* _transpose_environ
    def _transpose_environ(self, environ):
        """Translates a given environ to static.Cling's expectations."""
        environ['PATH_INFO'] = environ['PATH_INFO'][len(self.base_url[2]) - 1:]
        return environ

    #@+node:2014spring.20140628104046.1759: *3* _should_handle
    def _should_handle(self, path):
        """Checks if the path should be handled. Ignores the path if:

        * the host is provided as part of the base_url
        * the request's path isn't under the media path (or equal)
        """
        return path.startswith(self.base_url[2]) and not self.base_url[1]

    #@+node:2014spring.20140628104046.1760: *3* __call__
    def __call__(self, environ, start_response):
        # Hand non-static requests to Django
        if not self._should_handle(get_path_info(environ)):
            return self.application(environ, start_response)

        # Serve static requests from static.Cling
        if not self.debug:
            environ = self._transpose_environ(environ)
            return self.cling(environ, start_response)
        # Serve static requests in debug mode from StaticFilesHandler
        else:
            return self.debug_cling(environ, start_response)


    #@-others
#@+node:2014spring.20140628104046.1761: ** class MediaCling
class MediaCling(Cling):
    #@+others
    #@+node:2014spring.20140628104046.1762: *3* __init__

    def __init__(self, application, base_dir=None):
        super(MediaCling, self).__init__(application, base_dir=base_dir)
        # override callable attribute with method
        self.debug_cling = self._debug_cling

    #@+node:2014spring.20140628104046.1763: *3* _debug_cling
    def _debug_cling(self, environ, start_response):
        environ = self._transpose_environ(environ)
        return self.cling(environ, start_response)

    #@+node:2014spring.20140628104046.1764: *3* get_base_dir
    def get_base_dir(self):
        return settings.MEDIA_ROOT

    #@+node:2014spring.20140628104046.1765: *3* get_base_url
    def get_base_url(self):
        return settings.MEDIA_URL
    #@-others
#@-others
#@-leo
