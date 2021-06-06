#!/bin/bash


onetest=`pwd`/onetest.bash
exs="examples/"

echo "option: $1"

if [ "$1" == "-d" ]; then
	docker run -t -v `pwd`:/workdir nm bash -c "cd /workdir ; bash run_test.bash -g"
	docker run -t -v `pwd`:/workdir yosys bash -c "cd /workdir ; bash run_test.bash -s"
else
	cd $exs
	src=`ls | grep .py$`
	if [ "$1" == "-g" ] || [ "$1" == "" ]; then
		echo $src
		n=0
		for i in $src; do
		    bash $onetest $i -g &
		    pids[${n}]=$!
		    n=$n+1
		done

		for pid in ${pids[*]}; do
		    wait $pid
		done
	fi

	if [ "$1" == "-s" ] || [ "$1" == "" ]; then
		echo $src
		n=0
		for i in $src; do
		    bash $onetest $i -s &
		    pids[${n}]=$!
		    n=$n+1
		done

		for pid in ${pids[*]}; do
		    wait $pid
		done
	fi
fi
