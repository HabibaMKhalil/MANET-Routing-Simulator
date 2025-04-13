# 🌐 MANET Routing Protocol Simulator  
*A comprehensive MANET routing simulator comparing proactive/reactive protocols with TCL/NS2, Python visualization, and performance analysis. Includes GUI-based node movement simulations.*

---

## 📖 Table of Contents  
- [Features](#-features)  
- [Performance Metrics](#-performance-metrics)  
- [Tech Stack](#-tech-stack)  
- [Quick Start](#-quick-start)  
- [File Structure](#-file-structure)  
- [Usage Examples](#-usage-examples)  
- [Expected Output](#-expected-output)  
- [License](#-license)

---

## ✨ Features  
- **Dual Protocol Simulation**:  
  - Proactive (DSDV) via `proactive_routing.py`  
  - Reactive (AODV) via `reactive_protocol.py`  
- **NS2/TCL Integration**: `sim.tcl` for network simulations  
- **Performance Analysis**:  
  - AWK script (`performance.awk`) calculates throughput, PDR, delay  
  - Python visualization (`graph.py`) generates metric comparisons  
- **Interactive GUI**: Node movement visualization with TKinter  

---

## 📊 Performance Metrics  
| Metric               | Description                          |
|----------------------|--------------------------------------|
| Throughput (kbps)    | Data transfer rate                   |
| Packet Delivery Ratio (%) | Successful packet reception     |
| Average Delay (s)    | End-to-end communication delay       |
| Packet Loss (%)      | Percentage of lost packets           |
| Overhead (%)         | Routing protocol overhead            |

---

## 🛠️ Tech Stack 
- **NS2** (Network Simulator 2)  
- **TCL** (Simulation scripting)  
- **Python** (Visualization/GUI)  
- **AWK** (Log processing)  

---

## 🚀 Quick Start  
1. Run NS2 simulation:  
   ```bash
   ns sim.tcl <nodes> <protocol> <src> <dest> <src2> <dest2>
   ```
   
2. Generate metrics:
  ```bash
  awk -f performance.awk output.tr > performance.txt
  ```

3. Visualize results:
  ```bash
  python3 graph.py
  ```

## 📂 File Structure
                            
├── sim.tcl                  # NS2 simulation script                                  
├── performance.awk          # Metric calculation                            
├── graph.py                 # Results visualization                            
├── proactive_routing.py     # DSDV GUI simulator                     
└── reactive_protocol.py     # AODV GUI simulator                               

## 📝 Usage Examples

1. NS2 Command:
  ```bash
  ns sim.tcl 20 AODV 1 5 3 8  # 20 nodes, AODV protocol, two routes
  ```

2. GUI Simulation:
  ```bash
  python3 proactive_routing.py  # DSDV interactive mode
  ```

## 📊 Expected Output
Metrics Graph
