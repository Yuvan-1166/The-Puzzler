import torch
import torch.nn.functional as F


def board_to_tensor(board):
    """
    Converts a 4x4 integer grid into a (1, 16, 4, 4) one-hot float tensor.
    """
    board_tensor = torch.tensor(board, dtype=torch.float32)
    indices = torch.zeros_like(board_tensor, dtype=torch.long)

    mask = board_tensor > 0
    indices[mask] = torch.log2(board_tensor[mask]).long()

    one_hot = F.one_hot(indices, num_classes=16).float()
    tensor_3d = one_hot.permute(2, 0, 1)
    final_tensor = tensor_3d.unsqueeze(0)
    return final_tensor
