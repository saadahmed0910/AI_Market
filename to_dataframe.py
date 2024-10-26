import pandas as pd

#Save data to folder on desktop or change path according to how you chose to save it
data = pd.read_json('C:\Users\saada\Desktop\Market Analysis with AI\data.json')

# Create an empty list to hold the formatted data
organized_data = []

# Iterate through the JSON 
for school, details in data.items():
    for price_info in details['Prices']:
        # Append to dict so it can be used in dataframe
        organized_data.append({
            'School': school,
            'Package': price_info['Name'],
            'Price': price_info['Price']
        })

# Convert the list to a DataFrame
df = pd.DataFrame(organized_data)

# Further split the "Price" column if needed (for example, to separate amount and tax/session info)
df[['Amount', 'Additional Info']] = df['Price'].str.split(' ', n=1, expand=True)

# Drop the original "Price" column if not needed
df = df.drop(columns=['Price'])

# Display the organized DataFrame
df


