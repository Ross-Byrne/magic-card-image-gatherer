import pprint
import requests
import json
import os.path
import pandas as pd
from pandas import json_normalize


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def initialise_data_folder():
    if not os.path.exists('data'):
        os.makedirs('data')


# Get all card info from scyfall.com
# See: https://scryfall.com/docs/api/bulk-data
def fetch_card_data():
    print("Querying Scryfall bulk api...")
    response = requests.get("https://api.scryfall.com/bulk-data")
    bulk_data_json = response.json()
    data = bulk_data_json["data"]
    selected_obj = None

    # get all english cards using type: "default_cards"
    for obj in data:
        if obj["type"] == "default_cards":
            selected_obj = obj

    if selected_obj is None:
        print('An error occurred, cannot find default cards object')
    else:
        selected_id = selected_obj['id']
        file_name = f"default-cards-{selected_id}"

        # Check if file already exists
        exists = os.path.exists(f"data/{file_name}.json")

        if exists is True:
            print("JSON file already exists...")
        else:
            download_uri = selected_obj["download_uri"]
            cards_response = requests.get(download_uri)

            print("Saving Card JSON to file...")
            with open(f"data/default-cards-{selected_id}.json", 'w') as file:
                json.dump(cards_response.json(), file, indent=4)
                print("File saved")

        print("Finished processing default card json")


def main():
    initialise_data_folder()
    fetch_card_data()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
