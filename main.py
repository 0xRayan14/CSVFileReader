from typing import Any
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Heures au total

df = pd.read_csv("path/to/csvfile")
heureTotal: float | Any = df['Duration'].sum() / 3600
df['totalHours'] = df['Duration'] / 3600

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Assuming 'df' is your DataFrame with columns 'Date', 'Duration', 'Project', and 'Activity'

start_date = '2023-08-14'
end_date = '2023-12-21'
filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
filtered_df['Duration'] = pd.to_numeric(filtered_df['Duration'], errors='coerce')
total_hours = filtered_df['Duration'].sum() / 3600

expected_hours: float = 697.5
print(f"{total_hours} hours in total on {expected_hours}")

# Histogram for total hours per project
project_hours = filtered_df.groupby('Project')['Duration'].sum() / 3600
ax = project_hours.plot(kind='bar', title='Total Hours per Project')
plt.xlabel('Project')
plt.ylabel('Total Hours')

# Adding annotations
for i, v in enumerate(project_hours):
    if pd.notna(v) and np.isfinite(i) and np.isfinite(v):  # Check if the value is not NaN and i, v are finite
        ax.text(i, v + 0.1, f"{v:.2f}", ha='center', va='bottom')

plt.savefig('histogramProject.png')

# Histogram for total hours per task within each project
task_hours = filtered_df.groupby(['Project', 'Activity'])['Duration'].sum() / 3600
ax = task_hours.unstack().plot(kind='bar', stacked=True, title='Total Hours per Task in Each Project')
plt.xlabel('Project')
plt.ylabel('Total Hours')

# Adding annotations on each bar
for i, (name, values) in enumerate(task_hours.unstack().iterrows()):
    total_height = 0
    for j, v in enumerate(project_hours):
        ax.text(j, v + 0.1, f"{v:.2f}", ha='center', va='bottom')

# Legend on the upper left
ax.legend(loc='upper left', bbox_to_anchor=(1, 1), title='Activity')

plt.savefig('histogramActivity.png')

# Heures des projets
def calculate_total_hours(df, activity):
    activity_df = df[df['Activity'] == activity]
    total_hours = activity_df['Duration'].sum() / 3600
    return total_hours


total_duration = df['Duration'].sum() / 3600

# Heures des activités

activities = ['Vacances', 'CIE', 'EPSIC - Cours pro', 'Maladie', 'Cours Alice', 'Introduction apprentissage']

for activity in activities:
    total_hours = calculate_total_hours(df, activity)
    percentage = (total_hours / total_duration) * 100
    print(f"{total_hours:.2f} heures de {activity} ({percentage:.2f}%)")

rest_of_hours = total_duration - sum(calculate_total_hours(df, activity) for activity in activities)
print(f"Le reste est de {rest_of_hours:.2f} heures")


# Moyenne coaching

coaching_df = df[df['Activity'] == 'Coaching']
total_hours_coaching = coaching_df['Duration'].sum() / 3600
average_coaching = coaching_df['Duration'].mean() / 3600

print(f"{average_coaching:.2f} heures de moyenne de coaching")

# Cout de l'apprenti (programmation)

programming_projects = ['Rust', 'Site web statique', 'Java', 'Integration maquette',
                        'Projet présentation par groupes de 3', 'JavaScript', 'Grades calculator']
project_df = df[df['Project'].isin(programming_projects)]
total_hours_programing = project_df['Duration'].sum() / 3600

print(f"{total_hours_programing * 100:.2f}CHF de coût de programmation")

# Cout de l'apprenti (administratif)

cours = ['EPSIC - Cours pro', 'CIE', 'Vacances', 'Maladie', 'Cours Alice', 'Absence']
cours_df = df[df['Activity'].isin(cours)]
total_hours_cours = cours_df['Duration'].sum() / 3600
print(f"{(total_duration - (total_hours_programing + total_hours_cours)) * 100:.2f}CHF coût administration")

# Perte maladie

maladie_df = df[df['Activity'] == 'Maladie']
total_hours_maladie = maladie_df['Duration'].sum() / 3600

print(f"{total_hours_maladie * 100:.2f}CHF pertes dûes à la maladie")

# Retard le matin

at_work_df = df[df['Activity'] - cours_df]

df_unique_dates = at_work_df.drop_duplicates(subset=['Date'])

late_count = sum(df_unique_dates['From'] != '8:10')

if late_count > 0:
    print(f"Vous êtes arrivés en retard {late_count} fois.")
else:
    print("Vous n'êtes jamais arrivés en retard.")