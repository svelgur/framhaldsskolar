import matplotlib.pyplot as plt
import pandas as pd
import requests
import json

# importing data trhough statice API
url = "https://px.hagstofa.is:443/pxis/api/v1/is/Samfelag/skolamal/2_grunnskolastig/0_gsNemendur/SKO02108b.px"
query_params = {
  "query": [
    {
      "code": "Bakgrunnur",
      "selection": {
        "filter": "item",
        "values": [
          "124"
        ]
      }
    },
    {
      "code": "Kyn",
      "selection": {
        "filter": "item",
        "values": [
          "0"
        ]
      }
    },
    {
      "code": "Bekkur",
      "selection": {
        "filter": "item",
        "values": [
          "Grade 1",
          "Grade 2",
          "Grade 3",
          "Grade 4",
          "Grade 5",
          "Grade 6",
          "Grade 7",
          "Grade 8",
          "Grade 9",
          "Grade 10"
        ]
      }
    }
  ],
  "response": {
    "format": "json"
  }
}

session = requests.Session()
response = session.post(url, json=query_params)
response_json = json.loads(response.content.decode('utf-8-sig'))

# Create df from json

# Prepare lists to hold years, grades and values
years = []
grades = []
values = []

# Extract years, grades and values from the data
for record in response_json['data']:
    year = record['key'][0] # The first element in the key array is the year
    grade = record['key'][3] # The third element in the key array is the grade
    value = record['values'][0]  # The first element in the values array is the value
    
    years.append(year)
    grades.append(grade)
    values.append(value)
    
df = pd.DataFrame({
    'artal': years,
    'bekkur': grades, 
    'fjoldi': values
})

df['fjoldi'] = pd.to_numeric(df['fjoldi'])
df['artal'] = pd.to_numeric(df['artal'])

# Setting up a pivot table
pivot_df = df.pivot(index='artal', columns='bekkur', values='fjoldi')
# Rename the grades column so "Grade 1" becomes "1. bekkur"
pivot_df.columns = [f"{int(grade.split()[1])}. bekkur" for grade in pivot_df.columns]
# Reorder columns numerically
new_order = sorted(pivot_df.columns, key=lambda x: int(x.split('.')[0]))
pivot_df = pivot_df[new_order]

# Create new df that tracks the changes of students for each grade through the 10 years of schooling
bekkjarlisti = [col for col in pivot_df.columns if 'bekkur' in col]
throun_arganga_grunnskoli = {}

for year in pivot_df.index:
    key = year
    tmp_list = []
    for bekkur in bekkjarlisti:
        if year < 2024:
            tmp_list.append(pivot_df.at[year, bekkur])
        else:
            tmp_list.append('Nan')
        year = year+1
    throun_arganga_grunnskoli[key] = tmp_list

df = pd.DataFrame.from_dict(throun_arganga_grunnskoli, orient="index")

# Normalizing dataframe
for column in df.columns:
    if column == df.shape[1] - 1:
        break
    elif column == 0:
        continue
    else:
        df[column+10] = df.apply(lambda s: (((s[column] - s[0])/s[0])*100)+100 if s[column] != 'Nan' else 0, axis=1)
df[0] = 100
df.drop([1,2,3,4,5,6,7,8,9],axis = 1, inplace = True)

cols = list(range(10))
df.set_axis(cols, axis=1,inplace=True)
df = df.round()

# Define a standard year range from 0 to 10 (representing the progression from "1. bekkur" to "10. bekkur")
standard_years = list(range(11))
# Initialize figure and axes for the plot
fig, ax = plt.subplots(figsize=(14, 8))

# Each line will be a trajectory starting from a different year
for start_year in df.index:  # Loops through all years in dataframe
    values = list(filter(lambda x: x > 0, list(df[df > 0].loc[start_year])))  # Holds all values > 0

    if len(values) > 5: #plot values if we have a sufficient no years
        ax.plot(standard_years[:len(values)], values, marker='o', label=f'Start: {start_year}')
        # Add labels at the end of each curve
        ax.text(standard_years[len(values)-1], values[-1], f'Upphafsár: {start_year}', fontsize=9, 
                verticalalignment='center', horizontalalignment='left')
        
ax.set_title('Staðlaður árlegur vöxtur fyrir upphafsár hvers 1. bekkjar')
ax.set_xlabel('Ár frá upphafi skólagöngu')
ax.set_ylabel('Hlutfallslegur vöxtur')
ax.grid(True)

plt.tight_layout()
plt.savefig('normalized_student_immigrant_growth.pdf')
plt.show()