import numpy as np
from copy import copy


def get_means(x):

    x_ = copy(x)
    #x_[np.isnan(x)] = 0
    # calculate inter class variances
    inter_vars = []
    mus_0 = []
    mus_1 = []
    for t in range(1, len(x_)-1):
        w_0 = np.sum(x_[:t])
        w_1 = np.sum(x_[t:])
        
        if ((not  w_1) and (not  w_0)):
            raise ValueError
        elif ((not w_1) or (not w_0)):
            mus_0.append(0.)
            mus_1.append(0.)
            inter_vars.append(0.)
        else:
            mu_0 = np.sum(np.arange(1, t+1)*x_[:t]) / w_0
            mu_1 = np.sum(np.arange(t+1, len(x_)+1)*x_[t:]) / w_1
            mus_0.append(mu_0)
            mus_1.append(mu_1)
            
            inter_var = w_0 * w_1 * (mu_0-mu_1)**2
            inter_vars.append(inter_var)
     
    
    # find the max of inter class variance
    ind_max = inter_vars.index(max(inter_vars))
    ind_mu_0 = int(mus_0[ind_max])
    ind_mu_1 = int(mus_1[ind_max])
  
    return ind_mu_0, ind_mu_1, ind_max


