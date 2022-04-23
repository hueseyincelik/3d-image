import matplotlib.pyplot as plt
import matplotlib as mpl

from scipy import stats
import numpy as np

class Plot:
	def __init__(self, steps, shifts, chi_squared, df, orders, p=0.95, size=(10,6), latex=True):
		if chi_squared.shape[1] != len(orders):
			raise ValueError("Number of chi-squared data sets doesn't match the number of polynomial orders!")

		if latex:
			plt.rcParams['text.usetex'] = True
			plt.rcParams["font.family"] = ["Latin Modern Roman"]
			plt.rcParams['text.latex.preamble'] = r'\usepackage[locale=US,per-mode=symbol,separate-uncertainty,sticky-per]{siunitx}\usepackage[T1]{fontenc}\usepackage{lmodern}\usepackage{microtype}'

		chi_squared /= stats.distributions.chi2.ppf(p, df)
		k = [(df + 1)/step for step in steps]

		self.figure, self.axis = plt.subplots(figsize=size)

		orders_name = {'Constant': 0, 'Linear': 1, 'Quadratic': 2, 'Cubic': 3, 'Quartic': 4, 'Quintic': 5}
		colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:cyan', 'tab:pink', 'tab:purple']
		markers = ['o', '^', 'x', '*', 's', 'D']

		for _, (chi_square, shift) in enumerate(zip(chi_squared, shifts)):
			for j, (chi, order) in enumerate(zip(chi_square, orders)):

				self.axis.scatter(k, chi, s=30, marker=markers[j], color=colors[j], label=rf'Normalized {list(orders_name.keys())[list(orders_name.values()).index(order)]} $\chi^2\left(k\right)$' if shift == 0 else None, zorder=4)

				if shift == 0:
					self.axis.plot(x := np.linspace(k[-1], k[0], 1000), interpolate.PchipInterpolator(k[::-1], chi[::-1])(x), color=colors[j], lw=2.0, zorder=2)

				elif shift > 0:
					self.axis.plot(x := np.linspace(k[-1], k[0], 1000), interpolate.PchipInterpolator(k[::-1], chi[::-1])(x), color=colors[j], ls='dashed', zorder=2)

				else:
					self.axis.plot(x := np.linspace(k[-1], k[0], 1000), interpolate.PchipInterpolator(k[::-1], chi[::-1])(x), color=colors[j], ls='dotted', zorder=2)

		self.axis.axhline(1, color='red', linestyle='dashdot', label=rf'Critical Value $\alpha$ for $p = {p}$', zorder=3)

		self.axis.grid(True, which='major', axis='both', linewidth=0.5, alpha=0.5, linestyle='dashed', zorder=1)
		self.axis.tick_params(axis='both', which='both', direction='in', bottom=True, left=True, top=True, right=True, labelbottom=True, labeltop=False, labelleft=True, labelright=False)
		self.axis.minorticks_on()

		self.axis.xaxis.set_major_formatter(mpl.ticker.FormatStrFormatter('%.0f'))
		self.axis.xaxis.get_major_ticks()[0].label1.set_visible(False)

		self.axis.set_xlim(left=0)
		self.axis.set_ylim(bottom=0)

		self.axis.set_xlabel(r'Sliced Image Stack Size $k$')
		self.axis.set_ylabel(r"Normalized Pearson's Cumulative Test Statistic $\chi^2$")

		handles, _ = self.axis.get_legend_handles_labels()
		self.axis.legend(handles=[*handles[:-1], mpl.lines.Line2D([0], [0],color='white'), handles[-1], mpl.lines.Line2D([0], [0], color='black', label=r'Monotonic Cubic Spline $S$')], framealpha=1.0)

	def show(self):
		self.figure.tight_layout()
		plt.show()

	def save_figure(self, file_name):
		self.figure.savefig(file_name, bbox_inches='tight')