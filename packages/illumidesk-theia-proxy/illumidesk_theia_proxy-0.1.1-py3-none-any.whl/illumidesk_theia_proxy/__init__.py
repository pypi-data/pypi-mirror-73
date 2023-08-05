"""
Return config on servers to start for illumidesk-theia-proxy

See https://jupyter-server-proxy.readthedocs.io/en/latest/server-process.html
for more information.
"""
import os
import shutil


def setup_theia():
    # Make sure theia is in $PATH
    def _theia_command(port):
        executable = 'theia'
        full_path = shutil.which(executable)

        # Start theia in NODE_LIB_PATH env variable if set
        # If not, start in 'current directory', which is $REPO_DIR in mybinder
        # but /home/jovyan (or equivalent) in JupyterHubs
        working_dir = os.getenv('NODE_LIB_PATH', '.')

        if not full_path:
            raise FileNotFoundError('Can not find theia executable in $PATH')
        return ['theia', 'start', working_dir, '--hostname=0.0.0.0', '--port=' + str(port)]
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
