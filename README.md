# whereIs
Simple script that allows us to capture the victim's ip via link

## About the script
This script generates a link through ngrok, which redirects us to youtube, during the redirection we include the ip.php file, this script in php is the core of everything, this is responsible for capturing the ip that travels through the headers, then saves it in a file called ip.txt

## Requirements:
To run the script you can install ngrok in the same folder as the script, or the script can do it for you

## Usage:
```
python3 whereIs.py <port>
example: python3 whereIs.py 4343

Port 443 is not available, it could give errors
```
