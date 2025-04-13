import tkinter as tk
import random
import math
from collections import deque

class Node:
    def __init__(self, node_id, x, y):
        self.node_id = node_id
        self.x = x
        self.y = y
        self.routes = {}  # Routing table (destination_node -> next_hop)
        self.neighbors = []
        self.routing_timeout = {}  # Timeout for routes

    def move_randomly(self, max_width, max_height):
        self.x = random.randint(50, max_width - 50)
        self.y = random.randint(50, max_height - 50)

    def add_neighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def distance_to(self, other_node):
        return math.sqrt((self.x - other_node.x) ** 2 + (self.y - other_node.y) ** 2)

    def update_route(self, destination, next_hop):
        """Update the routing table."""
        self.routes[destination] = next_hop
        self.routing_timeout[destination] = 10  # Route timeout (just for simulation)
        return f"Route to Node {destination.node_id} via Node {next_hop.node_id} added."

    def clear_routes(self):
        """Clear all routes."""
        self.routes.clear()
        self.routing_timeout.clear()

    def set_initial_routes(self, nodes):
        """Set initial routes to all other nodes."""
        for node in nodes:
            if node != self:
                self.routes[node] = node
                self.routing_timeout[node] = 10  # Simulating active route

class Network:
    def __init__(self, root, communication_range=150):
        self.root = root
        self.nodes = []
        self.communication_range = communication_range
        self.movement_active = False
        self.selected_source = None
        self.selected_destination = None
        self.active_path = []

        # Set up the dark theme background for the entire window
        self.root.configure(bg="#282c34")
        
        # Canvas for the network
        self.canvas = tk.Canvas(self.root, bg="#282c34", width=650, height=500, highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=20, pady=20, rowspan=6, sticky="nsew")
        self.canvas.bind("<Button-1>", self.select_node)

        # Status text area
        self.status_text = tk.Text(
            self.root, height=15, width=60, bg="#1e1e1e", fg="#ffffff", font=("Consolas", 12), state="normal"
        )
        self.status_text.grid(row=6, column=0, padx=20, pady=20, sticky="nsew")

        # Buttons with dark theme
        self.start_button = tk.Button(
            self.root, text="Start Movement", font=("Helvetica", 12, "bold"), bg="#61afef", fg="white",
            activebackground="#98c379", activeforeground="black", command=self.start_movement
        )
        self.start_button.grid(row=0, column=1, padx=20, pady=5, sticky="ew")

        self.stop_button = tk.Button(
            self.root, text="Stop Movement", font=("Helvetica", 12, "bold"), bg="#e06c75", fg="white",
            activebackground="#d19a66", activeforeground="black", command=self.stop_movement
        )
        self.stop_button.grid(row=1, column=1, padx=20, pady=5, sticky="ew")

        self.send_button = tk.Button(
            self.root, text="Send Data", font=("Helvetica", 12, "bold"), bg="#98c379", fg="white",
            activebackground="#56b6c2", activeforeground="black", command=self.send_data
        )
        self.send_button.grid(row=2, column=1, padx=20, pady=5, sticky="ew")

        self.clear_button = tk.Button(
            self.root, text="Clear Logs", font=("Helvetica", 12, "bold"), bg="#c678dd", fg="white",
            activebackground="#abb2bf", activeforeground="black", command=self.clear_logs
        )
        self.clear_button.grid(row=3, column=1, padx=20, pady=5, sticky="ew")

        self.show_routes_button = tk.Button(
            self.root, text="Show Routing Tables", font=("Helvetica", 12, "bold"), bg="#56b6c2", fg="white",
            activebackground="#98c379", activeforeground="black", command=self.show_routing_tables
        )
        self.show_routes_button.grid(row=4, column=1, padx=20, pady=5, sticky="ew")

        self.stimulate_routes_button = tk.Button(
            self.root, text="Stimulate Routing", font=("Helvetica", 12, "bold"), bg="#61afef", fg="white",
            activebackground="#98c379", activeforeground="black", command=self.stimulate_routing
        )
        self.stimulate_routes_button.grid(row=5, column=1, padx=20, pady=5, sticky="ew")

        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_rowconfigure(3, weight=0)
        self.root.grid_rowconfigure(4, weight=0)
        self.root.grid_rowconfigure(5, weight=0)
        self.root.grid_rowconfigure(6, weight=1)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)

        self.create_nodes()
        self.update_neighbors()
        self.draw_network()

        # Log initial message
        self.update_status("Hello MANET")

    def create_nodes(self):
        for node_id in range(1, 16):  # 15 nodes
            x = random.randint(50, 700)
            y = random.randint(50, 400)
            node = Node(node_id, x, y)
            self.nodes.append(node)

        for node in self.nodes:
            node.set_initial_routes(self.nodes)

    def update_neighbors(self):
        for node in self.nodes:
            node.neighbors = []
        for i in range(len(self.nodes)):
            for j in range(i + 1, len(self.nodes)):
                if self.nodes[i].distance_to(self.nodes[j]) <= self.communication_range:
                    self.nodes[i].add_neighbor(self.nodes[j])
                    self.nodes[j].add_neighbor(self.nodes[i])

    def draw_network(self):
        self.canvas.delete("all")
        for node in self.nodes:
            fill_color = "#56b6c2"
            if node == self.selected_source:
                fill_color = "#e06c75"  # Red for source
            elif node == self.selected_destination:
                fill_color = "#98c379"  # Green for destination

            # Drawing a larger node with distinct borders
            self.canvas.create_oval(
                node.x - 20, node.y - 20, node.x + 20, node.y + 20,
                fill=fill_color, outline="#ffffff", width=3  # Increased border width
            )
            self.canvas.create_text(node.x, node.y, text=str(node.node_id), fill="#ffffff", font=("Arial", 10, "bold"))

        for node in self.nodes:
            for neighbor in node.neighbors:
                self.canvas.create_line(
                    node.x, node.y, neighbor.x, neighbor.y,
                    fill="#abb2bf", dash=(4, 2)
                )

        for i in range(len(self.active_path) - 1):
            node1 = self.active_path[i]
            node2 = self.active_path[i + 1]
            self.canvas.create_line(
                node1.x, node1.y, node2.x, node2.y,
                fill="#e06c75", width=3
            )

    def select_node(self, event):
        clicked_node = self.get_node_at(event.x, event.y)
        if not clicked_node:
            return

        if not self.selected_source:
            self.selected_source = clicked_node
            self.update_status(f"Selected Node {clicked_node.node_id} as Source.")
            self.active_path = []  # Clear previous path
        elif not self.selected_destination:
            self.selected_destination = clicked_node
            self.update_status(f"Selected Node {clicked_node.node_id} as Destination.")
        else:
            self.selected_source = clicked_node
            self.selected_destination = None
            self.update_status(f"Reset selection. Selected Node {clicked_node.node_id} as Source.")

        self.draw_network()

    def get_node_at(self, x, y):
        for node in self.nodes:
            if (node.x - 20 <= x <= node.x + 20) and (node.y - 20 <= y <= node.y + 20):
                return node
        return None

    def start_movement(self):
        if not self.movement_active:
            self.movement_active = True
            self.update_status("Node movement started.")
            self.active_path = []  # Clear any old path when movement starts
            self.move_nodes()

    def stop_movement(self):
        self.movement_active = False
        self.update_status("Node movement stopped.")

    def move_nodes(self):
        if self.movement_active:
            max_width = self.canvas.winfo_width()
            max_height = self.canvas.winfo_height()
            for node in self.nodes:
                node.move_randomly(max_width, max_height)
            self.update_neighbors()
            self.draw_network()
            self.root.after(500, self.move_nodes)

    def send_data(self):
        if not self.selected_source or not self.selected_destination:
            self.update_status("Select both Source and Destination nodes to send data.")
            return
        source = self.selected_source
        destination = self.selected_destination
        self.update_status(f"Sending data from Node {source.node_id} to Node {destination.node_id}...")

        path, hop_count = self.find_route(source, destination)
        if not path:
            self.update_status("No route found. Message cannot be delivered.")
            return

        self.update_status(f"Data sent via path: {' -> '.join(str(node.node_id) for node in path)} with {hop_count} hops.")
        self.active_path = path
        self.draw_network()

    def find_route(self, source, destination):
        """ Simple flood-based routing to find the shortest path (in terms of hops). """
        visited = set()
        queue = deque([(source, [source], 0)])  # Keep track of the number of hops in the queue

        while queue:
            current_node, path, hop_count = queue.popleft()
            if current_node == destination:
                return path, hop_count

            for neighbor in current_node.neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor], hop_count + 1))

        return None, None  # No path found

    def clear_logs(self):
        self.status_text.delete(1.0, tk.END)

    def show_routing_tables(self):
        # Create a new top-level window for routing tables
        routing_window = tk.Toplevel(self.root)
        routing_window.title("Routing Tables")
        routing_window.geometry("600x400")  # Set the size of the window

        # Create a scrollable text widget
        routing_text = tk.Text(routing_window, height=20, width=70, bg="#1e1e1e", fg="#ffffff", font=("Consolas", 12))
        routing_text.grid(row=0, column=0, padx=10, pady=10)

        # Add a vertical scrollbar
        scrollbar = tk.Scrollbar(routing_window, command=routing_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        routing_text.config(yscrollcommand=scrollbar.set)

        # Populate the routing table with paths and costs
        for node in self.nodes:
            routing_text.insert(tk.END, f"Node {node.node_id} Routing Table:\n")
            for destination, next_hop in node.routes.items():
                # Calculate the number of hops
                hops = self.get_hop_count(node, destination)
                routing_text.insert(tk.END, f"  Destination Node {destination.node_id}: Next Hop -> Node {next_hop.node_id}, Hops: {hops}\n")
            routing_text.insert(tk.END, "\n")  # Add an empty line between nodes

        routing_text.config(state="disabled")  # Disable editing the text box

    def get_hop_count(self, source, destination):
        """Calculate the hop count between source and destination."""
        visited = set()
        queue = deque([(source, 0)])  # Start with hop count of 0

        while queue:
            current_node, hop_count = queue.popleft()
            if current_node == destination:
                return hop_count

            for neighbor in current_node.neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, hop_count + 1))

        return 0  # Return infinity if no path is found

    def stimulate_routing(self):
        for node in self.nodes:
            for neighbor in node.neighbors:
                for destination, next_hop in neighbor.routes.items():
                    if destination != node:
                        node.update_route(destination, neighbor)
        self.update_status("Routing stimulated and updated across the network.")

    def update_status(self, message):
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("MANET Simulation")
    app = Network(root)
    root.mainloop()
