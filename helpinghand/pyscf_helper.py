import typing

from tequila import QubitHamiltonian
from tequila.quantumchemistry.pyscf_interface import QuantumChemistryPySCF


def pyscf_create_hamiltonians(
	molecule_creator: typing.Callable[[float], QuantumChemistryPySCF],
	distances: typing.List[float]
) -> typing.Tuple[
	typing.List[QubitHamiltonian],
	typing.List[float],
	typing.List[float]
]:
	"""Returns (hamiltonians, distances, fci_energies)"""
	hamiltonians: typing.List[QubitHamiltonian] = []
	fci_energies: typing.List[float] = []
	for distance in distances:
		molecule: QuantumChemistryPySCF = molecule_creator(distance)
		hamiltonians.append(molecule.make_hamiltonian())
		fci_energies.append(molecule.compute_energy('fci'))
	return (hamiltonians, distances, fci_energies)
