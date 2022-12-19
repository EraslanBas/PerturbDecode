from libraries import *

def setup_lr_scheduler(name, optimizer):
    if name == 'none':
        return None
    elif name == 'step':
        return optim.lr_scheduler.StepLR(optimizer=optimizer, step_size=10, gamma=0.5)

    
def setup_optimizer(name, param_list):
    if name == 'sgd':
        return optim.SGD(param_list)
    elif name == 'adam':
        return optim.Adam(param_list)
    else:
        raise KeyError("%s is not a valid optimizer (must be one of ['sgd', adam']" % name)

def save_checkpoint(current_state, filename):
    torch.save(current_state, filename)

def load_checkpoint(model, checkpoint_file):
    model.load_state_dict(torch.load(checkpoint_file)['state_dict'])
