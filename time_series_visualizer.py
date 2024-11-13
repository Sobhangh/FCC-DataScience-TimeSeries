import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'],index_col='date')

lower2_5 = df['value'].quantile(0.025)
higher2_5 = df['value'].quantile(0.975)

print("outliers #############################")
print(lower2_5, higher2_5)
# Clean data
df = df[(df['value']>=lower2_5) & (df['value']<=higher2_5)]


def draw_line_plot():
    # Draw line plot

    fig , ax = plt.subplots()
    ax.plot(df.index,df['value'])
    ax.set_xlabel('Date')
    ax.set_ylabel("Page Views")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)

    df_bar = df_bar.groupby(df_bar.date.dt.year).apply( lambda x: x.groupby(x.date.dt.month).mean())
    df_bar = df_bar.unstack()

    print("grouped data #############")
    df_bar.columns = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    df_bar.columns.name = "Month"
    print(df_bar)

    # Draw bar plot
    fig , ax = plt.subplots()
    df_bar.plot(kind='bar',ax=ax)
    plt.ylabel("Average Page Views")
    plt.xlabel("Years")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    #df_box['year'] = df_box.date.dt.year.astype(np.int8)
    print("years################################")
    print( df_box['year'])
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box['month_num'] = df_box.date.dt.month.astype(np.int8)
    print(df_box['month_num'])

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1,2)
    sns.boxplot(x="year",
                y="value",
                data=df_box,
                ax=ax1)
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel("Year")
    page_views = "Page Views"
    ax1.set_ylabel(page_views)

    #df_box.sort_values(by=["month_num"])
    sns.boxplot(x="month",
                y="value",
                data=df_box,
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                ax=ax2)
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel("Month")
    ax2.set_ylabel(page_views)

    # Save image and return fig (don't change this part)
    fig.set_figwidth(30)
    fig.savefig('box_plot.png')
    return fig
