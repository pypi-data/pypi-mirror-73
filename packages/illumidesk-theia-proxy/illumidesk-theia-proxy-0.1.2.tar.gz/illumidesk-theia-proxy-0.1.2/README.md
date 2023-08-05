# IllumiDesk Theia IDE

[Theia](https://www.theia-ide.org/) is a configurable web-based IDE
that supports [Visual Studio Code](https://code.visualstudio.com/) compatible extensions. This package was built using the [`jupyter-server-proxy` cookiecutter template](https://github.com/jupyterhub/jupyter-server-proxy/tree/master/contrib/template).

## Installation

## Requirements

#### Install THEIA IDE

This package's executes the standard `theia start --hostname=0.0.0.0 --port=3000` command. This command assumes the `theia` executable and `package.json` file required to start the application are globally available.

We recommend building a [docker image based on this example](https://github.com/theia-ide/theia-apps/tree/master/theia-deb-build-docker) to avoid configuration conflicts, particularly when mounting the user's home directory with a volume on a local host.

### Install Jupyter Notebook

This extension relies on the Jupyter Notebook to run. [Refer to Jupyter's official documentaion](https://jupyter.org/install) for installation instructions.

### Install illumidesk-theia-proxy

Install the package with pip:

```
pip install illumidesk-theia-proxy
```

### Running with jupyter/docker-stacks based image

The `THEIA IDE` requires `node v10x` for compilation. Therefore the version of node that runs `theia` should also equate to v10x. The jupyter/docker-stacks based images install more recent versions of node. To run `theia` with a container based on a `jupyter/docker-stacks` image install `NVM` and a version `10x` of `node`.

## Notes

- This package is tested with an image based on one of the [Jupyter docker-stacks](https://jupyter-docker-stacks.readthedocs.io/en/latest/) running with JupyterHub.
- `THEIA` requires Node 10x. The base `jupyter docker-stacks` images need some tweaking to make them work with `nvm` and the correct version of `node`. Refer to [this Dockerfile](https://github.com/IllumiDesk/illumidesk/src/illumidesk/workspaces/theia/templates/Dockerfile.theia.j2) for an example.

## Why?

IllumiDesk's setup requires `docker volume` mounts with the local host instance. Files copied to the `jovyan` home directory during the docker build stage are overriden by the files located on the host directories when running a container based on the image. Therefore `theia` is installed with a `debian package (*.deb)` with a docker multi-stage build.

## Attributions

- [`jupyter-theia-proxy`](https://github.com/jupyterhub/jupyter-server-proxy/tree/master/contrib/theia)
- [`theia docker apps`](https://github.com/theia-ide/theia-apps)
- [`jupyter-server-proxy`](https://github.com/jupyterhub/jupyter-server-proxy)

## License

BSD 3-Clause
