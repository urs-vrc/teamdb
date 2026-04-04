#!/bin/bash
# Copyright 2026 (c) The Umamusume Racing Society Contributors
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
set -euo pipefail

HANDLE="${1?team_handle required}"
FQDN="${2?team_fqdn required}"
DESC="${3:-No description provided}"
CSV_LINES="${4?members_csv_lines required}"
SECRET="${5?submission_secret required}"

if [[ "$SECRET" != "${TEAM_SUBMISSION_SECRET}" ]]; then
  echo "Error: Invalid submission secret (we got hijacked!?!??!??!)"
  exit 1
fi

if [[ ! "$HANDLE" =~ ^[a-zA-Z0-9]{5}$ ]]; then
  echo "Error: team_handle must be exactly 5 alphanumeric characters"
  exit 1
fi

if [ -d "teams/$HANDLE" ]; then
  echo "Error: Team handle '$HANDLE' already exists"
  exit 1
fi


TEMP_DIR=$(mktemp -d)
cat > "$TEMP_DIR/submission.json" <<EOF
{
  "team_handle": "$HANDLE",
  "team_fqdn": "$FQDN",
  "team_description": "$DESC",
  "members": [
$(echo "$CSV_LINES" | awk -F, '{printf "    {\"name\":\"%s\",\"discord_name\":\"%s\",\"vrc_name\":\"%s\",\"role\":\"%s\"}%s\n", $1, $2, $3, $4, (NR==1?"":",")}' | sed 's/,$//')
  ]
}
EOF

# Run your existing Dart validator
echo "Running Dart validator..."
cd validator || exit 1
dart run bin/validator.dart "$TEMP_DIR/submission.json"   # ← adjust path/command to match your Dart setup

# If validator passed, also check for exactly one captain (or whatever your rules are)
if ! echo "$CSV_LINES" | grep -q "team_captain"; then
  echo "Error: Team must have at least one team_captain"
  exit 1
fi

echo "Validation passed for team $HANDLE"
rm -rf "$TEMP_DIR"