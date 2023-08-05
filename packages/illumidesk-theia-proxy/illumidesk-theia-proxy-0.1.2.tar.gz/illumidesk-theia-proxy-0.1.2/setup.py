import setuptools
from os import path

# read the contents of your README file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="illumidesk-theia-proxy",
    version='0.1.2',
    url="https://github.com/illumidesk/illumidesk-theia-proxy",
    author="IllumiDesk Team",
    description="hello@illumidesk.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
	keywords=['jupyter', 'theia', 'jupyterhub'],
	classifiers=['Framework :: Jupyter'],
    install_requires=[
        'jupyter-server-proxy'
    ],
    entry_points={
        'jupyter_serverproxy_servers': [
            'theia = illumidesk_theia_proxy:setup_theia',
        ]
    },
    package_data={
        'illumidesk-theia-proxy': ['icons/*'],
    },
)
