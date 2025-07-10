import torch
from torchvision import transforms, models
from PIL import Image

def load_model(path):
    model = models.resnet18(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, 6)  # 6 classes
    model.load_state_dict(torch.load(path, map_location='cpu'))
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((150, 150)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])

    class_names = ['swipe_right', 'swipe_left', 'swipe_up', 'swipe_down', 'zoom_in', 'zoom_out']
    return model, transform, class_names

def predict_image(model, image, transform, class_names):
    tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(tensor)
        _, predicted = outputs.max(1)
        return class_names[predicted.item()]
