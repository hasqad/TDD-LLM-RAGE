"""
pass@k metric — unbiased estimator from the HumanEval paper.

Formula:
    pass@k = 1 - C(n - c, k) / C(n, k)

Where:
    n = total number of samples generated
    c = number of samples that passed all tests
    k = number of samples to pick (1 or 5)

Reference:
    Chen et al., "Evaluating Large Language Models Trained on Code", 2021
    https://arxiv.org/abs/2107.03374
"""

import math
from dataclasses import dataclass


@dataclass
class PassAtKResult:
    n: int              # total samples
    c: int              # samples that passed
    pass_at_1: float
    pass_at_5: float


def _comb(n: int, k: int) -> float:
    """Binomial coefficient C(n, k). Returns 0 if k > n."""
    if k > n:
        return 0.0
    return float(math.comb(n, k))


def pass_at_k(n: int, c: int, k: int) -> float:
    """
    Compute the unbiased pass@k estimate.

    Args:
        n: total samples generated
        c: samples that passed
        k: k in pass@k

    Returns:
        Float in [0, 1]
    """
    if n == 0:
        return 0.0
    if c == n:
        return 1.0
    if k > n:
        # If we ask for more samples than we generated,
        # fall back to c/n as a conservative estimate
        return c / n

    numerator = _comb(n - c, k)
    denominator = _comb(n, k)

    if denominator == 0:
        return 0.0

    return 1.0 - (numerator / denominator)


def compute_pass_at_k(passed_flags: list[bool]) -> PassAtKResult:
    """
    Given a list of booleans (True = sample passed, False = failed),
    compute pass@1 and pass@5.

    Args:
        passed_flags: list of bool, one per sample

    Returns:
        PassAtKResult with pass_at_1 and pass_at_5
    """
    n = len(passed_flags)
    c = sum(passed_flags)

    return PassAtKResult(
        n=n,
        c=c,
        pass_at_1=round(pass_at_k(n, c, 1), 4),
        pass_at_5=round(pass_at_k(n, c, 5), 4),
    )
