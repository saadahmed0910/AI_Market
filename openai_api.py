from openai import OpenAI, OpenAIError
import os
from dotenv import load_dotenv
import json

import tiktoken

from grabHTML import key_word_price


load_dotenv()
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY")
                )

MAX_TOKEN_LIMIT = 128000


try:
# Convert the dictionary tp string so it can pass through api
  content_strings = json.dumps(key_word_price, separators=(',', ':'))

  # Join all the strings into a single string to pass to the API
  combined_content = "\n\n".join(content_strings)
  
  encoding = tiktoken.encoding_for_model("gpt-4o-mini")

  #check how long entry is
  token_count = len(encoding.encode(combined_content))
     

     

#dont run if its beyond the limit of the model
  if token_count > MAX_TOKEN_LIMIT:
    combined_halves = []

    split_halfway = [combined_content[len(combined_content)//2:], combined_content[:len(combined_content)//2]]

    for all_content in split_halfway:
       
      completion = client.chat.completions.create(
      #cheapest model (shouldnt need more than this)
        model="gpt-4o-mini",
        messages=[
          {"role": "system", "content": "You are a Data Cleaner. Based on the user input of text, please extract the place name, price and description of services and upload it in an organized manner to a txt file."},
          {"role": "user", "content": all_content}
        ]
      )

      combined_halves.append(completion)

        
        #print(f"Skipping input: {token_count} tokens exceed the limit of {MAX_TOKEN_LIMIT} tokens.")
  else:
    combined_halves = []

    completion = client.chat.completions.create(
      #cheapest model (shouldnt need more than this)
      model="gpt-4o-mini",
      messages = [ 
         
        {"role": "system",
        "content": "Please provide the data of what is being asked next line in the following JSON format:{\n    \"School Name\": {\n        \"Prices\": [\n            {\n                \"Name\": \"Package #1 (E-Learning)\",\n                \"Price\": \"$579 + Tax\"\n            },\n            {\n                \"Name\": \"Package #2 (E-Learning)\",\n                \"Price\": \"$739 + Tax\"\n            }\n        ]\n    }\n}\n"},

        {"role": "system", "content": "Please extract the name of the website/place, all its prices, description of each price and return ONLY and ONLY organized data, no extra spaces or lines, no other completion message"},
        {"role": "user", "content": combined_content}
      ],
    )
    combined_halves.append(completion)

except OpenAIError as e:
  # Handle specific API errors
    if e.http_status == 402: 
        print("Error: Insufficient funds. Please top up your account.")
    else:
        print(f"An error occurred: {e}")

except Exception as e:
    # Handle any other exceptions
    print(f"An unexpected error occurred: {e}")

if completion:

  for final_result in combined_halves:

    print("--------------------------------------------------------------------------------------------------------------------")

    print(final_result.choices[0].message.content)

    response_content = final_result.choices[0].message.content

    # Check if response_content is empty
    if not response_content.strip():
        print("The response content is empty.")
        continue  # Skip to the next iteration if content is empty

        # Try parsing the content as JSON
    try:
        data = json.loads(response_content)
        print("JSON parsed successfully.")
        # Optionally save it to a file
        with open('data.json', 'w') as file:
            json.dump(data, file, indent=4)
        print("Data successfully saved to 'data.json'.")


    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print("Raw content:", response_content)



else:
   print("Could Not find Prices")