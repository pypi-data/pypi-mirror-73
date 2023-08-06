# spfwhitelister

spfwhitelister is very simple Python library/utility.

Given a list of domains, it will query SPF records
for those domains and retrieve the list of IP addresses
authorized to send email for those domains.  It can then
manage that list in a file.

This can be used when using greylistd. One could schedule
(crontab) this utility to run once or twice a day and manage
the list of whitelisted hosts.

I am using Exim on Debian. Exim4 is very powerfull but it can be
a real pain to configure, especially on Debian with the solit config.
I think this is easier. With greylistd any address missed because of
the delay would simply be greylisted.

This was tested on Debian with Exim4.

# Installation

We are on PyPi so

     pip3 install spfwhitelister


You can then run:

     spfwhitelister -o -d google.com amazon.com




