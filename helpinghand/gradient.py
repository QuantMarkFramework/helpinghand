import typing
import tequila as tq
from tequila import QCircuit
from tequila.hamiltonian.qubit_hamiltonian import QubitHamiltonian
from tequila.objective.objective import VectorObjective
from tequila.optimizers.optimizer_base import Optimizer, OptimizerResults
from tequila.quantumchemistry import QuantumChemistryBase
from tequila.objective.objective import Variable, assign_variable


def get_max_from_result(result: OptimizerResults) -> typing.List[float]:
	return [abs(max(gradient.values(), key=abs)) for gradient in result.history.gradients]


def get_max_from_VQE(
	molecule: QuantumChemistryBase,
	circuit_creator: typing.Callable[[QuantumChemistryBase], QCircuit],
	optimizer: Optimizer,
	initial_values: typing.Union[int, typing.Dict[Variable, float]] = None
) -> typing.Tuple[typing.List[float], int, float]:
	H: QubitHamiltonian = molecule.make_hamiltonian()
	U: QCircuit = circuit_creator(molecule)
	E: VectorObjective = tq.ExpectationValue(H=H, U=U)

	if isinstance(initial_values, int) or isinstance(initial_values, float):
		initial_values = {assign_variable(k): initial_values for k in E.extract_variables()}
	else:
		initial_values = {assign_variable(k): float(v) for k, v in initial_values.items()}
	result: OptimizerResults = optimizer(
		objective=E,
		initial_values=initial_values
	)

	gradients: typing.List[float] = get_max_from_result(result=result)
	qubits: int = U.n_qubits
	energy: float = result.energy

	return (gradients, qubits, energy)
