import matplotlib.pyplot as plt

def Plot(data: dict):
    _, ax = plt.subplots()
    plt.style.use("dark_background")
    fruits = bar_labels = ['Happy', 'Calm', 'Sad', 'Stressed', 'Confident']
    counts = list(data.values())
    bar_colors = ['tab:olive', 'tab:green', 'tab:cyan', 'tab:red', 'tab:purple']
    ax.bar(fruits, counts, label=bar_labels, color=bar_colors)
    ax.set_ylabel('Mood Count')
    ax.set_title('Your mood record')
    ax.legend(title='Mood')
    plt.show()
