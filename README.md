# gmusicdownloader.py
## A quickly hacked together Google Play Music album downloader based on gmusicapi

Supports album downloading and library syncing, automatic ID3 tagging and cover art downloading.  
Requires a Google Play Music All Access subscription.  
Downloaded tracks are **320kbps** MP3s.


![gmusicdl](https://s3.gifyu.com/images/render1558987999320.gif)

## Installation and running
```
pip3 install -r requirements.txt
chmod +x gmusicdownloader.py
./gmusicdownloader.py
```

## Usage
```
$ ./gmusicdownloader.py --help

usage: gmusicdownloader.py [-h] [-e EMAIL] [-p PASSWORD] [-d DEVICEID]
                           [-o OUTPUT] [-s]

Google Play Music album downloader

optional arguments:
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        Google Play Music email
  -p PASSWORD, --password PASSWORD
                        Google Play Music password
  -d DEVICEID, --deviceid DEVICEID
                        Google Play Music device ID
  -o OUTPUT, --output OUTPUT
                        output directory
  -s, --sync            sync Google Play Music library to output folder

```
