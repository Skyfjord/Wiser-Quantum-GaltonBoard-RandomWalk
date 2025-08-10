from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from qiskit_ibm_runtime.fake_provider import FakeAlgiers
from qiskit_aer.noise import NoiseModel

n = int(input("Enter number of levels : "))
shots = int(input("Enter number of shots: "))
#n peg galton board
main_qubits = 2*n+1
ancilla_qubits = n

backend = FakeAlgiers()  # Use a realistic backend for simulation
noise_model = NoiseModel.from_backend(backend)

qc = QuantumCircuit(main_qubits + ancilla_qubits)

qc.x(n)

for i in range(n):
	control_qubit = main_qubits + i  # Control qubit for the current peg
	qc.h(control_qubit)
	
	for j in range(-i,i+1):
		qc.cswap(control_qubit, n-1+j, n+j)
		qc.cx(n+j, control_qubit)
		qc.barrier()  # Add a barrier for clarity
	
	qc.cswap(control_qubit, n+i, n+1+i)

qc.measure_all()

# Noiseless, all-to-all simulator
simulator = AerSimulator(noise_model=noise_model)
compiled_circuit = transpile(qc, simulator)

# Run with shots
# shots = 10_00
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
plt.xticks(rotation=90)
plt.show()

_ = input("Do you want to see the circuit diagram? (y/n) : ")
if _ == "y":
    print(qc.draw(output='text', 
                  fold=-1, 
          wire_order=[i for i in range(main_qubits + ancilla_qubits - 1, main_qubits - 1, -1)] + 
            [i for i in range(main_qubits)],
            plot_barriers=False) )
