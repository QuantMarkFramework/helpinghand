import tequila as tq
from tequila.circuit import gates
import helpinghand.convenience_gates as congates
from tequila.objective.objective import FixedVariable, Objective, Variable
import numpy as np

HAS_PYTKET = True
try:
	from pytket import Circuit, OpType
	from pytket.circuit import fresh_symbol
except ImportError:
	HAS_PYTKET = False

TQ_TO_TKET = {
	"I": (lambda c: lambda _: c),
	"X": (lambda c: c.X, lambda c: c.CX, lambda c: c.CCX),
	"Y": (lambda c: c.Y, lambda c: c.CY),
	"Z": (lambda c: c.Z, lambda c: c.CZ),
	"H": (lambda c: c.H, lambda c: c.CH),
	"Rx": (lambda c: c.Rx, lambda c: c.CRx),
	"Ry": (lambda c: c.Ry, lambda c: c.CRy),
	"Rz": (lambda c: c.Rz, lambda c: c.CRz),
	"SWAP": (lambda c: c.SWAP, lambda c: c.CSWAP),
}

TKET_TO_TQ = {
	OpType.X: gates.X,
	OpType.CX: gates.CX,
	OpType.CCX: gates.Toffoli,
	OpType.Y: gates.Y,
	OpType.CY: gates.CY,
	OpType.Z: gates.Z,
	OpType.CZ: gates.CZ,
	OpType.H: gates.H,
	OpType.CH: gates.H,
	OpType.Rx: gates.Rx,
	OpType.CRx: gates.CRx,
	OpType.Ry: gates.Ry,
	OpType.CRy: gates.CRy,
	OpType.Rz: gates.Rz,
	OpType.CRz: gates.CRz,
	OpType.SWAP: gates.SWAP,
	OpType.CSWAP: gates.SWAP,
	OpType.V: congates.V,
	OpType.Vdg: congates.Vdg,
	OpType.CV: congates.V,
	OpType.CVdg: congates.Vdg,
}


class ConvertToTKETError(Exception):
	pass


class ConvertFromTKETError(Exception):
	pass


def to_tket(circuit: tq.QCircuit) -> Circuit:
	if not HAS_PYTKET:
		raise ModuleNotFoundError("Needed module pytket not found.")
	circ = Circuit(circuit.n_qubits)
	variable_map = {}

	for gate in circuit.gates:
		gate_function = TQ_TO_TKET.get(gate.name, None)
		if not len(gate.target) == 1:
			raise ConvertToTKETError("Only converting single target gates is supported.")
		if not gate_function:
			raise ConvertToTKETError(f'Converting gate {gate.name} is not supported.')
		n_control = len(gate.control)
		if n_control > len(gate_function) - 1:
			raise ConvertToTKETError(
				f'Converting gate {gate.name} with {n_control} controls is not supported.'
			)
		if gate.is_parametrized():
			variable = gate.parameter
			if isinstance(variable, FixedVariable):
				parameter = float(variable) / np.pi
			elif isinstance(variable, Variable):
				try:
					parameter = variable_map[variable.name]
				except KeyError:
					parameter = fresh_symbol(variable.name)
					variable_map[variable.name] = parameter
			elif isinstance(variable, Objective):  # CircuitAnalyser + make_upccgsd_ansatz ?
				variable = variable.extract_variables()[0]
				try:
					parameter = variable_map[str(variable.name)]
				except KeyError:
					parameter = fresh_symbol(str(variable.name))
					variable_map[str(variable.name)] = parameter
			else:
				raise ConvertToTKETError("I have no idea anymore about what is going on...")
			gate_function[n_control](circ)(parameter, *gate.control, *gate.target)
		else:
			gate_function[n_control](circ)(*gate.control, *gate.target)
	return circ


def from_tket(circuit: Circuit) -> tq.QCircuit:
	if not HAS_PYTKET:
		raise ModuleNotFoundError("Needed module pytket not found.")
	circ = tq.QCircuit()

	for gate in circuit:
		gate_function = TKET_TO_TQ.get(gate.op.type, None)
		if not gate_function:
			raise ConvertFromTKETError(f'Converting gate {gate.op.get_name()} is not supported.')
		parameters = gate.op.params
		if len(parameters) > 1:
			raise ConvertFromTKETError(
				"Only converting single or no parameter gates is supported."
			)
		arguments = [arg.index[0] for arg in gate.args]
		if parameters and isinstance(parameters[0], float):
			q_gate = gate_function(parameters[0] * np.pi, target=arguments[-1], control=arguments[:-1])
		elif parameters:
			q_gate = gate_function(parameters[0].name, target=arguments[-1], control=arguments[:-1])
		else:
			q_gate = gate_function(target=arguments[-1], control=arguments[:-1])
		circ += q_gate
	return circ
