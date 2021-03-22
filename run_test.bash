#!/bin/bash


exs="examples/"
cd $exs
src=`ls | grep .py$`

echo $src

for i in $src; do
    n="${i%.*}"
    o=$n.nmigen
    v=$n.v

    rm $o -f

    e="python3 $i generate $v"
    echo $e "> $o"
    $e > $o
    echo "if __name__ == '__main__':" >> $o
    echo "    $n.main()" >> $o
done
exit 0

python3 test.py 1>doc/example.md
cp ram.stat doc/example.stat
