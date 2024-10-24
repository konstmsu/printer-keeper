#! /bin/bash

set -euxo pipefail

cd "$(dirname "$0")"

PLIST=printer_keeper.plist

cp $PLIST ~/Library/LaunchAgents/

cd ~/Library/LaunchAgents/

launchctl unload $PLIST 
launchctl load $PLIST

# launchctl kickstart -pk gui/$(id -u)/printer_keeper
