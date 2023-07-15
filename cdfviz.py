import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import fsolve
from matplotlib.widgets import Slider


# Initial parameters
mu_demand_init, sigma_demand_init = 1.5, 0.3
mu_supply_init, sigma_supply_init = 0.5, 0.3

# Define the demand and supply curves


def demand(p, mu, sigma):
    return 1 - norm.cdf(p, mu, sigma)


def supply(p, mu, sigma):
    return norm.cdf(p, mu, sigma)

# Function to find equilibrium


def find_equilibrium(mu_demand, sigma_demand, mu_supply, sigma_supply):
    price_eq = fsolve(lambda p: supply(
        p, mu_supply, sigma_supply) - demand(p, mu_demand, sigma_demand), 0.5)
    quantity_eq = supply(price_eq, mu_supply, sigma_supply)
    return price_eq[0], quantity_eq


# Generate initial data
prices = np.linspace(0, 2, 1000)
demand_quantities = demand(prices, mu_demand_init, sigma_demand_init)
supply_quantities = supply(prices, mu_supply_init, sigma_supply_init)

# Initial equilibrium
equilibrium_price, equilibrium_quantity = find_equilibrium(
    mu_demand_init, sigma_demand_init, mu_supply_init, sigma_supply_init)

# Creating the plot
fig, ax = plt.subplots(figsize=(10, 5))
plt.subplots_adjust(bottom=0.4)

# Plots
demand_plot, = plt.plot(prices, demand_quantities, label='Demand')
supply_plot, = plt.plot(prices, supply_quantities, label='Supply')
equilibrium_plot, = plt.plot(equilibrium_price, equilibrium_quantity, 'ro')

# Sliders
axcolor = 'lightgoldenrodyellow'
ax_mu_demand = plt.axes([0.2, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_sigma_demand = plt.axes([0.2, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_mu_supply = plt.axes([0.2, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_sigma_supply = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)

s_mu_demand = Slider(ax_mu_demand, 'Demand Level (Mu)', 0.1,
                     2, valinit=mu_demand_init)
s_sigma_demand = Slider(ax_sigma_demand, 'Demand Elasticity (Sigma)',
                        0.01, 1.0, valinit=sigma_demand_init)
s_mu_supply = Slider(ax_mu_supply, 'Supply Level (Mu)', 0.1,
                     2.0, valinit=mu_supply_init)
s_sigma_supply = Slider(ax_sigma_supply, 'Supply Elasticity (Sigma)',
                        0, 1.0, valinit=sigma_supply_init)


def update(val):
    mu_demand = s_mu_demand.val
    sigma_demand = s_sigma_demand.val
    mu_supply = s_mu_supply.val
    sigma_supply = s_sigma_supply.val
    demand_quantities_new = demand(prices, mu_demand, sigma_demand)
    supply_quantities_new = supply(prices, mu_supply, sigma_supply)
    equilibrium_price_new, equilibrium_quantity_new = find_equilibrium(
        mu_demand, sigma_demand, mu_supply, sigma_supply)
    demand_plot.set_ydata(demand_quantities_new)
    supply_plot.set_ydata(supply_quantities_new)
    equilibrium_plot.set_data(equilibrium_price_new, equilibrium_quantity_new)
    fig.canvas.draw_idle()


s_mu_demand.on_changed(update)
s_sigma_demand.on_changed(update)
s_mu_supply.on_changed(update)
s_sigma_supply.on_changed(update)


plt.legend()

plt.xlabel('Price')
plt.ylabel('Quantity')

plt.grid(True)

plt.show()
