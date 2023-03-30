#!/usr/bin/env python

import requests
from datetime import datetime
import sys


def handlerSubCustomer(_id, subscription_level):

    # Make an HTTP GET request to get the client data
    url = f"http://localhost:8010/api/v1/customerdata/{_id}/"
    response = requests.get(url)

    # Handle errors in the GET request
    if response.status_code != 200:
        print(
            f"Error getting customer data with ID{_id} ", response.status_code)
        return

    # Get the JSON object from the client
    customer_data = response.json()

    # Update required parameters based on subscription level
    if subscription_level == "free":
        customer_data["data"]["SUBSCRIPTION"] = "free"
        customer_data["data"]["ENABLED_FEATURES"] = {
            k: False for k in customer_data["data"]["ENABLED_FEATURES"]}
        customer_data["data"]["DOWNGRADE_DATE"] = datetime.now().strftime("%d/%m/%Y %H:%M")

    elif subscription_level == "basic":
        customer_data["data"]["SUBSCRIPTION"] = "basic"
        customer_data["data"]["ENABLED_FEATURES"] = {
            k: False for k in customer_data["data"]["ENABLED_FEATURES"]}
        customer_data["data"]["ENABLED_FEATURES"]["ENABLE_EDXNOTES"] = True
        customer_data["data"]["LAST_PAYMENT_DATE"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        customer_data["data"]["UPGRADE_DATE"] = datetime.now().strftime("%d/%m/%Y %H:%M")

    elif subscription_level == "premium":
        customer_data["data"]["SUBSCRIPTION"] = "premium"
        customer_data["data"]["ENABLED_FEATURES"]["INSTRUCTOR_BACKGROUND_TASKS"] = False
        customer_data["data"]["ENABLED_FEATURES"]["ENABLE_COURSE_DISCOVERY"] = False
        customer_data["data"]["UPGRADE_DATE"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    else:
        print(f"Error: Invalid subscription level. Must provide 'free', 'basic' or 'premium''.")
        return


    # Make an HTTP PUT request to update client data
    response = requests.put(url, json=customer_data)

    # Handle errors in the PUT request
    if response.status_code != 200:
        print(
            f"Error updating customer data with ID {_id}")
        return

    print(
        f"Successful subscription upgrade for ID customer {_id}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("You must provide the command ('downgrade' or 'upgrade'), client ID, and subscription level as arguments")
        sys.exit(1)

    command = sys.argv[1]
    _id = sys.argv[2]
    subscription_level = sys.argv[3]

    if command == "downgrade":
        handlerSubCustomer(_id, subscription_level)
    elif command == "upgrade":
        handlerSubCustomer(_id, subscription_level)
    else:
        print("invalid command. Use 'downgrade' o 'upgrade'")
        sys.exit(1)