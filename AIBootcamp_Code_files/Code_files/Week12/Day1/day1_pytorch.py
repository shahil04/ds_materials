import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt

# Define queries, keys and values
queries = torch.tensor([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])
keys = torch.tensor([[1.0, 0.0, 1.0], [1.0, 1.0, 0.0], [0.0, 1.0, 1.0]])
values = torch.tensor([[10.0, 0.0], [0.0, 10.0], [5.0, 5.0]])

# Compute attention scores
scores = torch.matmul(queries, keys.T)

# Apply softmax to mormalize scores
attention_weights = F.softmax(scores, dim=-1)

# Compute weighted sum of values
context = torch.matmul(attention_weights, values)

print("Attention Weights: \n", attention_weights)
print("Context Vector:\n", context)

# Visualize attention weights
plt.matshow(attention_weights)
plt.colorbar()
plt.title("Attention Weights")
plt.show()