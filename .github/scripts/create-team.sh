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

HANDLE="${1}"
FQDN="${2}"
DESC="${3:-No description provided}"
CSV_LINES="${4}"

DIR="teams/$HANDLE"
mkdir -p "$DIR"

# FIXME: If you're seeing this jett, I fucking gave up midway and I have no idea wtf am I doing lmao
# members.csv
{
  echo "name,discord_name,vrc_name,role"
  echo "$CSV_LINES"
} > "$DIR/members.csv"

# metadata.yml
cat > "$DIR/metadata.yml" <<EOF
team_fqdn: "$FQDN"
team_handle: "$HANDLE"
team_description: |-
  ${DESC}
EOF

echo "Files generated successfully in $DIR"
ls "$DIR"

exit 0;