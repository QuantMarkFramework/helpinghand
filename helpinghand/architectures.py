import typing
from pytket.routing import Architecture


def node_line(nodes: typing.List[int]) -> typing.List[typing.List[int]]:
	return [[nodes[i], nodes[i + 1]] for i in range(len(nodes) - 1)]


def ourense(qubits: int = None) -> Architecture:
	return Architecture([[0, 1], [1, 2], [1, 3], [3, 4]])


def yorktown(qubits: int = None) -> Architecture:
	return Architecture([[0, 1], [1, 2], [0, 2], [2, 3], [2, 4], [3, 4]])


def melbourne(qubits: int = None) -> Architecture:
	return Architecture([
		*[[i, i + 1] for i in range(6)],
		*[[i, i + 1] for i in range(7, 13)],
		*[[i + 1, 13 - i] for i in range(6)]
	])


def almaden(qubits: int = None) -> Architecture:
	return Architecture([
		*[[i, i + 1] for i in range(4)],
		*[[i, i + 1] for i in range(5, 9)],
		*[[i, i + 1] for i in range(10, 14)],
		*[[i, i + 1] for i in range(15, 19)],
		[1, 6], [3, 8], [5, 10], [7, 12], [9, 14], [11, 16], [13, 18]
	])


def johannesburg(qubits: int = None) -> Architecture:
	return Architecture([
		*[[i, i + 1] for i in range(4)],
		*[[i, i + 1] for i in range(5, 9)],
		*[[i, i + 1] for i in range(10, 14)],
		*[[i, i + 1] for i in range(15, 19)],
		[0, 5], [5, 10], [10, 15], [7, 12],
		[4, 9], [9, 14], [14, 19]
	])


def falcon(qubits: int = None) -> Architecture:
	"""Falcon r4 from IBM"""
	return Architecture([
		*node_line([0, 1, 4, 7, 10, 12, 15, 18, 21, 23, 24, 25, 22, 19, 16, 14, 11, 8, 5, 3, 2, 1]),
		[6, 7], [17, 18], [25, 26], [19, 20], [8, 9], [12, 13], [13, 14]
	])


def hummingbird(qubits: int = None) -> Architecture:
	"""Hummingbird r2 from IBM"""
	return Architecture([
		*[[i, i + 1] for i in range(9)],
		*[[i, i + 1] for i in range(13, 23)],
		*[[i, i + 1] for i in range(27, 37)],
		*[[i, i + 1] for i in range(41, 51)],
		*[[i, i + 1] for i in range(55, 64)],
		*node_line([0, 10, 13]),
		*node_line([4, 11, 17]),
		*node_line([8, 12, 21]),
		*node_line([15, 24, 29]),
		*node_line([19, 25, 33]),
		*node_line([23, 26, 37]),
		*node_line([27, 38, 41]),
		*node_line([31, 39, 45]),
		*node_line([35, 40, 49]),
		*node_line([43, 52, 56]),
		*node_line([47, 53, 60]),
		*node_line([51, 54, 64]),
	])


def sycamore(qubit: int = None) -> Architecture:
	"""googles sycamore processof if all qubits would work"""
	return Architecture(node_line([
		5, 6, 4, 7, 3, 8, 2, 9, 1, 10, 0, 11,
		12, 10, 13, 9, 14, 8, 15, 7, 16, 6, 17,
		18, 16, 19, 15, 20, 14, 21, 13, 22, 12, 23,
		24, 22, 25, 21, 26, 20, 27, 19, 28, 18, 29,
		30, 28, 31, 27, 32, 26, 33, 25, 34, 24, 35,
		36, 34, 37, 33, 38, 32, 39, 31, 40, 30, 41,
		42, 40, 43, 39, 44, 38, 45, 37, 46, 36, 47,
		58, 46, 49, 45, 50, 44, 51, 43, 52, 42, 53
	]))


def aspen9(qubits: int = None) -> Architecture:
	return Architecture([
		*[[i, i + 1] for i in range(7)], [0, 7],
		*[[i, i + 1] for i in range(10, 17)], [10, 17],
		*[[i, i + 1] for i in range(20, 27)], [20, 27],
		*[[i, i + 1] for i in range(30, 37)], [30, 37],
		[2, 15], [1, 16], [12, 25], [11, 26], [22, 35], [21, 36]
	])


def line(qubits: int) -> Architecture:
	return Architecture([[i, i + 1] for i in range(qubits - 1)])


ARCHITECTURE_CREATORS = {
	"ourense": (ourense, False),
	"valencia": (ourense, False),
	"vigo": (ourense, False),
	"yorktown": (yorktown, False),
	"melbourne": (melbourne, False),
	"almaden": (almaden, False),
	"boeblingen": (almaden, False),
	"singapore": (almaden, False),
	"johannesburg": (johannesburg, False),
	"poughkeepsie": (johannesburg, False),
	"falcon": (falcon, False),
	"hummingbird": (hummingbird, False),
	"sycamore": (sycamore, False),
	"aspen9": (aspen9, False),
	"line": (line, False)
}


def select_architecture(name: str, qubits: int = None) -> Architecture:
	creator, scalable = ARCHITECTURE_CREATORS.get(name.lower())
	if scalable and not qubits:
		raise ValueError(
			f"Architecture '{name}' needs the 'qubits' parameter to be created."
		)
	if not creator:
		raise ValueError(
			f"Architecture '{name}' not found. Select from {list(ARCHITECTURE_CREATORS.keys())}."
		)
	arc = creator(qubits)
	if qubits and len(arc.nodes) < qubits:
		raise ValueError(F"Selected architecture '{name}' does not support {qubits} qubits.")
	return arc
