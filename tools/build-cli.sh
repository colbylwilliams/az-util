#!/bin/bash
set -e

cdir=$(cd -P -- "$(dirname -- "$0")" && pwd -P)
tcdir=${cdir%/*}

echo "Azure CLI Build Utility"
echo ""

pushd $tcdir > /dev/null

    echo "Creating a virtual environment"
    python -m venv env
    echo ""

    echo "Activating virtual environment"
    source env/bin/activate
    echo ""

    echo "Installing Azure CLI Dev Tools (azdev)"
    pip install azdev
    echo ""

    echo "Setting up Azure CLI Dev Tools (azdev)"
    azdev setup -r $PWD -e util
    echo ""

    echo "Running Linter on util extension source"
    azdev linter util
    echo ""

    echo "Running Style Checks on util extension source"
    azdev style util
    echo ""

    echo "Building util extension"
    azdev extension build util --dist-dir ./release_assets
    echo ""

    echo "Deactivating virtual environment"
    deactivate
    echo ""

popd > /dev/null

echo "Done."
echo ""
