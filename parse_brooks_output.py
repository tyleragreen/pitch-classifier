import argparse
from pathlib import Path

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description='Process a table of pitch data from Brook\'s Baseball.')
parser.add_argument('file_name', type=str, help='Path of raw table.')
args = parser.parse_args()

path = Path(args.file_name)

with open(path, 'r') as f:
    raw_html = f.read()

html = BeautifulSoup(raw_html, 'html.parser')

headers = [ header.string for header in html.findAll('th')]
tds = [[ data.string for data in row.findAll('td') ] for row in html.findAll('tr')]
tds = [ td for td in tds if len(td) > 0 ]

records = [ dict(zip(headers, row)) for row in tds ]

output_fields = ['start_speed', 'pfx_x', 'pfx_z', 'mlbam_pitch_name']
with open(f"{'/'.join(path.parts[:-1])}/{path.stem}.csv", 'w') as f:
    f.write(','.join(output_fields))
    f.write('\n')

    for record in records:
        fields = [ record[field] for field in output_fields]
        f.write(','.join(fields))
        f.write('\n')
