#!/bin/bash


i=$1
if [ ! -f "$i" ]; then
    echo "failed to find $i"
    exit 1
fi

n="${i%.*}"
o=$n.nmigen
v=$n.v

rm $o -f

e="python3 $i generate $v"
echo $e "> $o"
$e > $o
echo "if __name__ == '__main__':" >> $o
echo "    $n.main()" >> $o
