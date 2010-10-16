#!/bin/bash

MAIN="pyechonest"
submodules=`ls $MAIN | grep .py$ | sed -e 's/.py//g' `

#create the 'index' file
pydoc -w $MAIN

#create the other dudes
for s in $submodules; do pydoc -w $MAIN.$s; done

mv *.html doc/


mkdir -p doc/build
/usr/bin/env python setup.py build_sphinx

echo "all done!"