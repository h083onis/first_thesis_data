import torch
import torch.nn as nn

class CNN(nn.Module):
  def __init__(self, n_output, n_hidden):
    super().__init__()
    self.relu = nn.ReLU(inplace=True)
    self.embedding = nn.Embedding(2000,128)
    self.conv1 = nn.Conv2d(1, 128, (3,128))
    self.maxpool1 = nn.MaxPool2d((1998,1))
    self.conv2 = nn.Conv2d(1, 128, (4,128))
    self.maxpool2 = nn.MaxPool2d((1997,1))
    self.conv3 = nn.Conv2d(1, 128, (5,128))
    self.maxpool3 = nn.MaxPool2d((1996,1))
    self.flatten = nn.Flatten()
    self.l1 = nn.Linear(384, n_hidden)
    self.l2 = nn.Linear(n_hidden, n_output)

    self.features1 = nn.Sequential(
        self.conv1,
        self.relu,
        self.maxpool1)
    
    self.features2 = nn.Sequential(
        self.conv2,
        self.relu,
        self.maxpool2)
    
    self.features3 = nn.Sequential(
        self.conv3,
        self.relu,
        self.maxpool3)
    
    self.classifier = nn.Sequential(
       self.l1,
       self.relu,
       self.l2)

  def forward(self, x):
    x1 = self.embedding(x)
    x1 = x1.unsqueeze(1)
    # print(x1.shape)
    x2_1 = self.features1(x1)
    x2_2 = self.features2(x1)
    x2_3 = self.features3(x1)
    # print(x2_1.shape,x2_2.shape,x2_3.shape)
    x3_1 = self.flatten(x2_1)
    x3_2 = self.flatten(x2_2)
    x3_3 = self.flatten(x2_3)
    # print(x3_1.shape,x3_2.shape,x3_3.shape)
    x3_combined = torch.cat((x3_1, x3_2, x3_3), dim=1)
    # print(x2_combined.shape)
    x4 = self.classifier(x3_combined)
    return x4   