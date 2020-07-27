import pymc3 as pm


def run():
    with pm.Model():
        # Prior distributions for latent variables
        alpha = pm.Normal('alpha', 0, sd=100)
        beta = pm.Normal('beta', 0, sd=100)
        # x = pm.Normal('x', mu=10, sigma=10)

        # Draw samples
        # trace = pm.sample()
        trace = pm.sample(draws=1000)

        # Plot two parameters
        pm.plots.traceplot(trace, var_names=['alpha', 'beta'])


if __name__ == '__main__':
    run()
