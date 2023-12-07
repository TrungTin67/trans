import json
import csv
import re
import os

def check_output_folder(output_folder):
    out = output_folder + "/Final_CIS_report"
    try:
        os.mkdir(out)
        return out
    except FileExistsError:
        print(f"Folder '{output_folder}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_json_file(file_path):
    with open(file_path, 'rb') as json_file:
        data = json.load(json_file)
    return data
def format_summary(summary):
    formatted_summary = summary
    formatted_summary = formatted_summary.replace("\n", " ")
    formatted_summary = re.sub(r'Expected\s+<int>\s*:\s*(\d+)\s+to equal\s+<int>\s*:\s*(\d+)', r'Expected int: \1 to equal int: \2', formatted_summary)
    return formatted_summary

def csv_report(json_files,output_folder_path,input_folder_path):
    for json_file in json_files:
        fname = json_file.split(".json")[0]
        csv_filename = check_output_folder(output_folder_path) + "/" + fname + ".csv"
        json_file_path = os.path.join(input_folder_path, json_file)
        data = read_json_file(json_file_path)

        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['title', 'resource-id', 'property', 'expected', 'found', 'result', 'summary-line']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for result in data['results']:
                writer.writerow({
                    'title': result['title'],
                    'resource-id': result['resource-id'],
                    'property': result['property'],
                    'expected': ', '.join(result['expected']) if result['expected'] else '',
                    'found': ', '.join(result['found']) if result['found'] else '',
                    'result': result['result'],
                    'summary-line': format_summary(result['summary-line'])
                })

def sumarize_report(json_files,output_folder_path,input_folder_path):
    csv_filename = output_folder_path + "/Report_Summarize.csv"
    with open(csv_filename, 'w', newline='') as csvfile:
        for json_file in json_files:
            json_file_path = os.path.join(input_folder_path, json_file)
            data = read_json_file(json_file_path)
            server = json_file.split(".json")[0]
            fieldnames = ['Server', 'Test count', 'Success', 'Fail']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            writer.writerow({
                'Server': server,
                'Test count': data['summary']['test-count'],
                'Pass': int(data['summary']['test-count']) - int(data['summary']['failed-count']),
                'Fail': data['summary']['failed-count']
            })

    print(f'CSV file "{csv_filename}" created successfully.')

def main():
    print("Please input path of report json:")
    input_folder_path = input()
    if len(input_folder_path) <=0:
        input_folder_path = "/home/audit/CIS_with_Ansible/CIS_report"
    print("Please input path of report csv output:")
    output_folder_path = input()
    if len(output_folder_path) <=0:
        output_folder_path = "/home/audit/CIS_with_Ansible"

    json_files = [file for file in os.listdir(input_folder_path) if file.endswith('.json')]

    csv_report(json_files,output_folder_path,input_folder_path)

    sumarize_report(json_files,output_folder_path,input_folder_path)

    print(f'Report Summarize has created in {output_folder_path} \nReport CSVs have created {output_folder_path}/Final_CIS_report')

if __name__ == "__main__":
    main()