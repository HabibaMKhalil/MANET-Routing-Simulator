# Check if the required arguments are passed
if { [llength $argv] < 2 } {
    puts "Usage: ns <script.tcl> <Number of Nodes> <Routing Protocol> <Source Node> <Destination Node> <Second Source Node> <Second Destination Node>"
    exit 1
}

# Assign command-line arguments to variables
set NODES [lindex $argv 0]
set PROTO [lindex $argv 1]
set SRC    [lindex $argv 2]
set DEST   [lindex $argv 3]
set SRC2  [lindex $argv 4]
set DEST2  [lindex $argv 5]

# Prompt the user for source and destination if not provided
if { $SRC == "" } {
    puts "Enter the source node (0 to [expr $NODES-1]): "
    flush stdout
    gets stdin SRC
}

if { $DEST == "" } {
    puts "Enter the destination node (0 to [expr $NODES-1]): "
    flush stdout
    gets stdin DEST
}

# Prompt the user for the second source and destination if not provided
if { $SRC2 == "" } {
    puts "Enter the source node (0 to [expr $NODES-1]): "
    flush stdout
    gets stdin SRC2
}

if { $DEST2 == "" } {
    puts "Enter the destination node (0 to [expr $NODES-1]): "
    flush stdout
    gets stdin DEST2
}

# Validate source and destination input
if { $SRC < 0 || $SRC >= $NODES || $DEST < 0 || $DEST >= $NODES } {
    puts "Error: Source or destination node out of range."
    exit 1
}

# Validate second source and destination input
if { $SRC2 < 0 || $SRC2 >= $NODES || $DEST2 < 0 || $DEST2 >= $NODES } {
    puts "Error: Source or destination node out of range."
    exit 1
}

# Define the output directory
set DIR_NAME "./"  ;# Use the current directory or specify your desired directory

# Define options
set val(chan)           Channel/WirelessChannel    ;# channel type
set val(prop)           Propagation/TwoRayGround   ;# radio-propagation model
set val(netif)          Phy/WirelessPhy            ;# network interface type
set val(mac)            Mac/802_11                 ;# MAC type
set val(ifq)            Queue/DropTail/PriQueue    ;# interface queue type
set val(ll)             LL                         ;# link layer type
set val(ant)            Antenna/OmniAntenna        ;# antenna model
set val(ifqlen)         50                         ;# max packet in ifq
set val(nn)             $NODES                     ;# number of mobilenodes
set val(rp)             $PROTO                     ;# routing protocol
set val(sr)             $SRC                       ;# source node
set val(dt)             $DEST                      ;# destination node
set val(sr2)            $SRC2                       ;# second source node
set val(dt2)            $DEST2                      ;# second destination node
set val(x)              1000                       ;# X dimension of topography
set val(y)              1000                       ;# Y dimension of topography
set val(stop)           200                        ;# time of simulation end

set OUT_NAME "${DIR_NAME}/${PROTO}_${NODES}"
set ns            [new Simulator]
set tracefd       [open "$OUT_NAME.tr" w]
set namtrace      [open "$OUT_NAME.nam" w]

$ns trace-all $tracefd
$ns namtrace-all-wireless $namtrace $val(x) $val(y)

# set up topography object
set topo [new Topography]
$topo load_flatgrid $val(x) $val(y)

# general operational descriptor. Stores the hop details in the network.
create-god $val(nn)

# configure the nodes
$ns node-config -adhocRouting $val(rp) \
    -llType $val(ll) \
    -macType $val(mac) \
    -ifqType $val(ifq) \
    -ifqLen $val(ifqlen) \
    -antType $val(ant) \
    -propType $val(prop) \
    -phyType $val(netif) \
    #-channelType $val(chan) \
    -channel [new $val(chan)] \
    -topoInstance $topo \
    -agentTrace ON \
    -routerTrace ON \
    -macTrace OFF \
    -movementTrace ON

for {set i 0} {$i < $val(nn) } { incr i } {
    set node_($i) [$ns node]
    $node_($i) set X_ [ expr 10+round(rand()*480) ]
    $node_($i) set Y_ [ expr 10+round(rand()*380) ]
    $node_($i) set Z_ 0.0
}

for {set i 0} {$i < $val(nn) } { incr i } {
    $ns at [ expr 15+round(rand()*60) ] "$node_($i) setdest [ expr 10+round(rand()*480) ] [ expr 10+round(rand()*380) ] [ expr 2+round(rand()*15) ]"
}

$ns at 0.0 "$node_($val(sr)) label SOURCE1"
$ns at 0.0 "$node_($val(dt)) label DESTINATION1"

$ns at 0.0 "$node_($val(sr2)) label SOURCE2"
$ns at 0.0 "$node_($val(dt2)) label DESTINATION2"

$node_($val(sr)) color deepskyblue
$ns at 0.0 "$node_($val(sr)) color deepskyblue"
$node_($val(dt)) color deepskyblue
$ns at 0.0 "$node_($val(dt)) color deepskyblue"

$ns at 0.0 "$node_($val(sr)) add-mark . blue circle"
$ns at 0.0 "$node_($val(dt)) add-mark . blue circle"

$node_($val(sr2)) color deepskyblue
$ns at 0.0 "$node_($val(sr2)) color orange"
$node_($val(dt2)) color deepskyblue
$ns at 0.0 "$node_($val(dt2)) color orange"

$ns at 0.0 "$node_($val(sr2)) add-mark . red circle"
$ns at 0.0 "$node_($val(dt2)) add-mark . red circle"

$ns at 5.0 "$node_($val(sr)) label SOURCE1"
$ns at 5.0 "$node_($val(dt)) label DESTINATION1"

$ns at 5.0 "$node_($val(sr2)) label SOURCE2"
$ns at 5.0 "$node_($val(dt2)) label DESTINATION2"

# Set a TCP connection between the user-defined source and destination nodes
set tcp [new Agent/TCP/Newreno]
$tcp set class_ 2
set sink [new Agent/TCPSink]
$ns attach-agent $node_($val(sr)) $tcp
$ns attach-agent $node_($val(dt)) $sink
$ns connect $tcp $sink
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ns at 10.0 "$ftp start"

# Set a TCP connection between the user-defined second source and destination nodes
set tcp [new Agent/TCP/Newreno]
$tcp set class_ 2
set sink [new Agent/TCPSink]
$ns attach-agent $node_($val(sr2)) $tcp
$ns attach-agent $node_($val(dt2)) $sink
$ns connect $tcp $sink
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ns at 10.0 "$ftp start"

# Define node initial position in nam
for {set i 0} {$i < $val(nn)} { incr i } {
    # 30 defines the node size for nam
    $ns initial_node_pos $node_($i) 30
}

# Telling nodes when the simulation ends
for {set i 0} {$i < $val(nn) } { incr i } {
    $ns at $val(stop) "$node_($i) reset";
}

# ending nam and the simulation
$ns at $val(stop) "$ns nam-end-wireless $val(stop)"
$ns at $val(stop) "stop"
$ns at 150 "$ns halt"
proc stop {} {
    global ns tracefd namtrace
    $ns flush-trace
    close $tracefd
    close $namtrace
    # Run AWK scripts for throughput and RPD, and save outputs to text files
    exec awk -f performance.awk $OUT_NAME.tr > performance.txt

}

$ns run
