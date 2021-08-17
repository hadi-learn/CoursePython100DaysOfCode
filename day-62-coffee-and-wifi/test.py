import csv


with open('cafe-data.csv', newline='') as csv_file:
    print(csv_file)
    csv_data = csv.reader(csv_file, delimiter=',')
    print(csv_data)
    list_of_rows = []
    for row in csv_data:
        print(row)
        list_of_rows.append(row)
    print(list_of_rows)
    total_cafe = len(list_of_rows)
    print(total_cafe)
    print(type(total_cafe))
    total_aspect = len(list_of_rows[0])
    print(total_aspect)
