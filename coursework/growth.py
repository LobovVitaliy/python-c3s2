import pandas as pd
import matplotlib.pyplot as plt
from coursework.db import connect


def show_growth():
    df = pd.read_sql('SELECT year, count(*) FROM students GROUP BY year ORDER BY year', connect("10.0.3.122"))

    years = [item.tolist()[0] for item in df.values]
    counts = [item.tolist()[1] for item in df.values]
    print(years)
    plt.title('Growth for the year')

    plt.plot(years, counts)

    plt.xlabel('Year')
    plt.ylabel('Count')

    plt.show()
