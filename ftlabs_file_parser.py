import collections
import pathlib
import re
from datetime import datetime, timedelta

Result = collections.namedtuple("Result", ["serial_number","model","data_points","location"])
DataPoint = collections.namedtuple("DataPoint", ["time","value"])

class RD200Parser:
    header_regex = re.compile(r"(?:FTLAB RADON DATA FILE|FTLab Radon Data)\n(?:MODEL NAME|Model Name)\:\s(.*)\nS\/N\:\s(.*)\nUnit:\s(.*)\nTime step:\s(\S*)(?:.*)\nData No\s?\:\s(\d*)")
    line_regex = re.compile(r"(\d+)\)\s+(\d+)")
    filename_regex = re.compile(r"(.*)_Log Data\s(.*)\.txt")
    date_format = re.compile(r"(\d+)[^a-zA-Z0-9]+(\d+)[^a-zA-Z0-9]+(\d+)[^a-zA-Z0-9]+(\d+)[^a-zA-Z0-9]+(\d+)")
    def parse_file(self,file_path: str) -> Result:
        with open(file_path) as source_file:
            file_name = pathlib.Path(file_path).name
            filename_match = self.filename_regex.match(file_name)

            if not filename_match:
                raise Exception("Unable to parse filename")

            location = filename_match.group(1)
            date = filename_match.group(2)

            if not self.date_format.match(date):
                raise Exception("Unable to parse date from filename")

            file_date = datetime.strptime(date, "%Y-%m-%d %H-%M")
            file_date = file_date.replace(minute=0) # the readings and save times just cause excessive precision and are useless

            file_lines = source_file.readlines()
            header_match = self.header_regex.match("".join(file_lines[:6]))

            if not header_match:
                raise Exception("Unable to match file header")
            
            if len(header_match.groups()) != 5:
                raise Exception("Invalid header format")
            
            data_point_count = int(header_match.group(5))

            data_points = []
            for file_line in file_lines[6:]:
                line_match = self.line_regex.match(file_line)
                reading_number = int(line_match.group(1))
                hours_ago = data_point_count - reading_number
                data_points.append(DataPoint(time=file_date + timedelta(hours=-1 * hours_ago),value=line_match.group(2)))
            if (data_point_count != len(data_points)):
                print(f'Expected {data_point_count} data points, actually got {len(data_points)}')

            return Result(
                data_points=data_points,
                location=location,
                model=header_match.group(1),
                serial_number=header_match.group(2),
                )

