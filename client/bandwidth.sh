#!/bin/bash

TC=/sbin/tc

IF=$2

BANDWIDTH=$3mbit

DELAY=$4ms
JITTER=$5ms
DELAY_PERCENT=$6%

LOSS=$7%

start() {
	$TC qdisc add dev $IF handle 1: root htb default 11
	$TC class add dev $IF parent 1:1 classid 1:11 htb rate $BANDWIDTH
	$TC qdisc add dev $IF parent 1:11 handle 10: netem delay $DELAY $JITTER $DELAY_PERCENT loss $LOSS
}

change() {
	$TC class change dev $IF parent 1:1 classid 1:11 htb rate $BANDWIDTH
	$TC qdisc change dev $IF parent 1:11 handle 10: netem delay $DELAY $JITTER $DELAY_PERCENT loss $LOSS
}

stop() {
	$TC qdisc del dev $IF root
}

show() {
	$TC -s qdisc ls dev $IF
}

case "$1" in
	start)
		echo -n "Starting bandwidth shaping: "
		start
		echo "done"
	;;
	change)
		change
		echo "done"
	;;
	stop)
		echo -n "Stopping bandwidth shaping: "
		stop
		echo "done"
	;;
	show)
		echo -n "Bandwidth shaping status for $IF:"
		show
		echo "done"
	;;
	*)
	pwd=$(pwd)
	echo "Usage: $0 {start [iface] [bandwidth (mbps)] [delay (ms)] [jitter (ms)] [delay_percent (%)] [loss (%)] | stop [iface] | show [iface]}"
	;;
esac

exit 0
