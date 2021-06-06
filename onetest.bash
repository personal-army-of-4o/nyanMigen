#!/bin/bash


i=$1
if [ ! -f "$i" ]; then
    echo "failed to find $i"
    exit 1
fi

n="${i%.*}"
o=$n.nmigen
il=$n.il
v=$n.v

if [ "$2" == "-g" ]; then
	rm $o -f
	e="python3 $i generate -t il $il"
	echo "$e > $o"
	$e > $o
	echo "if __name__ == '__main__':" >> $o
	echo "    $n.main()" >> $o
fi
if [ "$2" == "-s" ]; then
	yosys -Q -p "read_ilang blink.il; proc; opt -full; write_verilog blink.v"
fi

