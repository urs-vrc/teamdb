# Sample Team Manifest

This is a sample format that all team directories should follow. These usually contain two files but may also contain two images, primarily the team banner and the team icon.

All team folders are named after their team handles, which is a shorthand identifiers for their teams, and they usually contain the following files:

### `metadata.yaml`

The `metadata.yaml` contains basic information about a team. These are usually short description of their teams .

```yaml
# Every team gets its own metadata.yaml, which includes basic information about their team.
# Brightling and other URS Online Services are expecting this file and format, so do NOT diverge from this format.

# team handles are your team shorthands/identifiers, must be 3-4 characters, ASCII only.
team_handle: EXM1
# the full name of your team, no character limit but we encourage to keep it within 32 characters.
team_fqdn: Example Team
# URL of your team icon, must be transparent and the icon resolution must be a power-of-two resolution
# If you want to include your own icon alongside your team database, make sure to use "./" instead (ex: ./example.png).
team_icon_url: https://example.com/favicon.png
# A short blurb about your team, maximum 256 characters.
team_blurb: This is an example team manifest that bots and the URS Online Services will read for your team description.
```

### `members.csv`

This includes the list of all the members of your teams, including captains, co-captains, trainers and regular roster participants. It must follow the format included in `members.csv`. Keep in mind the first values in the CSV must remain intact for it to be valid as these are the column names for each entry.

The column entry expects the following values:

| Column Name | Type | Description    |
| ----------- | ---- | -------------- |
| `discord_name` | string | The member's Discord username, must be lowercase and within 24 characters or less |
| `vrc_name` | string | The member's VRChat username, must be 64 characters. |
| `runstyle` | string | The members running style. Must use the following shorthands: FR (Front-running), PC (Pace-chasing), LS (Late-surging), EC (End-closing). If more than one style, append a + after the alternative style (ex: EC+LS). |
| `role` | number | The member's role. It expects a value from 0 up to 4, which will stand for the following: role ID 0 for Captains, role ID 1 for Co-Captains, role ID 2 for Trainers, role ID 3 for Regular Members, and role ID 4 for Temporary members. |
