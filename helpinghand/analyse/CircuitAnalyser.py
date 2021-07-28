from helpinghand.analyse.CircuitAnalytics import CircuitAnalytics
import typing
import tequila as tq
from tequila.circuit.compiler import Compiler


DEFAULT_COMPILER_ARGUMENTS = {
	"multitarget": True,
	"multicontrol": True,
	"trotterized": True,
	"generalized_rotation": True,
	"exponential_pauli": True,
	"controlled_exponential_pauli": True,
	"hadamard_power": True,
	"controlled_power": True,
	"power": True,
	"toffoli": True,
	"controlled_phase": False,
	"phase": True,
	"phase_to_z": False,
	"controlled_rotation": True,
	"swap": True,
	"cc_max": True,
	"ry_gate": False,
	"y_gate": False,
	"ch_gate": True
}


class CircuitAnalyser:
	"""Helper class to analyze circuits."""
	def __init__(
		self,
		compiler_arguments: typing.Dict[str, bool] = None,
		compiler: Compiler = None
	):
		if compiler_arguments is not None and compiler is not None:
			raise ValueError("Give compiler_arguments or compiler, not both.")
		if compiler is not None:
			self.compiler: Compiler = compiler
		elif compiler_arguments is not None:
			self.compiler: Compiler = Compiler(**compiler_arguments)
		else:
			self.compiler: Compiler = Compiler(**DEFAULT_COMPILER_ARGUMENTS)

	def __call__(self, circuit: tq.QCircuit) -> CircuitAnalytics:
		return CircuitAnalytics(circuit, self.compiler)

	def info(self, circuit: tq.QCircuit) -> None:
		"""Prints information about the circuit."""
		CircuitAnalytics(circuit, self.compiler).info()