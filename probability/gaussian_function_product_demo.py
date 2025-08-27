import numpy as np
import matplotlib.pyplot as plt

# from scipy.stats import norm
from matplotlib.widgets import Slider, Button


def gaussian(x, mu, sigma):
    """Gaussian function"""
    return np.exp(-((x - mu) ** 2) / (2 * sigma**2)) / (sigma * np.sqrt(2 * np.pi))


# Initial parameters for two Gaussian distributions
mu1_init, sigma1_init = (
    0,
    1,
)  # Initial mean and standard deviation of the first Gaussian distribution
mu2_init, sigma2_init = (
    2,
    0.5,
)  # Initial mean and standard deviation of the second Gaussian distribution

# Generate x-axis data
x = np.linspace(-5, 5, 300)

# Create the figure and subplots
fig, ax = plt.subplots(figsize=(12, 8))
plt.subplots_adjust(left=0.1, bottom=0.35)  # Make room for sliders


# Create function to update the plot
def update_plot(mu1, sigma1, mu2, sigma2):
    ax.clear()

    # Calculate parameters for the product Gaussian distribution
    mu_product = (mu1 * sigma2**2 + mu2 * sigma1**2) / (sigma1**2 + sigma2**2)
    sigma_product = np.sqrt((sigma1**2 * sigma2**2) / (sigma1**2 + sigma2**2))

    # Calculate two Gaussian functions and their product
    g1 = gaussian(x, mu1, sigma1)
    g2 = gaussian(x, mu2, sigma2)
    product = g1 * g2

    # Normalize the product for better comparison
    product_normalized = product / np.max(product) * np.max(g1)

    # Plot the original Gaussian functions
    ax.plot(x, g1, label=f"Gaussian 1: μ={mu1:.2f}, σ={sigma1:.2f}", linestyle="--")
    ax.plot(x, g2, label=f"Gaussian 2: μ={mu2:.2f}, σ={sigma2:.2f}", linestyle="--")

    # Plot the product result
    ax.plot(
        x,
        product_normalized,
        label="Product result (normalized)",
        color="red",
        linewidth=2,
    )

    # Plot the theoretical product Gaussian distribution
    g_product = gaussian(x, mu_product, sigma_product)
    g_product_normalized = g_product / np.max(g_product) * np.max(g1)
    ax.plot(
        x,
        g_product_normalized,
        label=f"Theoretical Product Gaussian: μ={mu_product:.2f}, σ={sigma_product:.2f}",
        linestyle=":",
        color="green",
        linewidth=2,
    )

    # Add vertical lines to show the mu values
    ax.axvline(x=mu1, color="blue", linestyle="-.", alpha=0.7, label=f"μ1={mu1:.2f}")
    ax.axvline(x=mu2, color="orange", linestyle="-.", alpha=0.7, label=f"μ2={mu2:.2f}")
    ax.axvline(
        x=mu_product,
        color="green",
        linestyle="-.",
        alpha=0.7,
        label=f"μ_product={mu_product:.2f}",
    )

    # Add legend and title
    ax.set_title("Product of Two Gaussian Functions", fontsize=14)
    ax.set_xlabel("x", fontsize=12)
    ax.set_ylabel("Probability Density", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    fig.canvas.draw_idle()


# Initial plot
update_plot(mu1_init, sigma1_init, mu2_init, sigma2_init)

# Create axes for the sliders
ax_mu1 = plt.axes([0.15, 0.25, 0.65, 0.03], facecolor="lightgoldenrodyellow")
ax_sigma1 = plt.axes([0.15, 0.2, 0.65, 0.03], facecolor="lightgoldenrodyellow")
ax_mu2 = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor="lightgoldenrodyellow")
ax_sigma2 = plt.axes([0.15, 0.1, 0.65, 0.03], facecolor="lightgoldenrodyellow")
ax_reset = plt.axes([0.15, 0.02, 0.1, 0.04])


# Create sliders
s_mu1 = Slider(ax_mu1, "μ1", -3.0, 3.0, valinit=mu1_init, valstep=0.1)
s_sigma1 = Slider(ax_sigma1, "σ1", 0.1, 2.0, valinit=sigma1_init, valstep=0.1)
s_mu2 = Slider(ax_mu2, "μ2", -3.0, 3.0, valinit=mu2_init, valstep=0.1)
s_sigma2 = Slider(ax_sigma2, "σ2", 0.1, 2.0, valinit=sigma2_init, valstep=0.1)
reset_button = Button(
    ax_reset, "Reset", color="lightgoldenrodyellow", hovercolor="0.975"
)


# Define update function for sliders
def update(_):
    # The underscore (_) is used as a placeholder for the event argument that Matplotlib sliders pass
    # This argument contains information about the slider event but we don't need to use it
    # It's a common Python convention to use underscore for variables that won't be used
    update_plot(s_mu1.val, s_sigma1.val, s_mu2.val, s_sigma2.val)


# Define reset function
def reset(_):
    s_mu1.reset()
    s_sigma1.reset()
    s_mu2.reset()
    s_sigma2.reset()


# Register the update function with each slider
s_mu1.on_changed(update)
s_sigma1.on_changed(update)
s_mu2.on_changed(update)
s_sigma2.on_changed(update)
reset_button.on_clicked(reset)

plt.show()
