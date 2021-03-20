import torch

def computedistance(checkpoint, model):
    distance = 0
    for checkpoint_param, param in zip(checkpoint, model.parameters()):
        difference = torch.add(-param, checkpoint_param)
        distance += torch.sum(torch.mul(difference, difference))
        
    return distance