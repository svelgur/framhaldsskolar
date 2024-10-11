import matplotlib.pyplot as plt
import pandas as pd

# Data for each "bekkur" with the corresponding years where percentages are provided
data = {
    'Year': [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
    'bekkur1': [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
    'bekkur2': [None, 125, 111, 103, 100, 102, 94, 107, 112, 120, 142, 121, 113, 116, 110, 138, 129],
    'bekkur3': [None, None, 133, 108, 103, 105, 112, 107, 114, 132, 143, 162, 137, 130, 128, 156, 184],
    'bekkur4': [None, None, None, 125, 110, 107, 109, 120, 118, 131, 156, 168, 187, 152, 151, 161, 202],
    'bekkur5': [None, None, None, None, 125, 115, 115, 113, 125, 137, 151, 180, 200, 199, 169, 211, 220],
    'bekkur6': [None, None, None, None, None, 134, 122, 123, 126, 133, 164, 184, 211, 236, 227, 208, 289],
    'bekkur7': [None, None, None, None, None, None, 143, 139, 135, 136, 151, 188, 201, 224, 259, 292, 267],
    'bekkur8': [None, None, None, None, None, None, None, 149, 152, 149, 149, 168, 200, 220, 263, 313, 351],
    'bekkur9': [None, None, None, None, None, None, None, None, 157, 181, 172, 165, 187, 209, 239, 318, 393],
    'bekkur10': [None, None, None, None, None, None, None, None, None, 178, 196, 186, 183, 194, 228, 290, 412]
}

# Convert data into a DataFrame
df = pd.DataFrame(data)

# Define a standard year range from 0 to 10 (representing the progression from "1. bekkur" to "10. bekkur")
standard_years = list(range(11))

# Initialize figure and axes for the plot
fig, ax = plt.subplots(figsize=(14, 8))

# Each line will be a trajectory starting from a different year
for start_year in range(2007, 2018):  # Data starts in 2007 and the last trajectory that can fully form starts in 2017
    values = []  # To hold the percentage values
    valid_years = []  # To hold the actual years where data is available

    # Extract the values for each bekkur, shifting appropriately
    for offset in range(10):
        target_year = start_year + offset
        if target_year <= 2023:
            bekkur_label = f'bekkur{offset+1}'
            value = df.loc[df['Year'] == target_year, bekkur_label].values[0]
            if pd.notna(value):
                values.append(value)
                valid_years.append(target_year)

    # Plot each trajectory if data exists
    if values:
        ax.plot(standard_years[:len(values)], values, marker='o', label=f'Start: {start_year}')
        # Add labels at the end of each curve
        ax.text(standard_years[len(values)-1], values[-1], f'Start: {start_year}', fontsize=9, 
                verticalalignment='center', horizontalalignment='left')

ax.set_title('Normalized Yearly Growth for Each "1. Bekkur" Starting Year')
ax.set_xlabel('Years Since Start')
ax.set_ylabel('Percentage Growth')
ax.grid(True)

plt.tight_layout()
plt.savefig('normalized_student_immigrant_growth.pdf')
plt.show()
