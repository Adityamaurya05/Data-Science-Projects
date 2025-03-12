import torch
import torch.nn as nn
import torchvision.models as models
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

num_classes = 8
class_names = ['Bharatanatyam', 'Kathak', 'Kathakali', 'Kuchipudi', 'Manipuri', 'Mohiniyattam', 'Odissi', 'Sattriya']

model = models.resnet34(weights='DEFAULT')
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, num_classes)

state_dict = torch.load('./model.pth', map_location=torch.device('cpu'), weights_only=True)
model.load_state_dict(state_dict, strict=False)

model.eval()

data_transforms = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

test_dir = './data'
test_dataset = datasets.ImageFolder(test_dir, transform=data_transforms)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)


def test_model(model, test_loader):
    correct = 0
    total = 0

    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs = inputs.to(torch.device('cpu'))
            labels = labels.to(torch.device('cpu'))

            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)

            total += labels.size(0)
            correct += (preds == labels).sum().item()

    print(f'Accuracy of the model on the test images: {100 * correct / total:.2f}%')

test_model(model, test_loader)
