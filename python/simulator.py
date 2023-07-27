from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt


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


# Load Contracts
# -------------------------------------------
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

# Calculate Remaining Balance
# --------------------------------------

def remaining_balance(principal, annual_interest_rate, monthly_payment, months_paid):
    monthly_interest_rate = (annual_interest_rate) / 12  # Convert annual interest rate to a monthly rate
    balance = principal

    for _ in range(months_paid):
        # Calculate the interest for the current month
        interest = balance * monthly_interest_rate
        
        # Deduct the payment from the balance, taking into account the interest
        balance = balance - (monthly_payment - interest)

        # If balance is less than 0, set it to 0
        balance = max(balance, 0)

    return balance

# print(remaining_balance(12000, 0.20, 200, 12))  # example calculation for interest-only

# Calculate the number of months between two datetime objects
# ---------------------------------------------------------------------
def months_between(date1, date2):
    # Ensure date1 is always the smaller (earlier) datetime
    if date1 > date2:
        date1, date2 = date2, date1

    months = (date2.year - date1.year) * 12 + date2.month - date1.month

    # If the day of the month of the earlier date is greater than the day of the month of the later date, subtract one month
    if date1.day > date2.day:
        months -= 1

    return months



# Calculate Payment
# -------------------------------------------
def calculate_payment(data_dict, date_prime):
    contract = data_dict.get("Contract")

    if contract == "Note":

        principal = float( data_dict.get("Principal") )
        note_type = data_dict.get("Note Type")
        interest = percentage_to_number( data_dict.get("Interest") )

        if note_type.lower() == "interest-only":
            monthly_payment = (interest * principal) / 12
        else:
            monthly_payment = float( data_dict.get("Monthly Payment") )

        contract_start_date =  datetime.strptime( data_dict.get('Start'), '%m/%d/%Y')
        contract_end_date =  datetime.strptime( data_dict.get('End'), '%m/%d/%Y')
        if date_prime ==  contract_end_date:
            total_payments = months_between(contract_start_date, contract_end_date)
            return remaining_balance(principal, interest, monthly_payment, total_payments)
        elif (date_prime <= contract_end_date) and (date_prime >= contract_start_date):
            return monthly_payment
        else:
            return 0
    else:
        contract_start_date =  datetime.strptime( data_dict.get('Start'), '%m/%d/%Y')
        if data_dict.get('End') == None:
            contract_end_date =  datetime.strptime( '12/31/9999', '%m/%d/%Y')
        else:
            contract_end_date =  datetime.strptime( data_dict.get('End'), '%m/%d/%Y')
        if (date_prime < contract_end_date) and (date_prime > contract_start_date):
            monthly_payment = float( data_dict.get("Monthly Payment") )
            return monthly_payment
        else:
            return 0

    return None




accounts = {}
for node in nodes:
    accounts[node] = 0


start_date_input = input("Enter the start date (MM/DD/YYYY): ")
date_prime = datetime.strptime(start_date_input, '%m/%d/%Y')



# calculate flow
# ---------------------------------------

import pandas as pd



simulation_length_days = int( input('Simulation length (days):') )

sources = []
destinations = []
monthly_payments = []


# calculate cashflow:
import calendar

flow_data = []


days_in_month = calendar.monthrange(date_prime.year, date_prime.month)[1]
first_day_of_month = datetime(date_prime.year, date_prime.month, 1)
for i in range(days_in_month):
    current_date = first_day_of_month + timedelta(days=i)
    for contract in contracts:
        if contract['Payout Day'] == current_date.day:
            sources.append(contract['Source'])
            destinations.append(contract['Destination'])
            monthly_payments.append( calculate_payment(contract, current_date) )
        
            flow_data.append( {'Source': contract['Source'], 'Destination': contract['Destination'], 'Monthly Payment': round( calculate_payment(contract, date_prime) , 2 ) } )


data = {'Source': sources,
        'Destination': destinations,
        'Monthly Payment': monthly_payments,
        }

data = flow_data

df = pd.DataFrame(data)
with open('../flow.yaml', 'w') as file:
            yaml.dump(data, file)

print('Inputs')
print('------------------')
for key, value in accounts.items():
    print(f"{key}: {value:.2f}") 

print('\n\n\n')



account_state = [list(accounts.values())]

for idx in range(simulation_length_days):
    for contract in contracts:
        if contract['Payout Day'] == date_prime.day:
            
            accounts[ contract['Source'] ] -= calculate_payment(contract, date_prime)
            accounts[ contract['Destination'] ] += calculate_payment(contract, date_prime)

            account_state.append(list(accounts.values())) # note: verify that this appends in the right order (same as labels later)

    date_prime = date_prime + timedelta(days=1)

account_state = np.transpose(account_state)

print('Outputs')
print('------------------')
for key, value in accounts.items():
    print(f"{key}: {value:.2f}") 

plt.figure()
listed = list(accounts.keys())
print(listed)
idx = np.squeeze(np.where(np.array(list(accounts.keys())) == '8SC'))
print('idx:'+str(idx))
plt.plot(account_state[idx])
plt.show()



#import subprocess
#subprocess.run(["node", "../server.js"], check=True)

