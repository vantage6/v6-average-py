import pandas as pd
from vantage6.common import info
from vantage6.algorithm.decorator.action import federated
from vantage6.algorithm.decorator.data import dataframe


@federated
@dataframe(1)
def partial_average(df1: pd.DataFrame, column_name: str) -> dict:
    """Compute local sum and row count for a single organization."""
    info(f"Extracting column {column_name}")
    numbers = df1[column_name]

    info("Computing partials")
    return {
        "sum": float(numbers.sum()),
        "count": len(numbers),
    }
