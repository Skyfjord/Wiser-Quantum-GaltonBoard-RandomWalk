from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
from qiskit_ibm_runtime.fake_provider import FakeAlgiers
from qiskit_aer.noise import NoiseModel

number_qubits = int(input("Enter number of position qubits: "))
iterator = int(input("Enter number of walk steps: "))
bias = float(input("Enter bias (between -1 and 1): "))
shots = int(input("Enter number of shots: "))

backend = FakeAlgiers()  # Use a realistic backend for simulation
noise_model = NoiseModel.from_backend(backend)

qr = QuantumRegister(number_qubits + 1, 'q')  # position + coin
cr = ClassicalRegister(number_qubits, 'c')    # measure only position
qc = QuantumCircuit(qr, cr)

coin_idx = number_qubits  # last qubit index is coin

def initial_state(qc):
    # Position in the center
    center_pos = (2 ** number_qubits) // 2
    binary_center = format(center_pos, f'0{number_qubits}b')

    for qubit_index, bit in enumerate(binary_center[::-1]):  
        if bit == '1':
            qc.x(qubit_index)

    # Unbiased coin flip
    qc.h(coin_idx)
    qc.s(coin_idx)
    # qc.rz(bias, coin_idx)  # Apply a rotation around Z-axis for bias
    # qc.s(coin_idx)
    # qc.s(coin_idx)
    
def walk_step(qc):
    qc.h(coin_idx)
    # --- MOVE RIGHT (Addition) ---
    # qc.x(coin_idx)  # Flip coin to select |1> for right move
    for m in range(number_qubits-1, 0, -1):
        controls = [coin_idx] + list(range(m))   # control on coin and bits 0..m-1
        qc.mcx(controls, m)                 # flip bit m if coin=1 and bits0..m-1 are all 1
    qc.mcx([coin_idx], 0)

    # --- MOVE LEFT (Subtraction) ---
    qc.x(coin_idx)  # Restore coin
    for m in range(number_qubits - 1, 0, -1):
        controls = [coin_idx] + list(range(m))
        ctrl_state_str = '0' * (m) + '1'
        qc.mcx(controls, m, ctrl_state=ctrl_state_str)

    qc.mcx([coin_idx], 0)

initial_state(qc)
for _ in range(iterator):
	walk_step(qc)

qc.measure(range(number_qubits), range(number_qubits))

simulator = AerSimulator(noise_model=noise_model)
compiled_circuit = transpile(qc, simulator)

result = simulator.run(compiled_circuit, shots=shots).result()
counts = result.get_counts()

histogram = {}
for bitstring, count in counts.items():
    pos_value = int(bitstring.replace(' ', ''), 2)
    histogram[pos_value] = histogram.get(pos_value, 0) + count

plt.bar(histogram.keys(), histogram.values())
plt.xlabel("Position")
plt.ylabel("Counts")
plt.title("Symmetric Quantum Random Walk Distribution")
plt.show()

# Print circuit
_ = input("Do you want to see the circuit diagram? (y/n) : ")
if _ == "y":
    print(qc.draw(output='text', 
				#   fold=-1,
				  ))