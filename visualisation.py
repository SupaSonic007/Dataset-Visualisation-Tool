from tools import Table
import pandas as pd
import tkinter as tk
from tkinter.filedialog import askopenfilenames
import seaborn as sb
import matplotlib.pyplot as plt
from os import system

# Grab column name based on index of the columns list from the attributes of the dataframe
def get_column_names(columns: list):
    return [ds.columns.to_list()[int(column.strip())] for column in columns]

# Format the dates to only have month and year
def format_dates(date: str, date_length=True) -> pd.Series:
    date
    if date_length:
        date = "-".join(date.split("-")[:2])
    else:
        date = "-".join(date.split("-")[1:])
    return dates


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
xName = input("X Name or None (blank): ")
print("\n Y:")
col2 = input("> ")
yName = input("Y Name or None (blank): ")
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


print("\n Limit x (min: %s, max:%s)" % (ds[x].min(), ds[x].max()))
xmin = input("X min: ")
xmax = input("X max: ")

print("\n Limit y (min: %s, max:%s)" % (ds[y].min(), ds[y].max()))
ymin = input("Y min: ")
ymax = input("Y max: ")

print("\nName of graph:")
name = input("Name: ")

# Sample before formatting for less stress on computer
ds = ds.sample(frac=float(sample))

# If type is date, else only use month and year
if "date" in hue.lower():
    dates = ds[hue].to_list()
    if len(dates[0].split("-")[0]) == 4:
        ds[hue] = pd.Series(list(map(format_dates, dates)))

# Clear the terminal
system("cls")
if sort_columns:
    sort_col_names = get_column_names([sort_columns.split(",")])
    ds.sort_values(sort_col_names)

if sort_columns:
    ds.sort_values(by=[sort_columns or (x, y)])

# Create the plot and save it
scatter = sb.scatterplot(x=x, y=y, hue=hue or None,
                         data=ds, palette=palette)
scatter.set(ylim=(float(ymin or ds[y].min()), float(ymax or ds[y].max())), xlim=(float(
    xmin or ds[x].min()), float(xmax or ds[x].max())), xlabel=(xName or None), ylabel=(yName or None), title=name)
plt.legend(loc="upper right")
plt.savefig("%s-%s_%s_%d_%d_%d_%d_%d" % (x, y, hue or 'None', round(float(sample)*100) or 'None', round(float(
    ymin or ds[y].min())), round(float(ymax or ds[y].max())), round(float(xmin or ds[x].min())), round(float(xmax or ds[x].max()))))
plt.show()
