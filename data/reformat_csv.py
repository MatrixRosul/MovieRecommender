import pandas as pd
import ast

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('vectorize.csv')

# Function to convert the string representation of a list to a list of floats


def convert_to_float_list(string_list):
    # Remove unnecessary characters and split the string into a list
    values_str = string_list.replace('[', '').replace(
        ']', '').replace('\n', '').replace(',', ' ').split()

    # Convert each value to a float
    return [float(x) for x in values_str]


if __name__ == ("__main__"):
    # Apply the function to the 'vector' column
    df['vector'] = df['vector'].apply(convert_to_float_list)

    # Save the DataFrame back to a CSV file
    df.to_csv('formatted_file.csv', index=False)
