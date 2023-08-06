"""timecast.optim

Todo:
    * Document available optimizers
"""
import flax
from flax.optim import Adagrad
from flax.optim import Adam
from flax.optim import GradientDescent
from flax.optim import LAMB
from flax.optim import LARS
from flax.optim import Momentum
from flax.optim import RMSProp

from timecast.optim._multiplicative_weights import MultiplicativeWeights
from timecast.optim._projected_sgd import ProjectedSGD


@flax.struct.dataclass
class _DummyGradHyperParams:
    """DummyGrad hyperparameters"""

    add: float


class DummyGrad(flax.optim.OptimizerDef):
    """Dummy optimizer for testing"""

    def __init__(self, add: float = 0.0):
        """Initialize hyperparameters"""
        super().__init__(_DummyGradHyperParams(add))

    def init_param_state(self, param):
        """Initialize parameter state"""
        return {}

    def apply_param_gradient(self, step, hyper_params, param, state, grad):
        """Apply per-parametmer gradients"""
        new_param = param + hyper_params.add
        return new_param, state


__all__ = [
    "Adagrad",
    "Adam",
    "GradientDescent",
    "Momentum",
    "MultiplicativeWeights",
    "LAMB",
    "LARS",
    "RMSProp",
    "ProjectedSGD",
]
