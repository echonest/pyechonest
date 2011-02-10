#!/bin/bash

# ==============================================
# = This script will make a pyechonest release =
# ==============================================

args=`getopt to: $*`

function usage() {
    echo "$0 -o <build result> [-t <temp work dir>]"
}

if [ $? != 0 ]; then
        usage
        exit 2
fi

EXPORT_LOCATION=""
TEMP_LOCATION="/tmp/pyechonest"
set -- $args
for i
do
    case "$i" in
        -o)
            EXPORT_LOCATION=$2; shift;
            shift;;
        -t)
            TEMP_LOCATION=$2; shift;
            shift;;
        --)
            shift; break;;
    esac
done

if [ -z "${EXPORT_LOCATION}" ]; then
    usage
    exit 2
fi

# check that sphinx is installed, we need it to make the docs!
type -P sphinx-build &>/dev/null || { echo "Please install sphinx (easy_install -U sphinx)" >&2; exit 1; }
# export a clean copy to export location
svn export . "$TEMP_LOCATION"

# remove this script, as well as our test files or .pyc files
rm -rf "$TEMP_LOCATION"/mkrelease.sh
rm -rf "$TEMP_LOCATION"/test.py
rm -rf "$TEMP_LOCATION"/test
rm -rf "$TEMP_LOCATION"/tmp

# remake the docs
cd "$TEMP_LOCATION" && \
    python "$TEMP_LOCATION"/setup.py build_sphinx

# remove pyc files
find "$TEMP_LOCATION" -name "*.pyc" | xargs rm -rf

# make zip and copy
cd "$TEMP_LOCATION" && \
    zip -r "$EXPORT_LOCATION"/pyechonest.zip .

# make egg and copy
cd "$TEMP_LOCATION" && \
    python "$TEMP_LOCATION"/setup.py bdist_egg && \
    cp dist/*.egg "$EXPORT_LOCATION"

# remove temp dir
rm -rf "$TEMP_LOCATION"
