import os
import os.path
import json
import signal
import psutil
import GPUtil
from traitlets import Float, Int, default
from traitlets.config import Configurable
from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from tornado import web


class MetricsHandler(IPythonHandler):
    @web.authenticated
    def get(self):
        """
        Calculate and return current resource usage metrics
        """
        pass
        # config = self.settings['nbresuse_display_config']
        
        # metrics = get_metrics(config)
        # self.write(json.dumps(metrics))

def _jupyter_server_extension_paths():
    """
    Set up the server extension for collecting metrics
    """
    return [{
        'module': 'nbdiscussion-board',
    }]

def _jupyter_nbextension_paths():
    """
    Set up the notebook extension for displaying metrics
    """
    return [
        {
            "section": "tree",
            "dest": "nbdiscussion_board",
            "src": "static",
            "require": "nbdiscussion_board/main"
        }
    ]

def load_jupyter_server_extension(nbapp):
    """
    Called during notebook start
    """
    pass
    # signal.signal(signal.SIGTERM, sigterm_handler)
    # resuseconfig = ResourceUseDisplay(parent=nbapp)
    # nbapp.web_app.settings['nbresuse_display_config'] = resuseconfig
    # route_pattern = url_path_join(nbapp.web_app.settings['base_url'], '/nbresuse/metrics')
    # nbapp.web_app.add_handlers('.*', [(route_pattern, MetricsHandler)])
