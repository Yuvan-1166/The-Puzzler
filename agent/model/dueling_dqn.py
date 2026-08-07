import torch
import torch.nn as nn
import torch.nn.functional as F


class DuelingDQN(nn.Module):
    def __init__(self):
        super(DuelingDQN, self).__init__()

        # Conv Layers
        self.conv1 = nn.Conv2d(in_channels=16, out_channels=128, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, padding=1)

        # Flattened Size 256 * 4 * 4

        flattend_size = 256*4*4

        # Value Stream
        self.val_fc = nn.Linear(flattend_size, 512)
        self.val_out = nn.Linear(512, 1)

        # Advantage Stream
        self.adv_fc = nn.Linear(flattend_size, 512)
        self.adv_out = nn.Linear(512, 4)

    def forward(self, x):
        # Conv Layers

        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))

        x = x.flatten(1)

        # Value Stream
        val = F.relu(self.val_fc(x))
        val = self.val_out(val)

        # Advantage Stream
        adv = F.relu(self.adv_fc(x))
        adv = self.adv_out(adv)

        q_values = val + (adv - adv.mean(dim=1, keepdim=True))

        return q_values
