import torch
import torch.utils
import torch.utils.data
import torchvision.models as models
import torch.nn as nn
from torchvision import datasets, transforms
import torch.optim as optim

model = models.mobilenet_v2(pretrained=True)

for param in model.parameters():
    param.requires_grad = False
    
model.classifier[1] = nn.Linear(model.last_channel, 5)

train_transform = transforms.Compose([
    transforms.RandomRotation(20),
    transforms.RandomHorizontalFlip(),
    transforms.RandomResizedCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.465, 0.406], std=[0.229, 0.224, 0.225])
])

val_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.465, 0.406], std=[0.229, 0.224, 0.225])
])

train_data = datasets.ImageFolder("TRAINING_IMAGE_FOLDER", transform=train_transform)
val_data = datasets.ImageFolder("Validation_IMAGE_FOLDER", transform=val_transform)

train_loader = torch.utils.data.DataLoader(train_data, batch_size=32, shuffle=True)
val_loader = torch.utils.data.DataLoader(val_data, batch_size=32, shuffle=False)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=1e-4)

for epoch in range(10):
    model.train()
    for inputs, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}, Loss: {loss.item()}")
