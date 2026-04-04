#!/usr/bin/env python3

import csv
import io
import os
import pathlib
import re
import sys


def main() -> int:
    if len(sys.argv) != 6:
        print(
            'Usage: validate-workflow-input.py <team_handle> <team_fqdn> <team_description> <members_csv_lines> <submission_secret>',
            file=sys.stderr,
        )
        return 64

    handle, fqdn, desc, csv_lines, secret = sys.argv[1:6]

    team_submission_secret = os.environ.get('TEAM_SUBMISSION_SECRET')
    if team_submission_secret is None:
        print('TEAM_SUBMISSION_SECRET is required', file=sys.stderr)
        return 1

    if secret != team_submission_secret:
        print('Error: Invalid submission secret', file=sys.stderr)
        return 1

    if not re.fullmatch(r'[A-Za-z0-9]{2,4}', handle):
        print('Error: team_handle must be 2-4 alphanumeric characters', file=sys.stderr)
        return 1

    if not fqdn.strip():
        print('Error: team_fqdn is required', file=sys.stderr)
        return 1

    existing_matches = [path for path in pathlib.Path('teams').glob(f'*/*/{handle}') if path.is_dir()]
    if existing_matches:
        print(f"Error: Team handle '{handle}' already exists", file=sys.stderr)
        return 1

    reader = csv.reader(io.StringIO(csv_lines))
    rows = []
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
        rows.append((discord_name, vrc_name, runstyle, role_value))

    if not rows:
        print('Error: At least one member row is required', file=sys.stderr)
        return 1

    print(f'Validation passed for team {handle}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())