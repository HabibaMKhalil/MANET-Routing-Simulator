# 🌐 MANET Routing Protocol Simulator  
*Comparing Proactive vs Reactive Routing in Mobile Ad-Hoc Networks*  

![Demo](https://via.placeholder.com/800x400?text=MANET+Simulation+Screenshot)  

## ✨ Features  
- **Dual Protocol Simulation**:  
  - Proactive (DSDV) via `proactive_routing.py`  
  - Reactive (AODV) via `reactive_protocol.py`  
- **NS2/TCL Integration**: `sim.tcl` for network simulations  
- **Performance Analysis**:  
  - AWK script (`performance.awk`) calculates throughput, PDR, delay  
  - Python visualization (`graph.py`) generates metric comparisons  
- **Interactive GUI**: Node movement visualization with TKinter  

## 📊 Performance Metrics  
- Throughput (kbps)  
- Packet Delivery Ratio (%)  
- Average Delay (s)  
- Packet Loss (%)  
- Overhead (%)  

## 🛠️ Tech Stack  
- **NS2** (Network Simulator 2)  
- **TCL** (Simulation scripting)  
- **Python** (Visualization/GUI)  
- **AWK** (Log processing)  

## 🚀 Quick Start  
1. Run NS2 simulation:  
   ```bash
   ns sim.tcl <nodes> <protocol> <src> <dest> <src2> <dest2>
   # Example:
   ns sim.tcl 20 AODV 1 5 3 8
Generate metrics:

bash
Copy
awk -f performance.awk output.tr > performance.txt
Visualize results:

bash
Copy
python3 graph.py
For GUI simulations:

bash
Copy
python3 proactive_routing.py  # or reactive_protocol.py
📂 File Structure
Copy
.
├── sim.tcl                  # NS2 simulation script
├── performance.awk          # Metric calculation
├── graph.py                 # Results visualization
├── proactive_routing.py     # DSDV GUI simulator
├── reactive_protocol.py     # AODV GUI simulator
└── performance.txt          # Generated metrics
📝 Usage Examples
1. NS2 Simulation:

bash
Copy
ns sim.tcl 15 DSDV 2 10  # 15 nodes, DSDV protocol, src=2, dest=10
2. GUI Simulation:

python
Copy
python3 reactive_protocol.py  # Interactive AODV simulation
📊 Expected Output
Metrics Graph
