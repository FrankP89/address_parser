'''
Example inputs:
121 N La Salle St #905, Chicago, IL 60602
Eiffel Tower, Paris, France
Rome
Chiangmai
123
dfhgidlbfkjnklagmdhu
'''

import guidance
from guidance import system, user, assistant, gen
from openai import OpenAI
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
# import openai


# client = OpenAI()
OPENAI_API_KEY = ''
client = OpenAI(api_key = OPENAI_API_KEY)

# openai.api_key = OPENAI_API_KEY
# add openai key to guidance
# guidance.set_openai_key(OPENAI_API_KEY)
model_name = "gpt-4"

# def text2location(address:str): 
#     if (address != None):      
#         trigger_prompt = address
#         format = ''' `json
#         {   city : "",
#             state: "",
#             country: ""
#         }
# `
# '''
#         guard_rail = "If the user does not provide all the information, do NOT fill it out"

#         prompt = f"Convert the following address to structured data: {format}" + address


#         llm = guidance.models.OpenAI(model_name, api_key=OPENAI_API_KEY)

#         with system():
#             lm = llm + "You are a system that converts human given addresses to readable structured data."

#         with user():
#             prompt_to_analyze = prompt

#             lm = lm + f"Follow the guardrail: {guard_rail} line by line. You can get penalized for not following it."
#             lm = lm + f"Read the {trigger_prompt}. Give only the address in the following format {format}. Do not give explanations. Comment: Return only the json response."

#         with assistant():
#             lm = lm + gen('answer_rating', temperature=0.1, max_tokens=50)

#         # Execute the guidance program
#         executed_program = lm

#         # Extract the structured data from the response
#         structured_data = executed_program['answer_rating']

#         print(structured_data)

#         # Extract the city, state, and country from the location object


#         # location = Location(city=city, state=state, country=country)


#         # print(executed_program)

#         # return location
    

address = "121 N La Salle St #905, Chicago, IL 60602"
address = "123"
all_addresses = [
    "121 N La Salle St #905, Chicago, IL 60602",
    "Eiffel Tower, Paris, France",
    "Rome",
    "Chiangmai",
    "123",
    "dfhgidlbfkjnklagmdhu"
]

class Location(BaseModel):
    city: str
    state: str
    country: str



def text2location(address:str):


    # for address in all_addresses:
    print("address", address)
    
    guard_rail = '''If the user does not provide all the information, do NOT fill it out.
                    If the information is wrong, leave it blank.
                    If the information is not in the correct format, leave it blank.
                    If the information is not in the correct format, leave it blank.
                    If the country is not provided, leave it blank.
                    If the state is not provided, leave it blank.
                    If the city is not provided, leave it blank.    
                '''
    # Call the completion function
    completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are a system that converts human given addresses to readable structured data."},
        {"role": "user", "content": f"Give only the address {address}"},
        {"role": "user", "content": f"Follow the guardrail: {guard_rail} line by line. You can get penalized for not following it."},
        {"role": "assistant", "content": f"Generate the address."},
    ],
    response_format=Location,
    )

    event = completion.choices[0].message.parsed

    # print(event)

    return event


# Call the Thread Pool Executor to invoke the translation (if needed) of the headers
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(text2location, human_address) for human_address in all_addresses]

    # Immediately check for exceptions
    for future in as_completed(futures):
        try:
            future.result()  # This will re-raise any exceptions
        except Exception as e:
            raise(f"An error occurred: {e}")
        
    
    # Wait for all the futures to complete
    wait(futures)
    # Extract the results
    results = [future.result() for future in futures]

    # Print the results
    for result in results:
        print(result)
                