#!/bin/bash


onetest=`pwd`/onetest.bash
exs="examples/"
cd $exs
src=`ls | grep .py$`

echo $src

n=0
for i in $src; do
    bash $onetest $i &
    pids[${n}]=$!
    n=$n+1
done

for pid in ${pids[*]}; do
    wait $pid
done
