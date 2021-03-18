#!/bin/bash


exs="examples/"
cp *.json $exs
cd $exs
src=`ls | grep .py$`

echo $src

for i in $src; do
    n="${i%.*}"
    e="python3 $i generate $n.v -s"
    o=$n.nmigen
    echo $e "> $o"
    $e > $o
    echo "if __name__ == '__main__':" >> $o
    echo "    $n.main()" >> $o
done
exit 0

python3 test.py 1>doc/example.md
cp ram.stat doc/example.stat
