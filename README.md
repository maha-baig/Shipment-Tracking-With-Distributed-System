# Distributed Causal Ordering and Clock Synchronization Visualizations

This repository contains four Python implementations of distributed systems algorithms for causal ordering and clock synchronization. Each script provides a graphical simulation using Tkinter and matplotlib. The implementations include:

- **BSS.py**: Demonstrates the **BSS (Birman-Schiper-Stephenson) Algorithm** for causal ordering using vector clocks.  
- **SES.py**: Implements the **SES (Schiper-Eggli-Sandoz) Algorithm** for causal ordering with vector clocks, where the receiver increments its clock upon message delivery.
- **matrix_clock.py**: Simulates **Matrix Clock** unicast message exchanges. Each process maintains a 3×3 matrix clock that is piggybacked on messages and merged on receipt.
- **bonus_task.py**: A bonus simulation of a real-world distributed supply chain system. Warehouses (W1, W2, and W3) exchange inventory update messages using matrix clocks to maintain causal consistency.

---

## Prerequisites

- **Python 3.x** (Tested on Python 3.7+)
- **Tkinter** (usually comes bundled with Python on most platforms)
- **Matplotlib**  
- **NumPy**  

### Installation of Dependencies

If you do not already have `matplotlib` and `numpy` installed, you can install them via pip:

```bash
pip install matplotlib numpy
```

---

## File Details and How to Run

### 1. BSS.py

**Description:**  
Simulates the BSS causal ordering algorithm. Three processes (P1, P2, and P3) are represented graphically.  
- **Behavior:**  
  - **Step 0:** All processes start with a vector clock of `[0, 0, 0]`.  
  - **Step 1:** P1 broadcasts a message by incrementing its own counter and sending its vector clock to P2 (immediate, solid arrow) and P3 (buffered, dashed arrow).  
  - **Step 2:** P2 receives the message and updates its clock (element-wise maximum).  
  - **Step 3:** P3 later receives the buffered message and updates its clock.
- **Interaction:**  
  - **Next Step** button: Advances the simulation one step.  
  - **Reset** button: Reinitializes the simulation.

**How to Run:**

```bash
python BSS.py
```

### 2. SES.py

**Description:**  
Simulates the SES causal ordering algorithm. Uses unicast messages with vector clocks where the receiver increments its counter upon message delivery.
- **Behavior:**  
  - **Step 0:** Initial state with all processes having vector clocks `[0, 0, 0]`.  
  - **Step 1:** P1 sends a message to P2 (clock increment and attached vector).  
  - **Step 2:** P2 receives the message, updates its clock (merging and incrementing its own counter).  
  - **Step 3:** P2 sends a buffered message to P3 (shown with a dashed arrow).  
  - **Step 4:** P3 receives and processes the buffered message, updating its clock.  
  - **Step 5:** P3 sends a message to P1.  
  - **Step 6:** P1 receives and updates its clock accordingly.
- **Interaction:**  
  - **Next Step** button: Moves the simulation forward by one event.  
  - **Reset** button: Resets the simulation to its initial state.

**How to Run:**

```bash
python SES.py
```

### 3. matrix_clock.py

**Description:**  
Simulates a Matrix Clock algorithm for unicast message exchanges between three processes. Each process maintains a full 3×3 matrix clock.
- **Behavior:**  
  - **Step 0:** All processes start with a 3×3 matrix clock filled with zeros.  
  - **Step 1:** P1 sends a message to P2 after incrementing its own counter in the matrix (its principle row).  
  - **Step 2:** P2 receives the message and merges its matrix with the received matrix (element-wise maximum per row).  
  - **Step 3:** P2 sends a message to P3 after updating its matrix.  
  - **Step 4:** P3 receives the message and updates its matrix accordingly.  
  - **Step 5:** P3 sends a message to P1, and finally,  
  - **Step 6:** P1 receives the message and updates its matrix.
- **Interaction:**  
  - **Next Step** button: Advances the simulation event-by-event.  
  - **Reset** button: Reinitializes the simulation.

**How to Run:**

```bash
python matrix_clock.py
```

### 4. bonus_task.py

**Description:**  
A bonus simulation that models a distributed supply chain system using matrix clocks. Three warehouses (W1, W2, and W3) exchange inventory updates.
- **Behavior:**  
  - **Step 0:** All warehouses start with a 3×3 matrix clock of zeros.  
  - **Step 1:** W1 sends an update ("Shipment dispatched from W1") to W2.  
  - **Step 2:** W2 receives the update and updates its matrix by merging.  
  - **Step 3:** W2 sends an update ("Shipment en route from W2") to W3.  
  - **Step 4:** W3 receives and updates its matrix.  
  - **Step 5:** W3 sends an update ("Shipment delivered to W3") to W1.  
  - **Step 6:** W1 receives the update and updates its matrix.
- **Interaction:**  
  - **Next Step** button: Processes the next event in the pre-defined sequence.  
  - **Reset** button: Resets the simulation to its initial state.

**How to Run:**

```bash
python bonus_task.py
```

---

## Setup and Running the Simulations

1. **Clone the Repository** (if applicable):

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Ensure Dependencies are Installed:**

   ```bash
   pip install matplotlib numpy
   ```

3. **Run Each Simulation:**

   - For **BSS** simulation:

     ```bash
     python BSS.py
     ```

   - For **SES** simulation:

     ```bash
     python SES.py
     ```

   - For **Matrix Clock** simulation:

     ```bash
     python matrix_clock.py
     ```

   - For **Bonus Task (Supply Chain)** simulation:

     ```bash
     python bonus_task.py
     ```

4. **Interacting with the Simulations:**

   - **Next Step Button:**  
     Click this button to advance the simulation one step at a time. Each click processes one event (e.g., sending a message, receiving a message, updating clocks).

   - **Reset Button:**  
     Click this button to reinitialize the simulation to its starting state. This resets the clocks and clears any progress.

   - **GUI Interface:**  
     Each simulation opens a new window showing either a graphical representation (using matplotlib) or a text-based log (in the bonus task). Follow on-screen labels and titles to understand the current state and event details.

---

## Expected Behavior

- **BSS.py and SES.py:**  
  You will see a graphical window with process nodes (P1, P2, P3) along with arrows representing message transmissions. The vector clocks for each process update according to the algorithm rules.

- **matrix_clock.py:**  
  The window displays process nodes with their 3×3 matrix clocks. Arrows with multi-line labels show the matrix attached to messages and the updates when messages are delivered.

- **bonus_task.py:**  
  This simulation displays three panels for warehouses (W1, W2, W3). Each panel shows the full matrix clock and a log of inventory updates. As you click "Next Step," the logs update to show the messages sent and received, along with the corresponding matrix clocks.

---

## Additional Notes

- The code is **well-commented** for clarity and understanding of each step in the simulation.
- Modify the **event sequences** or **GUI parameters** if you need to simulate different scenarios.
- These simulations are designed for educational purposes to demonstrate key concepts in distributed computing such as causal ordering and clock synchronization.

Feel free to reach out via the repository's issue tracker if you have any questions or need further assistance.

Happy Coding!