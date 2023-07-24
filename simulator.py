from datetime import datetime, timedelta
import numpy as np



# read in yaml file
# ------------------------------------------------


import yaml


def get_unique_names(yaml_file):
    unique_names = set()

    with open(yaml_file, 'r') as file:
        contracts = yaml.safe_load(file)

        for contract in contracts:
            source = contract.get('Source')
            destination = contract.get('Destination')

            if source:
                unique_names.add(source)
            if destination:
                unique_names.add(destination)

    return list(unique_names)

yaml_file = 'contracts.yaml'
nodes = get_unique_names(yaml_file)

with open(yaml_file, 'r') as file:
    contracts = yaml.safe_load(file)


def percentage_to_number(percentage):
    try:
        # Remove any percentage sign or whitespace from the input string
        percentage = percentage.strip("%")

        # Convert the percentage string to a float and divide by 100
        number = float(percentage) / 100
        return number
    except ValueError:
        return None

def calculate_payment(data_dict):
    contract = data_dict.get("Contract")

    if contract == "Note":
        principal = float( data_dict.get("Principal") )
        note_type = data_dict.get("Note Type")
        interest = percentage_to_number( data_dict.get("Interest") )
        if note_type == "Interest-Only" and interest is not None and principal is not None:
            return (interest * principal) / 12
        else:
            monthly_payment = float( data_dict.get("Monthly Payment") )
            return monthly_payment
    else:
        monthly_payment = float( data_dict.get("Monthly Payment") )
        return monthly_payment

    return None




accounts = {}
for node in nodes:
    accounts[node] = 0


start_date_input = input("Enter the start date (MM/DD/YYYY): ")
date_prime = datetime.strptime(start_date_input, '%m/%d/%Y')



print('Inputs')
print('------------------')
for key, value in accounts.items():
    print(f"{key}: {value:.2f}") 

print('\n\n\n')

for idx in range(365):
    for contract in contracts:
        if contract['Payout Day'] == date_prime.day:
            #print('\n\n')
            #print( contract['Source'] )
            #print( contract['Destination'] )
            #print( calculate_payment(contract) )
            accounts[ contract['Source'] ] -= calculate_payment(contract)
            accounts[ contract['Destination'] ] += calculate_payment(contract)

    date_prime = date_prime + timedelta(days=1)

print('Outputs')
print('------------------')
for key, value in accounts.items():
    print(f"{key}: {value:.2f}") 
