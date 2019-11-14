#!/bin/bash

target="semiservermgr"

target_file="$target/usr/local/bin/semiservermgr"
source_file="../src/semiservermgr.py"

#mkdir -p $target_dir
cp $source_file $target_file

fakeroot dpkg-deb --build $target
