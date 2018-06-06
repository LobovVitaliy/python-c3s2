import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from coursework.db import connect


def show_rating():
    df = pd.read_sql('SELECT "group", AVG(rating) as rating FROM students GROUP BY "group"', connect("10.0.3.122"))

    groups = [item.tolist()[0] for item in df.values]
    ratings = [item.tolist()[1] for item in df.values]

    plt.title('Group rating')

    plt.bar(np.arange(len(ratings)), ratings)
    plt.xticks(np.arange(len(groups)), groups)

    plt.xlabel('Group')
    plt.ylabel('Rating')

    plt.show()
