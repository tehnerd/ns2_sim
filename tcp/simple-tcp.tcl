#Create a simulator object
set ns [new Simulator]

#Open the ns trace file
set nf [open out.ns w]
set n0w [open n0w.ns w]
#set ql [open ql.ns w]

$ns trace-all $nf


puts [$ns info class]

proc finish {} {
        global ns nf
        $ns flush-trace
        close $nf
        exit 0
}

#Create two nodes
set n0 [$ns node]
set n1 [$ns node]



proc plotWindow {tcpSource outfile} {
   global ns
   set now [$ns now]
   set cwnd [$tcpSource set cwnd_]

# the data is recorded in a file called congestion.xg (this can be plotted # using xgraph or gnuplot. this example uses xgraph to plot the cwnd_
    puts  $outfile  "$now $cwnd"
    $ns at [expr $now+0.001] "plotWindow $tcpSource  $outfile"
  }


#error module
set loss_module [new ErrorModel]
$loss_module set rate_ 0.000125
$loss_module ranvar [new RandomVariable/Uniform]



#Create a duplex link between the nodes
set queuesize 3000
$ns duplex-link $n0 $n1 10Gb 10ms DropTail 
$ns queue-limit $n0 $n1 $queuesize
#$ns link-lossmodel $loss_module $n0 $n1
#$ns trace-queue $n0 $n1 $ql



#Create a TCP agent and attach it to node n0
set tcp [new Agent/TCP/Linux]
set snk [new Agent/TCPSink/Sack1]



$tcp set syn_ true
$tcp set mtu_ 8950
$tcp set packetSize_ 8850
$tcp set timestamps_ true
$tcp set window_ 2000


$ns attach-agent $n0 $tcp
$ns attach-agent $n1 $snk

$ns connect $tcp $snk

$ns at 0 "$tcp select_ca cubic"
$ns at 0.0 "plotWindow $tcp $n0w"
$ns at 0.5 "$tcp advanceby 100000000"
$ns at 10.0 "finish"

#Run the simulation
$ns run
