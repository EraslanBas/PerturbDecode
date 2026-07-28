from perturbdecode.utils.libraries import *



class CVAE_basic(nn.Module):

    def __init__(self, n_inputs, n_latents, n_cond, n_cond_in):
        super().__init__()

        self.n_inputs = n_inputs
        self.n_latents = n_latents
        self.n_cond = n_cond

        self.encoder = CVAE_basic_Encoder(n_inputs=n_inputs, 
                                          n_latents=n_latents, 
                                          n_cond=n_cond)
        self.decoder = CVAE_basic_Decoder(n_inputs=n_inputs, 
                                          n_latents=n_latents, 
                                          n_cond=n_cond)
        self.embedding = CVAE_basic_EmbeddingLayer(n_in=n_cond_in, 
                                                   n_out=n_cond)

    def forward(self, x, c):

        c = self.embedding(c)

        means, log_var = self.encoder(x, c)
        std = torch.exp(0.5 * log_var)
        eps = torch.randn_like(std)
        z = eps * std + means

        recon_x = self.decoder(z, c)

        return recon_x, x, means, log_var, c

    def inference(self, x, c):
        c = self.embedding(c)
        means, _ = self.encoder(x, c)
        return means

    def generate(self, z, c):
        c = self.embedding(c)
        recon_x = self.decoder(z, c)
        return recon_x

    def get_embedding(self, c):
        return self.embedding(c)


    
class CVAE_basic_Encoder(nn.Module):
    def __init__(self, n_inputs, n_latents, n_cond):
        super().__init__()

        self.encoder = nn.Sequential(nn.Linear(n_inputs+n_cond, 512),
                                     nn.BatchNorm1d(512),
                                     nn.ReLU(inplace=True),
                                     nn.Linear(512, 512),
                                    )

        self.linear_means = nn.Linear(512, n_latents)
        self.linear_log_var = nn.Linear(512, n_latents)

    def forward(self, x, c):
        
        x = torch.cat((x, c), dim=1)
        x = self.encoder(x)
        means = self.linear_means(x)
        logvar = self.linear_log_var(x)
        return means, logvar

    
class CVAE_basic_Decoder(nn.Module):
    def __init__(self, n_inputs, n_latents, n_cond):
        super().__init__()

        self.decoder = nn.Sequential(nn.Linear(n_latents + n_cond, 512),
                                     nn.ReLU(inplace=True),
                                     nn.Linear(512, n_inputs),
                                    )

    def forward(self, z, c):
        x = torch.cat((z, c), dim=1)
        x = self.decoder(x)
        return x

        
def CVAE_basic_get_loss_fn(alpha):

    def vae_loss_fn(recon_x, x, mean, log_var, c):
        BCE = torch.nn.functional.mse_loss(
            recon_x, x, reduction='sum')
        KLD = -0.5 * torch.sum(1 + log_var - mean.pow(2) - log_var.exp())

        return (BCE + alpha*KLD)/x.size(0), BCE, KLD

    return vae_loss_fn


class CVAE_basic_EmbeddingLayer(nn.Module):
    def __init__(self, n_in, n_out):
        super(CVAE_basic_EmbeddingLayer, self).__init__()
        self.embedding_layer = nn.Sequential(nn.Linear(n_in, n_out))

    def forward(self, x):
        return self.embedding_layer(x)
