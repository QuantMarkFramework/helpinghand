from helpinghand.compute import compute, compute_many
from helpinghand.hardware_ansatz import create_hardware_ansatz
from helpinghand.gradient import get_max_from_result, get_max_from_VQE
from helpinghand.analyse import CircuitAnalytics, CircuitAnalyser
from helpinghand.tket import to_tket, from_tket

try:
	from helpinghand.psi4_helper import molecus_for_working_psi4_distances
except ModuleNotFoundError:
	pass

try:
	from helpinghand.pyscf_helper import pyscf_create_hamiltonians
except ModuleNotFoundError:
	pass
