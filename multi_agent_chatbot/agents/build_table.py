import pandas as pd

def build_table(dataframe):
    return dataframe.style.set_properties(**{'background-color': 'lightblue', 'color': 'black'})
