from matplotlib import pyplot as plt
import numpy as np
from sklearn.mixture import GaussianMixture



folder_path = "/home/hibu60/Documents/unif/unifUNIGE/lab_physics_IV/this_data/"
file = 'pmt1_2053v_threshold_50mv'
X = np.loadtxt(folder_path + file)
X = X.reshape(-1, 1)


MIN_ADC_VALUE = 43
MAX_ADC_VALUE = 300


# Fit models with 1-10 components
k_arr = np.arange(4) + 1
models = [
         GaussianMixture(n_components=k).fit(X)
         for k in k_arr
]

for model in models:
    print(model.means_)


def gaussian(x, a, x0, sigma):
    y = a*np.exp(-(x-x0)**2/(2*sigma**2))
    return y



def plot_mixture(gmm, X, show_legend=True, ax=None):
    if ax is None:
        ax = plt.gca()

        # Compute PDF of whole mixture
    x = np.arange(MIN_ADC_VALUE, MAX_ADC_VALUE, 1)
    logprob = gmm.score_samples(x.reshape(-1, 1))
    pdf = np.exp(logprob)

    print('-------------------------------')
    print(gmm.get_params())
    n_components = gmm.n_components
    means = gmm.means_
    covariances = gmm.covariances_
    weights = gmm.weights_
    for i in range(len(means)):
        y = gaussian(x, 1000, means[i][0], covariances[i][0])
        ax.plot(x, y, linestyle=':')

    hist, bin_edges = np.histogram(X, bins=x)
    ax.plot(bin_edges[:-1], hist)

     # Compute PDF for each component
    responsibilities = gmm.predict_proba(x.reshape(-1, 1))
    pdf_individual = responsibilities * pdf[:, np.newaxis]

    # Plot data histogram
    #ax.hist(X, 300, density=True, histtype='stepfilled', alpha=0.4, label='Data')

    # Plot PDF of whole model
    #ax.plot(x, pdf, '-k', label='Mixture PDF')

    # Plot PDF of each component
    #ax.plot(x, pdf_individual, '--', label='Component PDF')
    ax.set_xlabel('$x$')
    ax.set_ylabel('$p(x)$')
    ax.set_xlim((0, 300))
    if show_legend:
        ax.legend()

 # Show all models for n_components 1 to 9
_, axes = plt.subplots(3, 3, figsize=np.array([3,3])*3, dpi=100)
for gmm, ax in zip(models, axes.ravel()):

     plot_mixture(gmm, X, show_legend=False, ax=ax)
     ax.set_title(f'k={gmm.n_components}')
plt.tight_layout()
plt.show()
