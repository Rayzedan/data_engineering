import seaborn as sns
import matplotlib.pyplot as plt


def plot_linear(data, x, y, name):
	sns.lineplot(data=data, x=x, y=y)
	plt.title(name)
	plt.savefig(f'../plots/{name}.png')
	plt.close()


def plot_step(data, x, y, name):
	sns.stripplot(data=data, x=x, y=y)
	plt.title(name)
	plt.savefig(f'../plots/{name}.png')
	plt.close()
