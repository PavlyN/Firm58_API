import requests
import re
from dotenv import load_dotenv
import os

load_dotenv()
session = requests.Session()

# Step 1: Login
login_data = {
    "j_username": os.getenv("USERNAME"),
    "j_password": os.getenv("PASSWORD"),
}

def guzmanExtract():
    login_response = session.post("https://guzman.firm58.com/j_spring_security_check", data=login_data)
    if login_response.status_code == 200:
        # print("Login successful")

        # Step 2: Make the target request with GWT permutation header
        target_url = "https://guzman.firm58.com/firm58ui/service/errorService"
        headers = {
            "Content-Type": "text/x-gwt-rpc; charset=UTF-8",
            "Accept": "*/*",
            "Origin": "https://guzman.firm58.com",
            "Referer": "https://guzman.firm58.com/main.do",
            "X-GWT-Module-Base": "https://guzman.firm58.com/firm58ui/",
            "X-GWT-Permutation": os.getenv("GWT-PERM"),  # Replace with your actual x-gwt-permutation value
        }
        
        payload = r"7|0|15|https://guzman.firm58.com/firm58ui/|07A0072F8C81AED48CB38DD283C8F555|com.firm58.web.gwt.error.client.ErrorRPCService|searchErrorSummary|com.sencha.gxt.data.shared.loader.FilterPagingLoadConfig|com.sencha.gxt.data.shared.loader.FilterPagingLoadConfigBean/3633305154|java.util.ArrayList/4159755760|com.sencha.gxt.data.shared.loader.FilterConfigBean/3253615692|sc|last_modified_date\!dr\!Month%20to%20Date|ao|and|com.sencha.gxt.data.shared.SortInfoBean/1820471044|com.sencha.gxt.data.shared.SortDir/317895740|category|1|2|3|4|1|5|6|7|2|8|0|9|0|10|8|0|11|0|12|250|0|7|1|13|14|0|15|"
        response = session.post(target_url, headers=headers, data=payload)
    else:
        print("Login failed")
    return response

def pershingExtract():
    login_response = session.post("https://pershing3.firm58.com/j_spring_security_check", data=login_data)
    if login_response.status_code == 200:
        # print("Login successful")

        # Step 2: Make the target request with GWT permutation header
        target_url = "https://pershing3.firm58.com/firm58ui/service/errorService"
        headers = {
            "Content-Type": "text/x-gwt-rpc; charset=UTF-8",
            "Accept": "*/*",
            "Origin": "https://pershing3.firm58.com",
            "Referer": "https://pershing3.firm58.com/main.do",
            "X-GWT-Module-Base": "https://pershing3.firm58.com/firm58ui/",
            "X-GWT-Permutation": os.getenv("GWT-PERM"),  # Replace with your actual x-gwt-permutation value
        }
        
        payload = r"7|0|15|https://pershing3.firm58.com/firm58ui/|07A0072F8C81AED48CB38DD283C8F555|com.firm58.web.gwt.error.client.ErrorRPCService|searchErrorSummary|com.sencha.gxt.data.shared.loader.FilterPagingLoadConfig|com.sencha.gxt.data.shared.loader.FilterPagingLoadConfigBean/3633305154|java.util.ArrayList/4159755760|com.sencha.gxt.data.shared.loader.FilterConfigBean/3253615692|sc|last_modified_date\!dr\!Month%20to%20Date|ao|and|com.sencha.gxt.data.shared.SortInfoBean/1820471044|com.sencha.gxt.data.shared.SortDir/317895740|category|1|2|3|4|1|5|6|7|2|8|0|9|0|10|8|0|11|0|12|250|0|7|1|13|14|0|15|"
        response = session.post(target_url, headers=headers, data=payload)
    else:
        print("Login failed")
    return response

customer = int(input("Pershing3:1 , Guzman:2\n"))
if customer ==1:
    response = pershingExtract()
elif customer ==2:
    response = guzmanExtract()
else:
    print("Invalid input")
    exit()
1
# print(response.status_code)
# print(response.text)

# Extract the response content as text
response_text = response.text

# Remove the '//OK' prefix if present
if response_text.startswith('//OK'):
    response_text = response_text[4:]

# Remove the array of strings (type information)
start_array = response_text.find('["')
end_array = response_text.find(']', start_array) + 1
if start_array != -1 and end_array != -1:
    response_without_strings = response_text[:start_array] + response_text[end_array:]
else:
    response_without_strings = response_text

# Extract all numbers from the response
numbers = re.findall(r'-?\d+', response_without_strings)
numbers = list(map(int, numbers))

# Define the mapping from category IDs to names
category_id_to_name = {
    -7: 'Other',
    10: 'Required Rate Missing',
    9: 'Duplicate Trade',
    8: 'Asset Not Found',
    7: 'Ambiguous Asset',
    6: 'Account Not Found',
}

# Find indices where category IDs occur
category_ids = set(category_id_to_name.keys())
indices = [i for i, num in enumerate(numbers) if num in category_ids]

# Split the numbers into segments for each category
segments = []
for i in range(len(indices)):
    start = indices[i]
    end = indices[i + 1] if i + 1 < len(indices) else len(numbers)
    segments.append(numbers[start:end])

# print(segments)

# Categories of interest
if customer==1: categories_of_interest = [10, 8, 7]
else: categories_of_interest = [8, 7]

# Process the segments
for segment in segments:
    if customer==2: categories_of_interest
    category_id = segment[0]
    if category_id in categories_of_interest:
        category_name = category_id_to_name.get(category_id, 'Unknown Category')
        if len(segment) > 3:
            value = segment[3]
            if (customer==2 and value == -6) or (customer==1 and value == -10):
                value = 0
            print(f"{category_name} -> New Errors: {value}")
        else:
            continue

