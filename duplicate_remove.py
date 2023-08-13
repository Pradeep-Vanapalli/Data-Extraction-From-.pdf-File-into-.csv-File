import pandas as pd

# Load the CSV file into a DataFrame
csv_file_path = "output34.csv"
df = pd.read_csv(csv_file_path)

# Remove duplicates from the "Name" column
df_unique_names = df.drop_duplicates(subset=["Name"], keep="first")

# Save the modified DataFrame back to a new CSV file
output_csv_file_path = "unique_names34.csv"
df_unique_names.to_csv(output_csv_file_path, index=False)

print("Duplicates removed and saved to:", output_csv_file_path)
