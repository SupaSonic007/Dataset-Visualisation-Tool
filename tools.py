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

        if isinstance(columns, pd.DataFrame):
            self.columns = columns.columns.to_list()
        elif isinstance(columns, list):
            self.columns = columns

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
            row = ""

            if i % 2 == 0:
                row = "+"
                for column in self.columns:
                    row += ("-" * (len(column)+2)) + "+"

            if i == 1:

                row = "| "

                for column in self.columns:

                    index = str(self.columns.index(column))

                    difference = (len(column)-len(list(index))) / 2

                    row += (" " * floor(difference)) + \
                        index + (" " * ceil(difference)) \
                        + " | "
            elif i == 3:
                row = "| " + " | ".join(self.columns) + " |"

            self.rows.append(row)
            self.table = "\n".join(self.rows)

    def set_columns(self, columns) -> None:
        self.columns = columns
        self.create_table()


def tsvToCsv(loc: str) -> None:
    with open(loc, "r") as file:
        print("Converting now!")
        with open("%s.csv" % loc.removesuffix(".tsv"), "w") as newFile:
            newFile.write(file.read().replace('\t', ','))
        print("Done!")
