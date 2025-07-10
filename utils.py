import torch
from torchvision import transforms
from PIL import Image

GESTURE_CLASSES = ['swipe_right', 'swipe_down', 'zoom_in', 'zoom_out', 'swipe_up', 'swipe_up_down']

def load_model(path):
    from torchvision import models
    model = models.resnet18(pretrained=False)
    model.fc = torch.nn.Linear(model.fc.in_features, len(GESTURE_CLASSES))
    model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))
    model.eval()
    return model

def predict_gesture(image_path, model):
    transform = transforms.Compose([
        transforms.Resize((150, 150)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], 
                             [0.229, 0.224, 0.225])
    ])
    img = Image.open(image_path).convert('RGB')
    input_tensor = transform(img).unsqueeze(0)  # add batch dimension
    output = model(input_tensor)
    _, predicted = torch.max(output, 1)
    return GESTURE_CLASSES[predicted.item()]
