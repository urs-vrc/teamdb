#!/usr/bin/env python3

import csv
import io
import json
import pathlib
import sys


def yaml_double_quoted(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


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

    if not 2 <= len(handle) <= 4:
        print('Error: team_handle must be 2-4 characters', file=sys.stderr)
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
        file_handle.write(f'team_handle: {yaml_double_quoted(handle)}\n')
        file_handle.write(f'team_fqdn: {yaml_double_quoted(fqdn)}\n')
        file_handle.write(f'team_icon_url: {yaml_double_quoted("./icon.png")}\n')
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