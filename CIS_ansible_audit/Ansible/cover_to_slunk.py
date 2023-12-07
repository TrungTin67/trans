import json
import ndjson
import os

def read_json_file(file_path):
    with open(file_path, 'rb') as json_file:
        data = json.load(json_file)
    return data

def cover(json_files,folder_path):
    for json_file in json_files:
        json_file_path = os.path.join(folder_path, json_file)
        data = read_json_file(json_file_path)
        with open(json_file_path, 'w') as f:
            writer = ndjson.writer(f, ensure_ascii=False)
            for result in data['results']:
                writer.writerow(result)

def main():
    print("Please input path of report json:")
    folder_path = input()
    if len(folder_path) <=0:
        folder_path = "/home/audit/CIS_with_Ansible/CIS_report"

    json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]

    cover(json_files,folder_path)

    print(f'Cover Completed')

if __name__ == "__main__":
    main()