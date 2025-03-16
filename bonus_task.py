import tkinter as tk
import copy

class SupplyChainMatrixSimulator:
    def __init__(self, master):
        """
        Initialize the distributed supply chain simulation.
        
        Args:
            master: The parent Tkinter window.
        """
        self.master = master
        self.master.title("Distributed Supply Chain Simulation using Matrix Clocks")
        self.setup_ui()
        self.reset_simulation()

    def setup_ui(self):
        """
        Set up the user interface with three frames (one for each warehouse) showing:
        - The warehouse name.
        - Its full 3x3 matrix clock.
        - A log (text area) displaying sent/received inventory updates.
        Also create Next Step and Reset buttons.
        """
        # Create frames for each warehouse: W1, W2, W3.
        self.frames = {}
        self.clock_labels = {}
        self.log_texts = {}
        for wh in ['W1', 'W2', 'W3']:
            frame = tk.Frame(self.master, bd=2, relief=tk.RIDGE, padx=10, pady=10)
            frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=5, pady=5)
            title = tk.Label(frame, text=wh, font=("Arial", 14, "bold"))
            title.pack()
            clock_label = tk.Label(frame, text="Matrix Clock:\n[[0, 0, 0],\n [0, 0, 0],\n [0, 0, 0]]",
                                   font=("Arial", 10), justify=tk.LEFT)
            clock_label.pack()
            log = tk.Text(frame, width=30, height=15)
            log.pack(expand=True, fill=tk.BOTH)
            self.frames[wh] = frame
            self.clock_labels[wh] = clock_label
            self.log_texts[wh] = log

        # Create a control frame with Next Step and Reset buttons.
        control_frame = tk.Frame(self.master)
        control_frame.pack(side=tk.BOTTOM, pady=5)
        self.next_button = tk.Button(control_frame, text="Next Step", command=self.next_step)
        self.next_button.pack(side=tk.LEFT, padx=5)
        self.reset_button = tk.Button(control_frame, text="Reset", command=self.reset_simulation)
        self.reset_button.pack(side=tk.LEFT, padx=5)

    def reset_simulation(self):
        """
        Reset the simulation state:
        - All warehouses start with a 3x3 matrix clock initialized to zeros.
        - Clear the log for each warehouse.
        - Reset the simulation event counter.
        - Predefine a sequence of events.
        """
        self.current_event = 0  # Event counter

        # Define initial 3x3 matrix clocks for each warehouse.
        self.matrix_clocks = {
            'W1': [[0, 0, 0] for _ in range(3)],
            'W2': [[0, 0, 0] for _ in range(3)],
            'W3': [[0, 0, 0] for _ in range(3)]
        }
        # Clear logs.
        self.logs = {
            'W1': [],
            'W2': [],
            'W3': []
        }
        # Define a predetermined sequence of events.
        # Each event is a dictionary with type ("send" or "deliver"),
        # sender, receiver, and message text.
        self.events = [
            # W1 sends an update to W2.
            {"type": "send", "sender": "W1", "receivers": ["W2"], "message": "Shipment dispatched from W1"},
            {"type": "deliver", "sender": "W1", "receiver": "W2", "message": "Shipment dispatched from W1"},
            # W2 sends an update to W3.
            {"type": "send", "sender": "W2", "receivers": ["W3"], "message": "Shipment en route from W2"},
            {"type": "deliver", "sender": "W2", "receiver": "W3", "message": "Shipment en route from W2"},
            # W3 sends an update to W1.
            {"type": "send", "sender": "W3", "receivers": ["W1"], "message": "Shipment delivered to W3"},
            {"type": "deliver", "sender": "W3", "receiver": "W1", "message": "Shipment delivered to W3"}
        ]
        self.update_ui()
        self.next_button.config(state=tk.NORMAL)

    def matrix_to_string(self, matrix):
        """
        Convert a 3x3 matrix (list of lists) to a multi-line string.
        
        Args:
            matrix: The matrix clock.
            
        Returns:
            A string representation of the matrix.
        """
        return "\n".join(str(row) for row in matrix)

    def update_ui(self):
        """
        Update each warehouse's clock display and log text area.
        """
        for wh in ['W1', 'W2', 'W3']:
            self.clock_labels[wh].config(text="Matrix Clock:\n" + self.matrix_to_string(self.matrix_clocks[wh]))
            self.log_texts[wh].delete("1.0", tk.END)
            for entry in self.logs[wh]:
                self.log_texts[wh].insert(tk.END, entry + "\n")

    def merge_matrices(self, current, received):
        """
        Merge two 3x3 matrices by taking the element-wise maximum of corresponding rows.
        
        Args:
            current: The receiver's current matrix clock.
            received: The matrix clock attached to the received message.
            
        Returns:
            A new merged matrix.
        """
        merged = []
        for i in range(3):
            merged.append([max(a, b) for a, b in zip(current[i], received[i])])
        return merged

    def send_message(self, sender, receivers, message_text):
        """
        Process a send event:
        - The sender increments its own counter in its principle row.
        - The updated matrix is attached as the message timestamp.
        - The sender's log is updated.
        
        Args:
            sender: The sending warehouse (e.g. "W1").
            receivers: List of intended recipient(s).
            message_text: The update message.
            
        Returns:
            A deep copy of the sender's matrix clock to be attached to the message.
        """
        # Map warehouse to index: W1 -> 0, W2 -> 1, W3 -> 2.
        index = {"W1": 0, "W2": 1, "W3": 2}[sender]
        # Increment sender's own counter in its principle row.
        self.matrix_clocks[sender][index][index] += 1
        # Copy the updated matrix to attach with the message.
        msg_matrix = copy.deepcopy(self.matrix_clocks[sender])
        # Log the send event.
        self.logs[sender].append(f"Sent: {message_text} (ts: {self.matrix_to_string(msg_matrix)})")
        return msg_matrix

    def deliver_message(self, receiver, sender, msg_matrix, message_text):
        """
        Process a delivery event:
        - The receiver merges its matrix clock with the received matrix.
        - The receiver's log is updated.
        
        Args:
            receiver: The warehouse receiving the update.
            sender: The warehouse that sent the update.
            msg_matrix: The matrix clock attached to the message.
            message_text: The update message.
        """
        # Merge the receiver's matrix with the received matrix.
        self.matrix_clocks[receiver] = self.merge_matrices(self.matrix_clocks[receiver], msg_matrix)
        # Log the delivery event.
        self.logs[receiver].append(f"Received from {sender}: {message_text} (ts: {self.matrix_to_string(msg_matrix)})")

    def next_step(self):
        """
        Process the next event in the sequence.
        """
        if self.current_event < len(self.events):
            event = self.events[self.current_event]
            if event["type"] == "send":
                # Process send event.
                sender = event["sender"]
                receivers = event["receivers"]
                message_text = event["message"]
                # Update sender's matrix clock and attach a deep copy.
                msg_matrix = self.send_message(sender, receivers, message_text)
                # Save the attached matrix for later delivery.
                event["matrix"] = msg_matrix
            elif event["type"] == "deliver":
                # Process delivery event.
                sender = event["sender"]
                receiver = event["receiver"]
                message_text = event["message"]
                # Look back for the corresponding send event to get the message matrix.
                msg_matrix = None
                for e in self.events[:self.current_event]:
                    if e.get("type") == "send" and e["sender"] == sender and e["message"] == message_text:
                        msg_matrix = e.get("matrix")
                        break
                if msg_matrix is not None:
                    self.deliver_message(receiver, sender, msg_matrix, message_text)
            self.current_event += 1
            self.update_ui()
        else:
            self.next_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = SupplyChainMatrixSimulator(root)
    root.mainloop()
