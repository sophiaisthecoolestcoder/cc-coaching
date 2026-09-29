#!/usr/bin/env bash
# Upload the public site to IONOS Webhosting over SFTP/SSH.
#
# Only the files listed in PUBLIC are sent. content/ (the client's source
# documents, including private data), tools/, the docs and styleguide.html
# never leave this machine.
#
# Usage, from anywhere:
#   IONOS_USER=… IONOS_HOST=… tools/deploy.sh        # dry run: shows what would change
#   IONOS_USER=… IONOS_HOST=… tools/deploy.sh --go   # upload for real
set -euo pipefail

cd "$(dirname "$0")/.."

: "${IONOS_USER:?set IONOS_USER (SFTP user from IONOS > Hosting > SFTP & SSH)}"
: "${IONOS_HOST:?set IONOS_HOST (e.g. access-XXXXXXX.webspace-host.com)}"
TARGET="${IONOS_DIR:-cc-coaching}"   # webspace folder the domain points at

PUBLIC=(index.html impressum.html datenschutz.html robots.txt sitemap.xml
        .htaccess assets styles scripts)

# Refuse to publish text that did not come from her documents.
(cd tools && python3 verify_verbatim.py | tail -1 | grep -q PASS) \
  || { echo "verify_verbatim.py did not PASS - not deploying." >&2; exit 1; }

DRY="--dry-run"
[[ "${1:-}" == "--go" ]] && DRY=""

rsync -avz --delete --exclude '.DS_Store' $DRY -e ssh \
  "${PUBLIC[@]}" "${IONOS_USER}@${IONOS_HOST}:${TARGET}/"

[[ -n "$DRY" ]] && echo -e "\nDry run only. Re-run with --go to upload."
