import seaborn as sns
import matplotlib.pyplot as plt


def plot_linear(data, x, y, name):
	plt.title(name)
	sns.lineplot(data=data.sample(1000), x=x, y=y, errorbar=None)
	plt.savefig(f'../plots/{name}.png')
	plt.close()


def plot_step(data, x, y, name):
	plt.title(name)
	sns.stripplot(data=data.sample(1000), x=x, y=y, dodge=True)
	plt.savefig(f'../plots/{name}.png')
	plt.close()
