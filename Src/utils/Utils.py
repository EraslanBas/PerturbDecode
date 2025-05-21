from .libraries import optim, torch

def setup_lr_scheduler(name, optimizer, step_size=10, gamma=0.5):
    if name == 'none':
        return None
    elif name == 'StepLR':
        return optim.lr_scheduler.StepLR(optimizer=optimizer, step_size=step_size, gamma=gamma)

    
def setup_optimizer(name, param_list):
    if name == 'sgd':
        return optim.SGD(param_list)
    elif name == 'adam':
        return optim.Adam(param_list)
    elif name == 'RMSprop':
        return optim.RMSprop(param_list)
    elif name == 'Adagrad':
        return optim.Adagrad(param_list)
    elif name == 'Adadelta':
        return optim.Adadelta(param_list)
    elif name == 'Adamax':
        return optim.Adamax(param_list)
    elif name == 'LBFGS':
        return optim.LBFGS(param_list)
    elif name == 'SparseAdam':
        return optim.SparseAdam(param_list)
    elif name == 'ASGD':
        return optim.ASGD(param_list)
    elif name == 'RAdam':
        return optim.RAdam(param_list)
    else:
        raise KeyError("%s is not a valid optimizer (must be one of ['sgd', adam']" % name)

def save_checkpoint(current_state, filename):
    torch.save(current_state, filename)

def load_checkpoint(model, checkpoint_file):
    model.load_state_dict(torch.load(checkpoint_file)['state_dict'])
