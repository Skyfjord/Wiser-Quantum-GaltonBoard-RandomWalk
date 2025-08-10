from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

n = int(input("Enter number of levels : "))
main_qubits = n+2
ancilla_qubits = n

qc = QuantumCircuit(main_qubits + ancilla_qubits)
qc.x(1)

for i in range(n):
	control_qubit = main_qubits + i
	qc.h(control_qubit)
	qc.cswap(control_qubit, i, i+1)
	qc.cx(i+1, control_qubit)
	qc.cswap(control_qubit, i+1, i+2)

qc.measure_all()

# Noiseless, all-to-all simulator
simulator = AerSimulator()
compiled_circuit = transpile(qc, simulator)

# Run with shots
shots = 10_000
result = simulator.run(compiled_circuit, shots=shots).result()
counts = result.get_counts()

# Convert counts to probabilities
# Marginalize out the last n ancilla bits
marginalized_counts = {}
for bitstring, count in counts.items():
    # Extract the main qubits (first `main_qubits` bits)
    main_bits = bitstring[ancilla_qubits:]
    if main_bits not in marginalized_counts:
        marginalized_counts[main_bits] = 0
    marginalized_counts[main_bits] += count

# Convert marginalized counts to probabilities
marginalized_probs = {k: v/shots for k, v in marginalized_counts.items()}

marginalized_probs = dict(sorted(marginalized_probs.items()))
# Plot marginalized probabilities
plt.figure(figsize=(12, 6))
plt.bar(marginalized_probs.keys(), marginalized_probs.values())
plt.xlabel("Bitstring (Main Qubits)")
plt.ylabel("Probability")
plt.title("Marginalized Probability Distribution")
plt.xticks(rotation=45)
plt.show()

_ = input("Do you want to see the circuit diagram? (y/n) : ")
if _ == "y":
    print(qc.draw(output='text', 
                  fold=-1, 
          wire_order=[i for i in range(main_qubits + ancilla_qubits - 1, main_qubits - 1, -1)] + 
            [i for i in range(main_qubits)],
            plot_barriers=False) )
