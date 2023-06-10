import requests
from tqdm import tqdm
import os
from notify import send_notification

# Read the links from list.txt
with open('list.txt', 'r') as file:
    links = file.read().splitlines()

# List to store the names of deceased persons
deceased_persons = []

# Iterate over each link with a progress bar
with tqdm(total=len(links), desc='Checking deaths') as pbar:
    for link in links:
        response = requests.get(link)
        content = response.text

        # Check if the person has died based on category
        if '2023 deaths' in content or 'Gestorben 2023' in content:
            # Extract the name from the link
            name = link.split('/')[-1].replace('_', ' ')
            deceased_persons.append(name)

        pbar.update(1)

# Read the previously checked deceased persons from died.txt if it exists
previous_deaths = []
if os.path.isfile('died.txt'):
    with open('died.txt', 'r') as file:
        previous_deaths = file.read().splitlines()

# Find new deaths by comparing with previously checked deaths
new_deaths = list(set(deceased_persons) - set(previous_deaths))

# Print the list of deceased persons
print("Deceased Persons:")
for person in deceased_persons:
    print(person)

# Print the list of new deaths
print("\nNew Deaths:")
for person in new_deaths:
    print(person)
    send_notification(f"New Death: {person}")

# Write the current deceased persons to died.txt
with open('died.txt', 'w') as file:
    for person in deceased_persons:
        file.write(person + '\n')

# Print the status bar
status = f"Checked: {len(links)} | Deceased: {len(deceased_persons)} | New Deaths: {len(new_deaths)}"
print(status)
