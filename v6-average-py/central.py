from vantage6.common import info
from vantage6.algorithm.client import AlgorithmClient
from vantage6.algorithm.decorator.algorithm_client import algorithm_client
from vantage6.algorithm.decorator.action import central


@central
@algorithm_client
def central_average(client: AlgorithmClient, column_name: str) -> dict:
    """Combine partials to a global average.

    Collect participating organizations, request partial sum/count from each,
    wait for results, then aggregate into a global average.
    """
    info("Collecting participating organizations")
    organizations = client.organization.list()
    ids = [organization.get("id") for organization in organizations]

    info("Requesting partial computation")
    task = client.task.create(
        method="partial_average",
        arguments={"column_name": column_name},
        organizations=ids,
        name="partial-average",
        description="Local sum and count per organization",
    )

    info("Waiting for results")
    results = client.wait_for_results(task_id=task.get("id"))
    info("Partial results are in!")

    info("Computing global average")
    global_sum = sum(output["sum"] for output in results)
    global_count = sum(output["count"] for output in results)

    return {"average": global_sum / global_count}
