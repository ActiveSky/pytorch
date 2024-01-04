import torch
from PIL import Image
from torchvision import transforms

def predict_digit(image_path, model):
    # 1.定义转换
    transform = transforms.Compose([
        transforms.Resize((28, 28)), # 调整图片大小
        transforms.ToTensor(), # 将PIL图片转换为Tensor
        transforms.Normalize((0.5,), (0.5,)) # 标准化
    ])

    # 2.打开图片并应用转换
    image = Image.open(image_path).convert('L') # 转换为灰度图
    image = transform(image)

    # 添加一个批次维度
    image = image.unsqueeze(0)
    # print image shape
    print("shape of image:",image.shape)

    # 将模型设置为评估模式
    model.eval()

    # predict result and probability
    with torch.no_grad():
        output = model(image)
        # 1.get the probability of the every class
        prob = torch.nn.functional.softmax(output, dim=1)
        # 2.print the probability which Keeps two decimal places of the every class use a dict 
        print("Probability:", {i: round(float(prob[0][i]), 2) for i in range(10)})
        # 3.get the predict result which has the highest probability
        pred = torch.argmax(prob, dim=1, keepdim=True)
        print("Predicted result:", pred.item())
        print("Probability:", prob[0][pred.item()].item())

    
    