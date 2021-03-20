import torch

a = torch.rand([1], requires_grad=True)

b=torch.exp(a)
b.backward(retain_graph=True)
print(a.grad)
c=a.grad.clone().detach()
print(c)
#a.grad.data.zero_()

#d=torch.exp()
print(a.grad)