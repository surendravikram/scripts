import csv

list_files = ["SRWM01.txt", "SRW01.txt", "SRW02.txt", "SSW01.txt", "SSW02.txt"]

dialect = csv.excel
dialect.delimiter = '\t'
final_dict = {}
all_drug_classes = set()
for file_name in list_files:
    with open(file_name, encoding='utf-8', newline='') as in_file:
        headings = in_file.readline().strip('\n').split(dialect.delimiter)
        rgi_reader_dict = csv.DictReader(in_file, dialect=dialect, fieldnames=headings)
        drug_class = []
        drug_class1 = []
        out_dict = {}
        for row in rgi_reader_dict:
            for key, value in row.items():
                if key == 'Drug Class':
                    drug_class.append(row['Drug Class'])
        [drug_class1.extend(i.split('; ')) for i in drug_class]
        all_drug_classes.update(drug_class1)
        for item in set(drug_class1):
            out_drug_class = []
            class_count = drug_class1.count(item)
            # out_drug_class.extend(counter)
            out_dict.update({item:class_count})
        final_dict[file_name] = out_dict

# print(out_dict)
print(final_dict)

all_drug_classes = sorted(all_drug_classes)
output_file = 'drug_class_counts_per_file.csv'
headers = ['Drug Class'] + list(list_files)
print(headers)

# Write to the CSV using DictWriter
with open(output_file, mode='w', encoding='utf-8', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers, delimiter='\t')

    # Write the header row
    writer.writeheader()

    # For each drug class, write its count in each file's column
    for drug_class in all_drug_classes:
        row = {'Drug Class': drug_class}

        # For each file, check if the drug class is present and add the count (or 0 if not)
        for file_name in list_files:
            row[file_name] = final_dict.get(file_name, {}).get(drug_class, 0)

        # Write the row
        writer.writerow(row)

print(f"\nData written to {output_file}")