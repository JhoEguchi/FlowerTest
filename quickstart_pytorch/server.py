from typing import List, Tuple

import flwr as fl
from flwr.common import Metrics


# Define metric aggregation function
def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]
    
    #print(accuracies)
    
    #for x in range(len(accuracies)):
	#    f = open("saida.txt", "w")
	#    f.write(accuracies[x])
	#    f.close()

    # Aggregate and return custom metric (weighted average)
    return {"accuracy": sum(accuracies) / sum(examples)}


# Define strategy
strategy = fl.server.strategy.FedAvg(
    fraction_fit=1.0,
    accept_failures = True,
    evaluate_metrics_aggregation_fn=weighted_average, 
    min_fit_clients=10,
    min_available_clients=10)

# Start Flower server
fl.server.start_server(
    server_address="[::]:8080",
    config={"num_rounds": 10},
    strategy=strategy,
)
