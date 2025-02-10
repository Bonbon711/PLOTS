import pandas as pd
import matplotlib.pyplot as plt

# Read the data from the CSV file
df = pd.read_csv('bar_assignment.csv')

# Transform 1 into "Yes" and 0 into "No"
df['COUNT'] = df['COUNT'].map({1: 'Yes', 0: 'No'})

# Create a crosstab to prepare for the stacked bar chart
crosstab = pd.crosstab(df['LABEL'], df['COUNT'])

# Plot the horizontal stacked bar chart
crosstab.plot(kind='barh', stacked=True, color=['red', 'green'])
plt.xlabel('Count')
plt.ylabel('Label')
plt.title('Horizontal Stacked Bar Chart')
plt.legend(title='COUNT')
plt.show()
