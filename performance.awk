BEGIN {
    recvdSize = 0
    txsize = 0
    drpSize = 0
    totalDelay = 0
    totalPackets = 0
    startTime = 400
    stopTime = 0
    totalLost = 0
    pktSize = 0
    hdrSize = 0
    overhead = 0
}

{
    event = $1
    time = $2
    node_id = $3
    pkt_size = $8
    level = $4

    # Store start time
    if (level == "AGT" && event == "s") {
        if (time < startTime) {
            startTime = time
        }
        txsize++   # Transmitted packets count
    }

    # Update total received packets' size and store packet arrival time
    if (level == "AGT" && event == "r") {
        if (time > stopTime) {
            stopTime = time
        }
        recvdSize++   # Received packets count
        totalDelay += (time - startTime)  # Calculate delay
        totalPackets++  # Total packets (received + transmitted)
    }

    # Handle dropped packets
    if (level == "AGT" && event == "D") {
        drpSize++   # Dropped packets count
        totalLost++  # Increment lost packet count
    }

    # Handle packet overhead (header size)
    if (pkt_size > 0) {
        hdrSize = pkt_size % 400
        pktSize += (pkt_size - hdrSize)
    }
}

END {
    # Calculate throughput, PDR, delay, packet loss, and overhead
    duration = stopTime - startTime
    throughput = (recvdSize * 8) / duration  # Throughput in bps (converted to kbps)
    pdr = (recvdSize / txsize) * 100  # Packet Delivery Ratio (PDR)
    avgDelay = totalDelay / recvdSize  # Average delay per received packet
    packetLoss = (totalLost / totalPackets) * 100  # Packet loss percentage
    overhead = (pktSize / (recvdSize * 400)) * 100  # Overhead percentage

    # Output the results to the file performance.txt
    printf "Throughput (kbps): %.2f\n", throughput > "performance.txt"
    printf "PDR (%%): %.2f\n", pdr > "performance.txt"
    printf "Average Delay (s): %.2f\n", avgDelay > "performance.txt"
    printf "Packet Loss (%%): %.2f\n", packetLoss > "performance.txt"
    printf "Overhead (%%): %.2f\n", overhead > "performance.txt"
}
