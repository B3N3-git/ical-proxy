# ical-proxy

## A simple proxy for ics subscriptions. I created it for adding Icloud calendar subscriptions to my Nextcloud instance.

### Fetch ics file

http\<s\>://\<ip-address\>:\<port\>/ical-proxy?url=\<your_url_to_the_ics_file\>

### Docker

You have to build your own docker image because I am to lazy to create a Docker account.

Just execute this command: **docker build -t ical-proxy .** after you copied this git repo.