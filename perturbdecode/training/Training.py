from perturbdecode.utils.Utils import *
from perturbdecode.utils.libraries import *


def train_model_CVAE(trainloader, model, optimizer, loss_fn, single_batch=False):
    
    """
    Method for training model (updating model params) based on given criterion.
    
    testloader : DataLoader
        Data for the evaluation.
        
    model : PyTorch model
        Model to be evaluated.
        
    optimizer: PyTorch optimizer
        Optimizer that will be used during training.
        
    loss_fn : Function
        Loss function that will be used for optimization.
    
    """
    
    
    model.train()

    total_loss = 0
    total_samples = 0

    for sample in trainloader:
        model.zero_grad()
        input = sample['y'].cuda() if next(model.parameters()).is_cuda else sample['y']
        condition = sample['X'].cuda() if next(model.parameters()).is_cuda else sample['X']

        output = model(input, condition)
        loss, BCE, KLD = loss_fn(*output)
        batch_size = len(input)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()*batch_size
        total_samples += batch_size

        if single_batch:
            break

    return {'train_loss': total_loss / total_samples, "BCE": BCE, "KLD":KLD}



def evaluate_model_CVAE(testloader, model, loss_fn, single_batch=False):
    """
    Method for evaluating model based on given criterion
    
    testloader : DataLoader
        Data for the evaluation.
        
    model : PyTorch model
        Model to be evaluated.
        
    
    loss_fn : Function
        Loss function that will be used for optimization.
    
    """
    
    model.eval()

    total_loss = 0
    total_samples = 0

    for sample in testloader:
        with torch.no_grad():
            input = sample['y'].cuda() if next(model.parameters()).is_cuda else sample['y']
            condition = sample['X'].cuda() if next(model.parameters()).is_cuda else sample['X']

            output = model(input, condition)
            loss, BCE, KLD = loss_fn(*output)
            batch_size = len(input)

        total_loss += loss.item()*batch_size
        total_samples += batch_size

        if single_batch:
            break

    return {'test_loss': total_loss / total_samples, "BCE": BCE, "KLD":KLD}


