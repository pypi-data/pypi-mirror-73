# This project
from ....units import solarsystem
from ..util import from_equation
from .helpers import PotentialTestBase

class EquationBase(PotentialTestBase):
    def test_plot(self):
        # Skip for now because contour plotting assumes 3D
        pass

    def test_pickle(self):
        # Skip for now because these are not picklable
        pass

    def test_save_load(self):
        # Skip for now because these can't be written to YAML
        pass

class TestHarmonicOscillatorFromEquation(EquationBase):
    Potential = from_equation("1/2*k*x**2", vars="x", pars="k",
                              name='HarmonicOscillator',
                              hessian=True)
    potential = Potential(k=1.)
    w0 = [1.,0.]

    def test_derp(self):
        import numpy as np
        self.potential.gradient(np.random.random(size=(1,13)))

# class TestHarmonicOscillatorFromEquationUnits(EquationBase):
#     Potential = from_equation("1/2*k*x**2", vars="x", pars="k",
#                               name='HarmonicOscillator',
#                               hessian=True)
#     potential = Potential(k=1., units=solarsystem)
#     w0 = [1.,0.]

# class TestKeplerFromEquation(EquationBase):
#     Potential = from_equation("-G*M/sqrt(x**2+y**2+z**2)", vars=["x","y","z"],
#                               pars=["G","M"], name='Kepler',
#                               hessian=True)
#     potential = Potential(G=1., M=1., units=solarsystem)
#     w0 = [1.,0.,0.,0.,6.28,0.]
