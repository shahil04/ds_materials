import torch
import torchvision.models as models

# Load a pre-trained ResNet50 model
model = models.resnet50(pretrained=True)

# Print model architecture
# print(model)

# Freeze the model parameters
for param in model.parameters():
    param.requires_grad = False
    
# Modify the final layer for a new task
num_features = model.fc.in_features
model.fc = torch.nn.Linear(num_features, 10)

# print("Modified MOdel:\n", model)

# for name, param in model.named_parameters():
#     print(f"Layer: {name}, Required Grad: {param.requires_grad}")

for name, param in model.named_parameters():
    if "layer4" in name:
        param.requires_grad = True
