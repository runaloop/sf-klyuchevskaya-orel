#!/usr/bin/env bash
# Rename the campaign folder id and every internal reference to it.
# Run once, right before publishing, so the edition can coexist with the
# original mod:  tools/rename_campaign.sh SF_Klyuchevskaya_88_Orel
set -euo pipefail
new=${1:?usage: rename_campaign.sh <new_folder_id>}
old=SF_Klyuchevskaya_88
root=$(cd "$(dirname "$0")/.." && pwd)/mod/campaigns
[ -d "$root/$old" ] || { echo "no folder $root/$old"; exit 1; }
[ -e "$root/$new" ] && { echo "$root/$new already exists"; exit 1; }
mv "$root/$old" "$root/$new"
grep -rlZ "${old}[\\/]" "$root/$new" --include='*.ini' --include='*.xml' \
  | xargs -0 sed -i "s/${old}\([\\\\\/]\)/${new}\1/g"
left=$(grep -rc "${old}[\\/]" "$root/$new" --include='*.ini' --include='*.xml' | grep -vc ':0$' || true)
echo "renamed $old -> $new, files still mentioning the old id: $left"
