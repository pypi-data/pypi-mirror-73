"""timecast.optim._projected_sgd"""
import jax
import jax.numpy as jnp
from flax import struct
from flax.optim.base import OptimizerDef


@struct.dataclass
class _ProjectedSGDHyperParams:
    """ProjectedSGD hyperparameters"""

    learning_rate: jnp.ndarray
    projection_threshold: float


class ProjectedSGD(OptimizerDef):
    """Gradient descent optimizer with projections."""

    def __init__(self, learning_rate: float = None, projection_threshold: float = None):
        """Constructor for the ProjectedSGD optimizer.
        Args:
          learning_rate (float): the step size used to update the parameters.
          projection_threshold (float): threshold for parameters (Frobenius
          norm for matrices, 2-norm for vectors)
        """
        projection_threshold = projection_threshold or float("inf")
        hyper_params = _ProjectedSGDHyperParams(learning_rate, projection_threshold)
        super().__init__(hyper_params)

    def init_param_state(self, param):
        """Initialize parameter state"""
        return ()

    def apply_param_gradient(self, step, hyper_params, param, state, grad):
        """Apply per-parametmer gradients"""
        del step
        assert hyper_params.learning_rate is not None, "no learning rate provided."
        new_param = param - hyper_params.learning_rate * grad
        norm = jnp.linalg.norm(new_param)
        new_param = jax.lax.cond(
            norm > hyper_params.projection_threshold,
            new_param,
            lambda x: hyper_params.projection_threshold / norm * x,
            new_param,
            lambda x: x,
        )
        return new_param, state
