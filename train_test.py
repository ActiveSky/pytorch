import torch
from torch import nn
import torch.optim as optim
from prepare_data import prepare_data
from torch.utils.tensorboard import SummaryWriter

logger = SummaryWriter("./pytorch_tb/train_test")
# super parameters
n_epochs = 5
learning_rate = 0.01
momentum = 0.5
log_interval = 10


def net_train(net: nn.Module, trainloader: torch.utils.data.DataLoader):
    """
    Train the neural network model.
    """
    # set the optimizer and loss function

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(net.parameters(), lr=learning_rate)

    print("Start training...")
    for epoch in range(n_epochs):  # loop over the dataset multiple times
        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            
            inputs, labels = data
            # 1.gradient to zero
            optimizer.zero_grad()  # zero the parameter gradients
            # 2.input data
            outputs = net(inputs)  # forward
            # 3.calculate loss
            loss = criterion(outputs, labels)  # calculate the loss
            # 4.backpropagation
            loss.backward()  # backpropagation
            # 5.update parameters
            optimizer.step()  # update parameters

            # print statistics
            running_loss += loss.item()
            if i % 100 == 99:  # print every 2000 mini-batches
                print("[%d, %5d] loss: %.3f" % (epoch + 1, i + 1, running_loss / 2000))
                logger.add_scalar('training loss', running_loss / 100, epoch * len(trainloader) + i)
                logger.add_scalar('training accuracy', accuracy, epoch * len(trainloader) + i)
                running_loss = 0.0
    print("Finished Training")


def net_test(net: nn.Module, testloader: torch.utils.data.DataLoader):
    print("Start testing...")
    correct = 0
    total = 0
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        print(
            "Accuracy of the network on the test images: %d %%"
            % (100 * correct / total)
        )
    print("Finished Testing")
