#!/bin/bash
__heredoc__="""

This script is used to build manylinux wheels, which can then be installed or
uploaded to pypi.


MB_PYTHON_TAG=cp38-cp38 ./run_manylinux_build.sh
PLAT=i686 MB_PYTHON_TAG=cp38-cp38 ./run_manylinux_build.sh

MB_PYTHON_TAG=cp37-cp37m ./run_manylinux_build.sh
MB_PYTHON_TAG=cp36-cp36m ./run_manylinux_build.sh
MB_PYTHON_TAG=cp35-cp35m ./run_manylinux_build.sh
MB_PYTHON_TAG=cp27-cp27m ./run_manylinux_build.sh

# MB_PYTHON_TAG=cp27-cp27mu ./run_nmultibuild.sh

docker pull quay.io/erotemic/manylinux-opencv:manylinux1_i686-opencv4.1.0-py3.6

"""

PLAT=${PLAT:=x86_64}
DOCKER_IMAGE=${DOCKER_IMAGE:="quay.io/erotemic/manylinux-for:$PLAT-opencv4.1.0-v4"}
# Valid multibuild python versions are:
# cp27-cp27m  cp27-cp27mu  cp34-cp34m  cp35-cp35m  cp36-cp36m  cp37-cp37m
MB_PYTHON_TAG=${MB_PYTHON_TAG:=$(python -c "import setup; print(setup.native_mb_python_tag())")}
NAME=${NAME:=$(python -c "import setup; print(setup.NAME.replace('-', '_'))")}
VERSION=${VERSION:=$(python -c "import setup; print(setup.VERSION)")}
echo "
MB_PYTHON_TAG = $MB_PYTHON_TAG
DOCKER_IMAGE = $DOCKER_IMAGE
VERSION = $VERSION
NAME = $NAME
"

if [ "$_INSIDE_DOCKER" != "YES" ]; then

    set -e
    docker run --rm \
        -v $PWD:/io \
        -e _INSIDE_DOCKER="YES" \
        -e MB_PYTHON_TAG="$MB_PYTHON_TAG" \
        -e NAME="$NAME" \
        -e VERSION="$VERSION" \
        $DOCKER_IMAGE bash -c 'cd /io && ./run_manylinux_build.sh'

    __interactive__='''
    docker run --rm \
        -v $PWD:/io \
        -e _INSIDE_DOCKER="YES" \
        -e MB_PYTHON_TAG="$MB_PYTHON_TAG" \
        -e NAME="$NAME"
        -e VERSION="$VERSION" \
        -it $DOCKER_IMAGE bash

    set +e
    set +x
    '''

    BDIST_WHEEL_PATH=$(ls wheelhouse/$NAME-$VERSION-$MB_PYTHON_TAG*.whl)
    echo "BDIST_WHEEL_PATH = $BDIST_WHEEL_PATH"
else
    set -x
    set -e

    VENV_DIR=$HOME/venv-$MB_PYTHON_TAG
    source $VENV_DIR/bin/activate
    pip install scikit-build cmake ninja

    cd /io
    python setup.py bdist_wheel

    chmod -R o+rw _skbuild
    chmod -R o+rw dist

    /opt/python/$MB_PYTHON_TAG/bin/python -m pip install auditwheel
    /opt/python/$MB_PYTHON_TAG/bin/python -m auditwheel show dist/$NAME-$VERSION-$MB_PYTHON_TAG*.whl
    /opt/python/$MB_PYTHON_TAG/bin/python -m auditwheel repair dist/$NAME-$VERSION-$MB_PYTHON_TAG*.whl
    chmod -R o+rw wheelhouse
    chmod -R o+rw $NAME.egg-info
fi
