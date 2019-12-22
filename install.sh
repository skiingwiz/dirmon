#!/bin/bash

dir=/opt/dirmon

this=$(readlink -f $(dirname $0))
mkdir -p $dir

cp $this/dirmon.py $this/dirmon.cfg $dir
cp $this/systemd/* /etc/systemd/system/
