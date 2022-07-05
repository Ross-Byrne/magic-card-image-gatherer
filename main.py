import pprint
import requests
import json
import os
import pandas as pd

data_dir = f"{os.getcwd()}/data"


def print_json(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


# Removes old versions of downloaded json file
def clean_data_directory(new_file_name):
    # scan data directory for files
    with os.scandir(data_dir) as dirs:
        for entry in dirs:
            # remove file if new file
            if entry.name != f"{new_file_name}.json":
                print(f"Removing file: {entry.name}...")
                try:
                    os.remove(f"{data_dir}/{entry.name}")
                except OSError as e:  # if failed, report it back to the user
                    print("Error: %s - %s." % (e.filename, e.strerror))


# Look at files in data directory and fine json file
def get_card_json_from_file():
    json_file_name = None

    # scan data directory for files
    with os.scandir(data_dir) as dirs:
        for entry in dirs:
            # remove file if new file
            if "default-cards-" in entry.name:
                json_file_name = entry.name
    return json_file_name


# Get all card info from scyfall.com
# See: https://scryfall.com/docs/api/bulk-data
def fetch_card_data():
    print("Querying Scryfall bulk api...")
    response = requests.get("https://api.scryfall.com/bulk-data")
    bulk_data_json = response.json()
    data = bulk_data_json["data"]
    selected_obj = None
    cards_json = []

    # get all english cards using type: "default_cards"
    for obj in data:
        if obj["type"] == "default_cards":
            selected_obj = obj

    if selected_obj is None:
        print('An error occurred, cannot find default cards object')
    else:
        selected_id = selected_obj['id']
        file_name = f"default-cards-{selected_id}"
        file_path = f"{data_dir}/{file_name}.json"

        # Check if file already exists
        if os.path.exists(file_path) is True:
            print("File already exists...")
        else:
            print("Querying all cards api...")
            download_uri = selected_obj["download_uri"]
            cards_response = requests.get(download_uri)
            cards_json = cards_response.json()

            print("Saving Card JSON to file...")
            with open(f"{data_dir}/default-cards-{selected_id}.json", 'w') as file:
                json.dump(cards_json, file, indent=4)
                print("File save complete...")

        # Cleanup old files
        clean_data_directory(file_name)

        print("Finished processing default card json...")
        return file_path


# Sanitise card json data to remove unused values
def sanitise_card_data(file_path):
    cards_json = []
    print("Loading json from file...")
    try:
        with open(file_path) as file:
            cards_json = json.load(file)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    print(f"Total Unprocessed Cards: {len(cards_json)}")
    print("Sanitising json data...")
    data = []

    for card in cards_json:
        if "id" in card.keys() and "image_uris" in card.keys():
            sanitised_card = {"id": card["id"], "image_uri": card["image_uris"]["normal"]}

            # Only add cards with IDs and Image URIs
            if len(sanitised_card["id"]) > 0 and len(sanitised_card["image_uri"]) > 0:
                data.append(sanitised_card)
    return data


# Iterate through card json and download card images
def download_card_images(sanitised_data):
    print(f"Total Cards: {len(sanitised_data)}")
    print("Starting to download Card Images...")

    # rate limit download by 100ms per request
    

def main():
    # Create data folder
    if not os.path.exists('data'):
        os.makedirs('data')

    json_file_path = fetch_card_data()
    sanitised_data = sanitise_card_data(json_file_path)
    download_card_images(sanitised_data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
