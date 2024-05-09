import torch
from torch import nn
from torchsummary import summary

'''ResNet18网络搭建'''

class Residual(nn.Module):
    def __init__(self, input_channels, out_channels, use_1conv=False, strides=1):
        super(Residual, self).__init__()
        self.relu = nn.ReLU()
        self.conv1 = nn.Conv2d(in_channels=input_channels,out_channels=out_channels,kernel_size=3,padding=1,stride=strides)
        self.conv2 = nn.Conv2d(in_channels=out_channels,out_channels=out_channels,kernel_size=3,padding=1)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.bn2 = nn.BatchNorm2d(out_channels)

        if use_1conv:
            self.conv3 = nn.Conv2d(in_channels=input_channels,out_channels=out_channels,kernel_size=1,stride=strides)
        else:
            self.conv3 = None

    def forward(self,x):
        y = self.relu(self.bn1(self.conv1(x)))
        y = self.bn2(self.conv2(y))
        if self.conv3:
            x = self.conv3(x)
        # 残差直接将数据加到上面去
        y = self.relu(y+x)
        return y


class ResNet18(nn.Module):
    def __init__(self, Residual):
        super(ResNet18, self).__init__() # 这一步骤是确保ResNet18继承nn.Module的全部功能，并执行初始化

        self.b1 = nn.Sequential(
            nn.Conv2d(in_channels=3,out_channels=64,kernel_size=7,stride=2,padding=3),
            nn.ReLU(),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(kernel_size=3,stride=2,padding=1),
        )

        self.b2 = nn.Sequential(
            Residual(64,64,use_1conv=False,strides=1),
            Residual(64,64,use_1conv=False,strides=1)

        )

        self.b3 = nn.Sequential(
            Residual(64,128,use_1conv=True,strides=2),
            Residual(128, 128, use_1conv=False, strides=1)
        )

        self.b4 = nn.Sequential(
            Residual(128, 256, use_1conv=True, strides=2),
            Residual(256, 256, use_1conv=False, strides=1)
        )

        self.b5= nn.Sequential(
            Residual(256, 512, use_1conv=True, strides=2),
            Residual(512, 512, use_1conv=False, strides=1)
        )

        self.b6 = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)), # 全局平均池化
            nn.Flatten(),
            nn.Linear(512,10)
        )

    def forward(self,x):
        x = self.b1(x)
        x = self.b2(x)
        x = self.b3(x)
        x = self.b4(x)
        x = self.b5(x)
        x = self.b6(x)
        return x


if __name__ == '__main__':
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = ResNet18(Residual).to(device)
    print(summary(model,(1,512,512)))
    # 保存模型
    torch.save(model,'ResNet18_model_information.pth')