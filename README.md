# 🌐 MANET Routing Protocol Simulator  
*A comprehensive MANET routing simulator comparing proactive/reactive protocols with TCL/NS2, Python visualization, and performance analysis. Includes GUI-based node movement simulations.*

## 📌 Project Overview
A Mobile Ad-Hoc Network (MANET) simulator that **compares proactive (DSDV) and reactive (AODV) routing protocols** through:
- **NS2/TCL simulations** for network performance analysis  
- **Python visualization** of throughput, delay, and packet loss metrics  
- **Interactive GUI** demonstrating node movement and pathfinding  
- **AWK-based analytics** for processing simulation traces  

Key capabilities:  
✔️ Real-time protocol performance comparison  
✔️ Visual demonstration of route discovery (RREQ/RREP)  
✔️ Customizable network scenarios (15-50 nodes)  
✔️ Comprehensive metrics: PDR, overhead, latency 

## 📖 Table of Contents  
- [Features](#-features)  
- [Performance Metrics](#-performance-metrics)  
- [Tech Stack](#tech-stack)  
- [Quick Start](#-quick-start)  
- [File Structure](#-file-structure)  
- [Usage Examples](#-usage-examples)  
- [Expected Output](#-expected-output)

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
![NS2](https://github.com/user-attachments/assets/cdd459de-a210-4977-85fb-c649c6ac78ef)

    ```bash
    ns sim.tcl 20 AODV 1 5 3 8  # 20 nodes, AODV protocol, two routes
    ```

2. GUI Simulation:
![proactive routing ](https://github.com/user-attachments/assets/6a8e55df-faa3-4d20-b8fe-5bba3c2c5f68)
![reactive routing ](https://github.com/user-attachments/assets/f966b40b-275c-474f-aa25-28748e3022c1)

    ```bash
    python3 proactive_routing.py  # DSDV interactive mode
    ```

## 📊 Expected Output
![Metrics](https://github.com/user-attachments/assets/ec93d4c6-89da-47a5-9fd1-49e2cc45ad9f)
