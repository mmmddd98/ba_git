import torch

def create_checkpoint(model):
    checkpoint = []
    for param in model.parameters():
        newparams = param.clone().detach().to(device='cuda')
        checkpoint.append(newparams)

    return checkpoint