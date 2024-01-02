import pandas as pd
import matplotlib.pyplot as plt


def plot(filename: str):
    # Load your data into a DataFrame
    data = pd.read_csv(filename)
    
    # Convert 'date' column to datetime and extract the year
    data['date'] = pd.to_datetime(data['date'])
    data['year'] = data['date'].dt.to_period('Y')
    
    # Aggregating data to get annual sum for each category
    aggregated_data = data.groupby(['year', 'category']).agg(
        {'price_with_tax': 'sum'}
        ).reset_index()
    
    # Pivoting the data for the bar chart
    pivot_data = aggregated_data.pivot(
        index='year',
        columns='category',
        values='price_with_tax'
        ).fillna(0)
    
    # Ensuring the 'Other' category is last
    pivot_data = pivot_data[
        sorted(pivot_data.columns, key=lambda x: (x != 'Other', x))]
    
    # Choosing a colormap with more distinguishable colors
    # color_map = plt.cm.get_cmap('tab20', len(aggregated_data.columns))
    color_map = plt.colormaps['tab20']
    
    # Creating a stacked bar chart
    ax = pivot_data.plot(
        kind='bar',
        stacked=True,
        figsize=(12, 8),
        color=[color_map(i) for i in range(len(pivot_data.columns))]
        )
    
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # Calculating the sum of spendings for each category
    category_sums = pivot_data.sum(axis=0)
    
    # Creating custom labels for the legend with category names and their respective total spendings
    legend_labels = [f"{cat}: ${total:.2f}" for cat, total in
                     category_sums.items()]
    
    # Creating and adjusting the legend within the plot area
    legend = ax.legend(
        legend_labels,
        title='',
        loc='upper center',
        ncol=2,
        bbox_to_anchor=(0.5, 0.95)
        )
    plt.setp(legend.get_texts(), fontsize=12)
    
    # Adjusting x-axis labels (years)
    ax.set_xticklabels(
        [label.get_text() for label in ax.get_xticklabels()],
        fontsize=12,
        fontweight='bold',
        rotation=0
        )
    for label in ax.get_xticklabels():
        label.set_y(
            label.get_position()[1] - 0.03
            )  # Adjusting the y-position of the labels for spacing
    
    # Adjusting plot elements
    plt.title(
        'Mobile Game Spendings by Year (2014 - 2023)',
        fontsize=16,
        fontweight='bold'
        )
    plt.xlabel('')
    plt.ylabel('Amount Spent (USD)')
    plt.tick_params(axis='x', which='both', length=0)
    plt.tight_layout()
    
    # Show the plot
    plt.show()
    

if __name__ == '__main__':
    plot('data.csv')
    