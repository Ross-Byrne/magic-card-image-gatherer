import pprint
import requests
import json
import os
import pandas as pd

data_dir = f"{os.getcwd()}/data"


def jprint(obj):
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
        if os.path.exists(f"{data_dir}/{file_name}.json") is True:
            print("JSON file already exists...")
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

        print("Finished processing default card json")


# Iterate through card json and download card images
def download_card_images(file_name):
    print("Starting to download Card Images...")


def main():
    # Create data folder
    if not os.path.exists('data'):
        os.makedirs('data')

    fetch_card_data()
    print("")

    file_name = get_card_json_from_file()
    if file_name is None:
        print("Error finding json file")
        return

    # Stream json from file and start collecting card images
    download_card_images(file_name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
