import tkinter as tk
import random
import math

class Node:
    def __init__(self, node_id, x, y):
        self.node_id = node_id
        self.x = x
        self.y = y
        self.routes = {}  # Routing table (destination_node -> next_hop)
        self.neighbors = []
        self.rreq_id = 0  # Unique RREQ ID for this node to prevent duplicates
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


class Network:
    def __init__(self, root, communication_range=150):
        self.root = root
        self.nodes = []
        self.communication_range = communication_range
        self.movement_active = False
        self.selected_source = None
        self.selected_destination = None
        self.active_path = []

        # GUI settings (more space for the network)
        self.canvas = tk.Canvas(self.root, bg="#282c34", width=650, height=500, highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=20, pady=20, rowspan=5, sticky="nsew")
        self.canvas.bind("<Button-1>", self.select_node)

        # Adjusted size for message box (smaller)
        self.status_text = tk.Text(
            self.root, height=15, width=60, bg="#1e1e1e", fg="#ffffff", font=("Consolas", 12), state="normal"
        )
        self.status_text.grid(row=0, column=1, padx=20, pady=20, rowspan=5, sticky="nsew")

        # Buttons remain on the right
        self.start_button = tk.Button(
            self.root, text="Start Movement", font=("Helvetica", 12, "bold"), bg="#61afef", fg="white",
            activebackground="#98c379", activeforeground="black", command=self.start_movement
        )
        self.start_button.grid(row=6, column=2, padx=20, pady=5, sticky="ew")

        self.stop_button = tk.Button(
            self.root, text="Stop Movement", font=("Helvetica", 12, "bold"), bg="#e06c75", fg="white",
            activebackground="#d19a66", activeforeground="black", command=self.stop_movement
        )
        self.stop_button.grid(row=7, column=2, padx=20, pady=5, sticky="ew")

        self.send_button = tk.Button(
            self.root, text="Send Data", font=("Helvetica", 12, "bold"), bg="#98c379", fg="white",
            activebackground="#56b6c2", activeforeground="black", command=self.send_data
        )
        self.send_button.grid(row=8, column=2, padx=20, pady=5, sticky="ew")

        self.clear_button = tk.Button(
            self.root, text="Clear Logs", font=("Helvetica", 12, "bold"), bg="#c678dd", fg="white",
            activebackground="#abb2bf", activeforeground="black", command=self.clear_logs
        )
        self.clear_button.grid(row=9, column=2, padx=20, pady=5, sticky="ew")

        # Responsive layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(5, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=3)

        self.create_nodes()
        self.update_neighbors()
        self.draw_network()

        # Log initial message
        self.update_status("Hello MANET")

    def create_nodes(self):
        for node_id in range(1, 20):  # Create 10 nodes
            x = random.randint(50, 700)
            y = random.randint(50, 400)
            node = Node(node_id, x, y)
            self.nodes.append(node)

    def update_neighbors(self):
        """Update neighbors for each node based on distance and communication range."""
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

            self.canvas.create_oval(
                node.x - 15, node.y - 15, node.x + 15, node.y + 15,
                fill=fill_color, outline="#ffffff", width=2
            )
            self.canvas.create_text(node.x, node.y, text=str(node.node_id), fill="#ffffff")

        for node in self.nodes:
            for neighbor in node.neighbors:
                self.canvas.create_line(
                    node.x, node.y, neighbor.x, neighbor.y,
                    fill="#abb2bf", dash=(4, 2)
                )

        # Draw active path if it exists
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

        # Reset active path when a new source is selected
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
            if (node.x - 15 <= x <= node.x + 15) and (node.y - 15 <= y <= node.y + 15):
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

        # Simulate AODV's route discovery process
        self.update_status(f"Node {source.node_id} is sending RREQ to find a route to Node {destination.node_id}.")
        path = self.find_route(source, destination)
        if path:
            self.active_path = path
            self.update_status(f"Data successfully sent along the path: {self.path_to_string(path)}")
        else:
            self.update_status("No route found between the source and destination nodes.")
        self.draw_network()

    def find_route(self, source, destination):
        visited = set()
        queue = [[source]]
        self.update_status(f"Source Node {source.node_id} is looking for a route to Node {destination.node_id}...")

        while queue:
            path = queue.pop(0)
            node = path[-1]

            # Check if destination has been reached
            if node == destination:
                self.update_status(f"Route found: {self.path_to_string(path)}")
                return path

            if node not in visited:
                visited.add(node)

                # Simulate forwarding RREQ by intermediate nodes
                for neighbor in node.neighbors:
                    if neighbor not in visited:
                        new_path = list(path)
                        new_path.append(neighbor)
                        queue.append(new_path)
                        self.update_status(f"Node {node.node_id} forwards RREQ to Node {neighbor.node_id}.")

        self.update_status("No path found.")
        return None  # No path found

    def path_to_string(self, path):
        return " -> ".join(f"Node {node.node_id}" for node in path)

    def update_status(self, message):
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)

    def clear_logs(self):
        self.status_text.delete(1.0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("MANET Reactive Routing Protocol Simulator")
    root.geometry("900x700")
    root.configure(bg="#282c34")

    network = Network(root)
    root.mainloop()
