import torch.nn as nn
import numpy


class MLP(nn.Module):
    """Very basic multiple layer neural network"""

    def __init__(self, input_size, outputs):
        super(MLP, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, input_size * 2, bias=True),
            nn.ReLU(),
            nn.Linear(input_size * 2, outputs, bias=True),
            nn.Softmax(dim=1)
        )

    def forward(self, x):
        return self.model(x)



class LeNet(nn.Module):
    """
    `Paper <http://vision.stanford.edu/cs598_spring07/papers/Lecun98.pdf>`_.

    Attributes
    ----------
    input_size: (n, 32, 32)
        Supported input sizes

    References
    ----------
    .. [1] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner.
        "Gradient-based learning applied to document recognition."
        Proceedings of the IEEE, 86(11):2278-2324, November 1998.

    """
    def __init__(self, input_size, num_classes):
        super(LeNet, self).__init__()

        if not isinstance(num_classes, int):
            num_classes = numpy.product(num_classes)

        n_channels = input_size[0]
        self.conv1 = nn.Conv2d(n_channels, 20, 5, 1)
        self.pool1 = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(20, 50, 5, 1)
        self.pool2 = nn.MaxPool2d(2, 2)
        self.fc1   = nn.Linear(50 * 5 * 5, 500)
        self.fc2   = nn.Linear(500, num_classes)

        # this layer is ot part of the paper
        self.end   = nn.Softmax(dim=1)

    def forward(self, x):
        # For DQN, the value returned is the estimated reward
        # each action will give us
        out = nn.functional.relu(self.conv1(x))
        out = self.pool1(out)
        out = nn.functional.relu(self.conv2(out))
        out = self.pool2(out)
        out = out.view(out.size(0), -1)
        out = nn.functional.relu(self.fc1(out))
        return self.fc2(out)

    def action_probs(self, x):
        # Sometimes we want it normalized
        out = self.forward(x)
        return self.end(out)
