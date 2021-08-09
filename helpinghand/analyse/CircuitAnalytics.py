import typing
import tequila as tq
from tequila.circuit.compiler import Compiler
from tequila.circuit._gates_impl import QGateImpl
from helpinghand.tket import from_tket, to_tket

HAS_PYTKET = True
try:
	from pytket.routing import Architecture
	from pytket.passes import DefaultMappingPass, DecomposeSwapsToCXs
	from pytket.predicates import CompilationUnit
except ImportError:
	HAS_PYTKET = False


class CircuitAnalytics:
	"""Helper for inspecting circuit analytics"""
	def __init__(
		self,
		circuit: tq.QCircuit,
		compiler: Compiler,
		architecture: Architecture = None
	):
		self.abstract_circuit: tq.QCircuit = circuit

		if architecture:
			if not HAS_PYTKET:
				raise ModuleNotFoundError(
					"Pytket needs to be installed to use architecture when analysing circuits."
				)
			tket_circuit = to_tket(compiler(circuit))
			mapper = DefaultMappingPass(architecture)
			decomposer = DecomposeSwapsToCXs(architecture)
			cu = CompilationUnit(tket_circuit)
			mapper.apply(cu)
			decomposer.apply(cu)
			self.circuit: tq.QCircuit = from_tket(cu.circuit)
		else:
			self.circuit: tq.QCircuit = compiler(circuit)

		self.qubit_count: int = self.circuit.n_qubits
		self.gate_depth: int = self.circuit.depth
		self.gate_count: int = len(self.circuit.gates)
		self.parameter_count: int = len(
			list(self.circuit.make_parameter_map().keys())
		)

		self.gate_counts: typing.Dict[str, int] = {}
		self.gate_qubit_counts: typing.Dict[int, int] = {}
		gate: QGateImpl
		for gate in self.circuit.gates:
			targets: int = len(gate.target)
			controls: int = len(gate.control)
			qubits: int = targets + controls
			name: str = f'{"C" * controls}{gate.name} ({qubits})'

			if name in self.gate_counts:
				self.gate_counts[name] += 1
			else:
				self.gate_counts[name] = 1

			if qubits in self.gate_qubit_counts:
				self.gate_qubit_counts[qubits] += 1
			else:
				self.gate_qubit_counts[qubits] = 1

	def __str__(self):
		gate_qubit_counts: typing.List[str] = []
		for qubits, count in self.gate_qubit_counts.items():
			gate_qubit_counts.append(
				f'Number of {qubits} Qubit Gates: {count}\n'
			)
		return (
			f'Qubit Count:             {self.qubit_count}\n'
			f'Gate Depth:              {self.gate_depth}\n'
			f'Gate Count:              {self.gate_count}\n'
			f'Parameter Count:         {self.parameter_count}\n'
			f'{"".join(gate_qubit_counts)}'
		)

	def info(self) -> None:
		"""Prints information about the circuit."""
		print("========== CIRCUIT INFO ==========")
		print(self)
		print("Gate Counts:")
		for gate, count in self.gate_counts.items():
			print(f'{gate}: {count}')
		print()
