#FIRST RUN FAMA FRENCH DATA FILE
import pandas as pd
import requests
import numpy as np
import plotly.express as px
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import *
import numpy as np
import plotly.graph_objects as go
import warnings
from pypfopt import plotting
import matplotlib.pyplot as plt
lower_b = 0
upper_b = 1
#setup----------------------------------------------------------
rf = .041
df = pd.read_csv("output.csv",index_col=0, parse_dates=True)
mu = mean_historical_return(df,frequency=52)
cov = sample_cov(df, frequency=52)
#EF-------------------------------------------------------------
ef = EfficientFrontier(mu, cov, weight_bounds=(lower_b, upper_b))
ef_best_port = ef.deepcopy()
ef_best_port.max_sharpe(risk_free_rate=rf)
ret_tangent, std_tangent, _ = ef_best_port.portfolio_performance()
#print(ef_plot.clean_weights())
#Graph-----------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(std_tangent, ret_tangent, marker=".", s=500, c="r", label="Max Sharpe Portfolio")
#Random Samples--------------------------------------------------
samples = 500000
w = np.random.dirichlet(np.ones(ef.n_assets), samples)
mask = np.all((w >= lower_b) & (w <= upper_b), axis=1)
w = w[mask][:10000]  # take first 1000 valid samples

rets = w.dot(ef.expected_returns)
stds = np.sqrt(np.diag(w @ ef.cov_matrix @ w.T))
sharpes =  (rets - rf) / stds
ax.scatter(stds, rets, marker=".", c=sharpes, cmap="YlGnBu")



plotting.plot_efficient_frontier(ef, ax=ax, show_assets=True)
plt.show()
print(f'The optuomal weights are {ef_best_port.clean_weights()} and the sharpe is {ef_best_port.portfolio_performance()[2]}')
