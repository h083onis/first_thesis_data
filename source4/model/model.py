import torch
import torch.nn as nn
import torch.nn.init as init

class CNN(nn.Module):
    def __init__(self, n_output, n_hidden):
        super().__init__()
        self.relu = nn.ReLU(inplace=True)
        self.embedding = nn.Embedding(2001,128)
        self.conv1 = nn.Conv2d(1, 128, (3,128))
        self.maxpool1 = nn.MaxPool2d((1998,1))
        self.conv2 = nn.Conv2d(1, 128, (4,128))
        self.maxpool2 = nn.MaxPool2d((1997,1))
        self.conv3 = nn.Conv2d(1, 128, (5,128))
        self.maxpool3 = nn.MaxPool2d((1996,1))
        self.flatten = nn.Flatten()
        self.l1 = nn.Linear(384, n_output)
        self.dropout = nn.Dropout(0.5)

        self.features1 = nn.Sequential(
            self.conv1,
            self.relu,
            self.maxpool1,
        )

        self.features2 = nn.Sequential(
            self.conv2,
            self.relu,
            self.maxpool2,
        )

        self.features3 = nn.Sequential(
            self.conv3,
            self.relu,
            self.maxpool3,
        )


    def forward(self, x):
        x1 = self.embedding(x)
        # print(x1.shape)
        # print(x1)
        x1 = x1.unsqueeze(1)
        # print(x1.shape)
        x2_1 = self.features1(x1)
        x2_2 = self.features2(x1)
        x2_3 = self.features3(x1)
        # print(x2_1.shape,x2_2.shape,x2_3.shape)
        x3_combined = torch.cat((x2_1, x2_2, x2_3), dim=1)
        # print(x3_combined.shape)
        x4 = self.flatten(x3_combined)
        x5 = self.dropout(x4)
        x6 = self.l1(x5)
        return x6
