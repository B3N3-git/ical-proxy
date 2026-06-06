# ical-proxy

## A simple proxy for ics subscriptions. I created it for adding Icloud Calendars to my Nextcloud instance.

### Fetch ics file

http\<s\>://\<ip-address\>:\<port\>/ical_url?url=\<your_url_to_the_ics_file\>

You have to build your own docker image because I am to lazy to create a Docker account.

Just execute this command: docker build -t ical-proxy .