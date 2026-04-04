#!/usr/bin/env python3

import csv
import io
import pathlib
import re
import sys


def main() -> int:
    if len(sys.argv) != 5:
        print('Usage: create-team.py <team_handle> <team_fqdn> <team_description> <members_csv_lines>', file=sys.stderr)
        return 64

    handle, fqdn, desc, csv_lines = sys.argv[1:5]

    if not handle:
        print('Error: team_handle required', file=sys.stderr)
        return 64
    if not fqdn:
        print('Error: team_fqdn required', file=sys.stderr)
        return 64

    if not re.fullmatch(r'[A-Za-z0-9]{2,4}', handle):
        print('Error: team_handle must be 2-4 alphanumeric characters', file=sys.stderr)
        return 1

    target_dir = pathlib.Path('teams') / 'active' / handle
    existing_matches = [path for path in pathlib.Path('teams').glob(f'*/*/{handle}') if path.is_dir()]
    if existing_matches:
        print(f"Error: Team handle '{handle}' already exists", file=sys.stderr)
        return 1

    target_dir.mkdir(parents=True, exist_ok=False)

    rows = []
    reader = csv.reader(io.StringIO(csv_lines))
    for line_number, row in enumerate(reader, start=1):
        if not row or all(not cell.strip() for cell in row):
            continue
        if len(row) != 4:
            print(f'Error: CSV row {line_number} must have exactly 4 columns', file=sys.stderr)
            return 1
        discord_name, vrc_name, runstyle, role = (cell.strip() for cell in row)
        if not discord_name or not vrc_name or not runstyle or not role:
            print(f'Error: CSV row {line_number} contains an empty field', file=sys.stderr)
            return 1
        try:
            role_value = int(role)
        except ValueError:
            print(f'Error: CSV row {line_number} role must be an integer', file=sys.stderr)
            return 1
        if role_value < 0:
            print(f'Error: CSV row {line_number} role must be >= 0', file=sys.stderr)
            return 1
        rows.append([discord_name, vrc_name, runstyle, str(role_value)])

    if not rows:
        print('Error: At least one member row is required', file=sys.stderr)
        return 1

    members_path = target_dir / 'members.csv'
    with members_path.open('w', newline='') as file_handle:
        writer = csv.writer(file_handle)
        writer.writerow(['discord_name', 'vrc_name', 'runstyle', 'role'])
        writer.writerows(rows)

    metadata_path = target_dir / 'metadata.yaml'
    with metadata_path.open('w', encoding='utf-8', newline='\n') as file_handle:
        file_handle.write(f'team_handle: {handle}\n')
        file_handle.write(f'team_fqdn: {fqdn}\n')
        file_handle.write('team_icon_url: ./icon.png\n')
        file_handle.write('team_blurb: |-\n')
        blurb_lines = desc.splitlines() or ['']
        for line in blurb_lines:
            file_handle.write(f'  {line}\n')

    print(f'Files generated successfully in {target_dir}')
    print('members.csv')
    print('metadata.yaml')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())