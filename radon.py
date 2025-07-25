import argparse
import csv
import ftlabs_file_parser
import glob
import math
import pathlib
import statistics

arg_parser = argparse.ArgumentParser("radon")
arg_parser.add_argument("path", help="Path to export files", type=str)
args = arg_parser.parse_args()

file_parser = ftlabs_file_parser.RD200Parser()

path_pattern=pathlib.Path(args.path).joinpath('*.txt')
all_results = {}
for source_file_path in (glob.glob(str(path_pattern.resolve()))):
    print(f'Processing {source_file_path}')
    try:
        result = file_parser.parse_file(source_file_path)
        for data_point in result.data_points:
            if data_point.time not in all_results:
                all_results[data_point.time] = []
            all_results[data_point.time].append(int(data_point.value))
    except Exception as e:
        print(f'Unable to parse file: {e}')

sum=0
count=0

with open('averages.csv', 'w+') as avg_file:
    with open('output.csv', 'w+') as csv_file:
        csvwriter = csv.writer(csv_file)
        avgwriter = csv.writer(avg_file)
        for key, value in sorted(all_results.items()):
            average_value = math.ceil(statistics.fmean(value))
            sum += average_value
            count += 1
            output = [key]
            output.append(average_value)
            output.extend(value)
            csvwriter.writerow(output)
            output = [key, average_value]
            avgwriter.writerow(output)


print(f'Average level: {math.ceil(sum/count)}')
