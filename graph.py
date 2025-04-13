import matplotlib.pyplot as plt

# Read the results from throughput.txt
results = {}
with open("performance.txt", "r") as f:
    for line in f:
        if ":" in line:
            key, value = line.strip().split(": ")
            results[key] = float(value)

# Data for plotting
metrics = ["Throughput (kbps)", "PDR (%)", "Average Delay (s)", "Packet Loss (%)", "Overhead (%)"]
values = [results["Throughput (kbps)"], results["PDR (%)"], results["Average Delay (s)"], results["Packet Loss (%)"], results["Overhead (%)"]]

# Create the plot
plt.figure(figsize=(10, 6))
plt.bar(metrics, values, color=['blue', 'green', 'red', 'purple', 'orange'])
plt.title("Network Performance Metrics")
plt.xlabel("Metric")
plt.ylabel("Value")
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()
