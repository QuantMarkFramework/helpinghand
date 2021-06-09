import tequila as tq
from tequila.circuit.circuit import QCircuit


def create_uent(n_qubits: int) -> QCircuit:
	circuit: QCircuit = QCircuit()
	for i in range(1, n_qubits, 2):
		circuit += tq.gates.CZ(target=i, control=i - 1)
	for i in range(2, n_qubits, 2):
		circuit += tq.gates.CZ(target=i, control=i - 1)
	return circuit


def create_rotations(n_qubits: int, depth_position: int):
	circuit: QCircuit = QCircuit()
	for qubit in range(n_qubits):
		circuit += tq.gates.Rz(f'{qubit}^{depth_position}_0', target=qubit)
		circuit += tq.gates.Rx(f'{qubit}^{depth_position}_1', target=qubit)
		circuit += tq.gates.Rz(f'{qubit}^{depth_position}_2', target=qubit)
	return circuit


def create_hardware_ansatz(
	n_qubits: int,
	d: int,
	uent: QCircuit = None
) -> QCircuit:
	if not uent:
		uent = create_uent(n_qubits)
	circuit: QCircuit = create_rotations(n_qubits, 0)
	for depth in range(d):
		circuit += uent
		circuit += create_rotations(n_qubits, depth + 1)
	return circuit
