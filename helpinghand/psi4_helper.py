import typing
from collections.abc import Callable

from tequila import QubitHamiltonian
from tequila.quantumchemistry.psi4_interface import QuantumChemistryPsi4


def molecus_for_working_psi4_distances(
	molecule_creator: Callable[[float], QuantumChemistryPsi4],
	distances: typing.List[float]
) -> typing.Tuple[
	typing.List[QubitHamiltonian],
	typing.List[float],
	typing.List[float]
]:
	"""
	Returns (hamiltonians, readl_distances, fci_energies)
	"""
	hamiltonians: typing.List[QubitHamiltonian] = []
	real_distances: typing.List[float] = []
	fci_energies: typing.List[float] = []
	for distance in distances:
		try:
			molecule: QuantumChemistryPsi4 = molecule_creator(distance)
			fci_energies.append(molecule.compute_energy("fci"))
			real_distances.append(distance)
			hamiltonians.append(molecule.make_hamiltonian())
		except SystemError:
			print(f'Failed at distance {distance}')
			approximated: bool = False
			i = 1
			while not approximated and i < 11:
				new_R = distance - 0.001 * i
				try:
					molecule: QuantumChemistryPsi4 = molecule_creator(new_R)
					fci_energies.append(molecule.compute_energy("fci"))
					real_distances.append(distance)
					hamiltonians.append(molecule.make_hamiltonian())
					approximated = True
				except SystemError:
					print(f'Failed at R={new_R}')
					i += 1
			if not approximated:
				print(f'Gave up on distance {distance} :(')
	return (hamiltonians, real_distances, fci_energies)
