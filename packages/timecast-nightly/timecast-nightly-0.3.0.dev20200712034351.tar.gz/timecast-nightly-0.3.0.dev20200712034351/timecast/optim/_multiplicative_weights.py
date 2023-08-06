"""timecast.optim._multiplicative_weights"""
import jax.numpy as jnp
from flax import struct
from flax.optim.base import OptimizerDef


@struct.dataclass
class _MultiplicativeWeightsHyperParams:
    """MultiplicativeWeights hyperparameters"""

    eta: jnp.ndarray


class MultiplicativeWeights(OptimizerDef):
    """Multiplicative weights"""

    def __init__(self, eta: float = None):
        """Constructor for the MultiplicativeWeights optimizer.
        Args:
          eta (float): rate used to update the parameters.
        """
        hyper_params = _MultiplicativeWeightsHyperParams(eta)
        super().__init__(hyper_params)

    def init_param_state(self, param):
        """Initialize parameter state"""
        return ()

    def apply_param_gradient(self, step, hyper_params, param, state, grad):
        """Apply per-parametmer gradients"""
        del step

        exp = param * jnp.exp(-1 * hyper_params.eta * grad)
        new_param = exp / exp.sum()
        return new_param, state
