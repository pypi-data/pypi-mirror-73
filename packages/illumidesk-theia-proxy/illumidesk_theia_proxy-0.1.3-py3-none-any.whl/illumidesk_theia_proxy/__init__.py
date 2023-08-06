"""
Return config on servers to start for illumidesk-theia-proxy

See https://jupyter-server-proxy.readthedocs.io/en/latest/server-process.html
for more information.
"""
import os
import shutil
import logging


logger = logging.getLogger(__name__)
logger.setLevel('INFO')


def setup_theia():
    # Make sure theia is in $PATH
    def _theia_command(port):
        executable = shutil.which('theia')
        if not executable:
            raise FileNotFoundError('Can not find theia executable in $PATH')
        # Create theia working directory
        home_dir = os.environ.get('HOME') or '/home/jovyan'
        working_dir = f'{home_dir}/theia'
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)
            logger.info("Created directory %s" % working_dir)
        else:    
            logger.info("Directory %s already exists" % working_dir)
        return ['theia', 'start', '--hostname=0.0.0.0', '--port=' + str(port)]
    return {
        'command': _theia_command,
        'environment': {
            'USE_LOCAL_GIT': 'true'
        },
        'launcher_entry': {
            'title': 'Theia IDE',
            'icon_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'theia.svg')
        }
    }
