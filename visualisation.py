from tools import Table
import pandas as pd
import tkinter as tk
from tkinter.filedialog import askopenfilenames
import seaborn as sb
import matplotlib.pyplot as plt
from os import system

# Grab column name based on index of the columns list from the attributes of the dataframe
def get_column_names(columns:list):
    return [ds.columns.to_list()[int(column.strip())] for column in columns]

# Format the dates to only have month and year
def format_dates(dates: pd.Series) -> pd.Series:
    dates = dates.to_list()
    if len(dates[0].split("-")[0]) == 4:
        for i in range(len(dates)):
            dates[i] = "-".join(dates[i].split("-")[:2])
    else:
        for i in range(len(dates)):
            dates[i] = "-".join(dates[i].split("-")[1:])
    return pd.Series(dates)

# Initialise tkinter without a window and grab the file/s
tk.Tk().withdraw()
files = askopenfilenames()

# Split the files into their own datasets and then concatenate them if there is more than one
datasets = []

for file in files:
    datasets.append(pd.read_csv(file))

if isinstance(datasets, list):
    ds = pd.concat(datasets)

# Fancy print statement to show all columns and indexes to ask which columns to compare
# Looks like:
# +----+----+----+
# | 0  | 1  | 2  |
# +----+----+----+
# | c1 | c2 | c3 |
# +----+----+----+

# Init columns
columns = "+"
print(ds.columns)
table = Table(ds)
# Print columns and indexes
print(table)

# Ask X and Y columns and Hue
print("\n X:")
col1 = input("> ")
print("\n Y:")
col2 = input("> ")
print("\n Hue (Leave blank for None):")
hue = input("> ")
print("\n Sample Size (0.00-1.00)")
sample = input("> ")

# Grab column names for Seaborn use
[x, y] = get_column_names([col1, col2])
if hue:
    [hue] = get_column_names([hue])

print("\n Sort by column/s (seperated by ',' if multiple or blank for none)")
sort_columns = input("> ")
if sort_columns:
    [sort_columns] = get_column_names([sort_columns])

# If type is date, else only use month and year
if "date" in hue.lower():
    ds[hue] = format_dates(ds[hue])

# Clear the terminal
system("cls")
if sort_columns: sort_col_names = get_column_names([sort_columns.split(",")]); ds.sort_values(sort_col_names)

if sort_columns: ds.sort_values(by=[sort_columns or (x, y)])

# Create the plot and save it
scatter = sb.scatterplot(x=x, y=y, hue=hue or None, data=ds.sample(frac=float(sample)))
scatter.set(ylim=(ds[y].min(), ds[y].max()), xlim=(ds[x].min(), ds[x].max()))
plt.legend(loc="upper right")
plt.savefig("%s-%s_%s_%d" % (x, y, hue or 'None', round(float(sample)*100) or 'None'))
plt.show()
