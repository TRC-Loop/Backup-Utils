# Backup-Utils
A Python Program that backups a folder and packs it to a zip.
## Coded using some ai: ChatGPT from OpenAI

this code does these things:
create Zip file from source_dir in deflated mode (max compression)
copy zip file to target_dir
delete old files in the target_dir directory(maxold)
wait a delay

thats it.
### Try it out. Just run it. it deletes files that are older than 30 seconds and makes an backup every 10 seconds.


## Libaries:
colorama
alive_progress
built-in:
os
datetime
zipfile
time
