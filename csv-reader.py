import csv
import argparse

def extract_columns(file_paths, columns):
    extracted_data = {column: [] for column in columns}
    for file_path in file_paths:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                for column in columns:
                    value = row.get(column, "")
                    extracted_data[column].append(value)
    return extracted_data

def format_output(extracted_data, columns):
    column_widths = {column: max(len(column), max((len(value) for value in values), default=0)) for column, values in extracted_data.items()}
    headers = " | ".join(f"{column.center(column_widths[column])}" for column in columns)

    rows = []
    num_rows = max(len(values) for values in extracted_data.values())
    for i in range(num_rows):
        row = " | ".join(f"{(extracted_data[column][i] if i < len(extracted_data[column]) else '').ljust(column_widths[column])}" for column in columns)
        rows.append(row)
    
    # Calculate
    divider_length = sum(column_widths[column] for column in columns) + (len(columns) - 1) * 3 + 4
    divider = "-" * divider_length
    
    return divider, headers, divider, rows

def main():
    parser = argparse.ArgumentParser(description='CSV Reader to extract specific columns.')
    parser.add_argument('-f', '--files', nargs='+', required=True, help='CSV file paths')
    parser.add_argument('-sc', '--show-columns', action='store_true', help='Show columns present in the file')
    parser.add_argument('-c', '--columns', nargs='+', required=False, help='Columns to extract')
    parser.add_argument('-o', '--output', help='Output file path')

    args = parser.parse_args()

    if args.show_columns:
        unique_columns = set()
        for file_path in args.files:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                unique_columns.update(reader.fieldnames)
        print("Columns present in the selected files:")
        print("\n".join(unique_columns))
    else:
        if not args.columns:
            print("Please specify columns to extract using the -c or --columns option.")
            return

        extracted_data = extract_columns(args.files, args.columns)
        
        divider, headers, divider, rows = format_output(extracted_data, args.columns)
        
        output_lines = [divider, "| " + headers + " |", divider] + ["| " + row + " |" for row in rows]

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as output_file:
                output_file.write("\n".join(output_lines) + "\n" + divider)
        print("\n".join(output_lines))
        print (divider)

if __name__ == "__main__":
    main()
