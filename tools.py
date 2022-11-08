import pandas as pd
from math import ceil, floor


class Table():
    '''
    Hold table data to generate a table
    in the command line
    '''

    table = ""
    rows = list()
    columns = list()

    def __init__(self, columns=list()) -> None:
        # If columns are defined in init, set them
        if isinstance(columns, pd.DataFrame):
            self.columns = columns.columns.to_list()
        elif isinstance(columns, list):
            self.columns = columns

        # Create the table immediately
        self.create_table()

    def __str__(self) -> str:
        # print(Table) prints the table output
        return self.table

    def create_table(self) -> None:
        # From columns, create rows for indexes and columns and junction rows

        # 0 - Divider
        # 1 - Indexes
        # 2 - Divider
        # 3 - Column Names
        # 4 - Divider
        for i in range(5):
            # Init row
            row = ""

            # Every second row is a divider
            if i % 2 == 0:
                # Crosspoint between lines are represented as +
                row = "+"
                for column in self.columns:
                    # Create the index and add '-' for each character in the column name including a space either side
                    row += ("-" * (len(column)+2)) + "+"

            # Indexes of columns
            if i == 1:

                # First divider on the left
                row = "| "

                # Add each column into the row
                for column in self.columns:

                    index = str(self.columns.index(column))

                    # Turn the string into a list of characters and measure the length
                    difference = (len(column)-len(list(index))) / 2

                    # If it's a float, round up on one side and round down on the other for the number
                    row += (" " * floor(difference)) + \
                        index + (" " * ceil(difference)) \
                        + " | "
            elif i == 3:
                # Connect list of names with a divider either side
                row = "| " + " | ".join(self.columns) + " |"

            # Add the row to the table
            self.rows.append(row)
        # Join the rows together to create the table
        self.table = "\n".join(self.rows)

    def set_columns(self, columns) -> None:
        # Set the columns of the table
        self.columns = columns
        self.create_table()


def tsvToCsv(loc: str) -> None:
    # Convert a tsv file to a csv file
    with open(loc, "r") as file:
        print("Converting now!")
        with open("%s.csv" % loc.removesuffix(".tsv"), "w") as newFile:
            newFile.write(file.read().replace('\t', ','))
        print("Done!")
