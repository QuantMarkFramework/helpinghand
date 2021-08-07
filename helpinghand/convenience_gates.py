import tequila as tq
import numpy as np
import typing


def V(target: typing.Union[list, int], control: typing.Union[list, int] = None) -> tq.QCircuit:
	return tq.gates.Rx(target=target, control=control, angle=0.5 * np.pi)


def Vdg(target: typing.Union[list, int], control: typing.Union[list, int] = None) -> tq.QCircuit:
	return tq.gates.Rx(target=target, control=control, angle=0.5 * np.pi).dagger()
