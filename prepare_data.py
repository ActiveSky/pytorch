# import library

from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torchvision
from torch.utils.tensorboard import SummaryWriter

# # set the writer for tensorboardX object
# writer = SummaryWriter('./pytorch_tb')

# set the super parameters
batch_size_train = 32
batch_size_test = 1000


def prepare_data():
    """
    Prepare the MNIST dataset for training and testing.

    Returns:
    train_loader (DataLoader): DataLoader object for training data.
    test_loader (DataLoader): DataLoader object for testing data.
    """
    # 1.data preparation
    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,)),
        ]
    )
    # 2.load train and test data
    trainset = datasets.MNIST(
        "./data/MNIST_data/", download=True, train=True, transform=transform
    )
    testset = datasets.MNIST(
        "./data/MNIST_data/", download=True, train=False, transform=transform
    )

    # 3.create data loader
    train_loader = DataLoader(trainset, batch_size=batch_size_train, shuffle=True)
    test_loader = DataLoader(testset, batch_size=batch_size_test, shuffle=False)

    return train_loader, test_loader


if __name__ == "__main__":
    train_loader, test_loader = prepare_data()
    images, labels = next(iter(train_loader))

    # use tensorboardX to visualize the data
    writer=SummaryWriter('./pytorch_tb')
    writer.add_image("images", torchvision.utils.make_grid(images))
    
