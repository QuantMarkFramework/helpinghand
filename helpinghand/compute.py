import typing

import tequila as tq
from tequila import QCircuit, QubitHamiltonian
from tequila.objective.objective import (
	Variable,
	VectorObjective,
	assign_variable
)
from tequila.optimizers.optimizer_base import Optimizer, OptimizerResults


class DifferentSizeInputListsError(Exception):
	"""Raised when lists that are give as parameters have different sizes."""
	pass


def compute(
	hamiltonian: QubitHamiltonian,
	circuit: QCircuit,
	optimizer: Optimizer,
	initial_values: typing.Union[int, typing.Dict[Variable, float]] = None
) -> OptimizerResults:
	objective: VectorObjective = tq.ExpectationValue(H=hamiltonian, U=circuit)
	if isinstance(initial_values, int) or isinstance(initial_values, float):
		initial_values = {assign_variable(k): initial_values for k in objective.extract_variables()}
	else:
		initial_values = {assign_variable(k): float(v) for k, v in initial_values.items()}
	result: OptimizerResults = optimizer(
		objective=objective,
		initial_values=initial_values
	)
	return result


def compute_many(
	hamiltonians: typing.List[QubitHamiltonian],
	circuits: typing.Union[typing.List[QCircuit], QCircuit],
	initial_values: typing.Union[
		int,
		typing.Dict[Variable, float],
		typing.List[typing.Dict[Variable, float]]
	],
	optimizer: Optimizer,
	mark: bool = True
) -> typing.List[OptimizerResults]:
	hamiltonian_count: int = len(hamiltonians)
	if not isinstance(circuits, list):
		circuits = [circuits for _ in range(hamiltonian_count)]
	if not isinstance(initial_values, list):
		initial_values = [initial_values for _ in range(hamiltonian_count)]

	if not (hamiltonian_count == len(circuits) and len(circuits) == len(initial_values)):
		raise DifferentSizeInputListsError()

	results: typing.List[OptimizerResults] = []
	for i in range(hamiltonian_count):
		results.append(compute(
			hamiltonian=hamiltonians[i],
			circuit=circuits[i],
			optimizer=optimizer,
			initial_values=initial_values[i]
		))
		if mark:
			print('.', end='')
	if mark:
		print()
	return results
