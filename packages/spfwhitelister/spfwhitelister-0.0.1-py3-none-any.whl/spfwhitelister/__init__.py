#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#
# Query DNS looking for spf records for a given domain
# and add the addresses to the greylistd's whitelist
#

from dns.resolver import Resolver


def parse_record(resolver,record):
    """This will parse a TXT record and return the list of
       addresses/networks. It does expect the record to start with
       v=spf
    """

    #print("Parsing {}".format(record))
    mylist = []
    for subrec in record.split(" ")[1:]:
        if subrec.startswith("include:"):
            mylist += process_include(resolver,subrec)
        elif subrec.startswith("redirect:"):
            #print("Got redirect in {}".format(record))
            mylist += process_include(resolver,subrec)
        elif subrec.startswith("ip4:"):
            thisnet = subrec.split(":")[1].strip()
            mylist.append(thisnet)
        elif subrec.startswith("ip6:"):
            thisnet = subrec[4:].strip()
            mylist.append(thisnet)

    return mylist


def get_txt(resolver,addr):
    """Look for spf TXT records"""

    mylist = []
    try:
        txtrec = resolver.query(addr,"TXT")
        for arec in txtrec:
            arec = arec.to_text().strip().strip('"').replace("\" \"","")
            #print("Checking {}".format(arec))
            if arec.startswith("v=spf"):
                mylist += parse_record(resolver,arec)
            #else:
                #print ("Not starting with v=spf...{}".format(arec[:4]))
    except:
        pass
    return mylist

def process_include(resolver,record):
    """Process include and redirect mechanisms"""
    addr = record.split(":")[1]
    return get_txt(resolver,addr)



def get_spf_list(domains):
    """Generate list of spf approved IP addresses for the list of domains
    """

    mylist = []
    if isinstance(domains,str):
        domains = [domains]
    myresolver = Resolver()
    for adom in domains:
        mylist += get_txt(myresolver,adom)
    return mylist

if __name__ == "__main__":
    print("\n".join(get_spf_list("junkemailfilter.com")))
