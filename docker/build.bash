#!/bin/bash

pushd nm
if [ "$?" != "0" ]; then
	exit
fi
bash build.bash
if [ "$?" != "0" ]; then
	exit
fi
popd
if [ "$?" != "0" ]; then
	exit
fi
pushd ys
if [ "$?" != "0" ]; then
	exit
fi
bash build.bash
if [ "$?" != "0" ]; then
	exit
fi

