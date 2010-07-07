#!/bin/bash

MAIN="pyechonest"
submodules=`ls $MAIN | grep .py$ | sed -e 's/.py//g' `

#create the 'index' file
pydoc -w $MAIN

#create the other dudes
for s in $submodules; do pydoc -w $MAIN.$s; done

mv *.html doc/
echo "all done!" 