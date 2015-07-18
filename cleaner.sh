u=$(whoami)
folder="/Users/$u/.config/cache"
launcherpath="/Users/$u/Library/LaunchAgents"
launcher="com.extools.comagent"
flag="/var/tmp/flag"

launchctl unload "$launcherpath"/"$launcher".plist
rm "$launcherpath"/"$launcher".plist
rm -Rf "$folder"
rm $flag
rm /var/tmp/temp
