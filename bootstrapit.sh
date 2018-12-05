#!/bin/bash
# Bootstrapit Project Configuration

AUTHOR_NAME="Manuel Barkhau"
AUTHOR_CONTACT="mbarkhau@gmail.com"

KEYWORDS="environ variables mypy config configuration"
DESCRIPTION="Type safe environment variables parsing."


LICENSE_ID="MIT"

PACKAGE_NAME="myenv"
MODULE_NAME="myenv"
GIT_REPO_NAMESPACE="mbarkhau"
GIT_REPO_DOMAIN="gitlab.com"

DEFAULT_PYTHON_VERSION="python=3.6"
SUPPORTED_PYTHON_VERSIONS="python=3.6 python=3.7"

PACKAGE_VERSION="201812.0003-beta"

# GIT_REPO_URL=https://${GIT_REPO_DOMAIN}/${GIT_REPO_NAMESPACE}/${PACKAGE_NAME}


IS_PUBLIC=1


## Download and run the actual update script

if [[ $KEYWORDS == "keywords used on pypi" ]]; then
    echo "Default bootstrapit config detected.";
    echo "Did you forget to update parameters in your 'bootstrapit.sh' ?"
    exit 1;
fi

PROJECT_DIR=$(dirname "$0");

if ! [[ -f "$PROJECT_DIR/scripts/bootstrapit_update.sh" ]]; then
    mkdir -p "$PROJECT_DIR/scripts/";
    RAW_FILES_URL="https://gitlab.com/mbarkhau/bootstrapit/raw/master";
    curl --silent "$RAW_FILES_URL/scripts/bootstrapit_update.sh" \
        > "$PROJECT_DIR/scripts/bootstrapit_update.sh.tmp";
    mv "$PROJECT_DIR/scripts/bootstrapit_update.sh.tmp" \
        "$PROJECT_DIR/scripts/bootstrapit_update.sh";
fi

source "$PROJECT_DIR/scripts/bootstrapit_update.sh";
