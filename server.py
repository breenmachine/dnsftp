#!/usr/bin/python
import socket
import logging
import dns
import dns.message
import string
from binascii import b2a_base64
import re
import argparse
import sys

#Override/Modify this function to change the behavior of the server for any given query. Probably should strip whitespace.
#The current implementation uses sequential id's starting at 'startValue' - so 1.subdomain.domain.com, 2.subdomain.domain.com...
#return None when done
def get_response_data(query_name):
    itemNumber=int(query_name[0:str(query_name).find('.')])-args.startValue
    if itemNumber < 0 or itemNumber >= len(dataItems):
        return None
    logging.debug('[+] Pulling data for payload number '+str(itemNumber)+'/'+str(len(dataItems)-1))
    return re.sub('\s+',' ',dataItems[itemNumber])

def chunks(l, n):
    '''Split string l into n sized chunks'''
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def handle_query(msg,address):
    qs = msg.question
    logging.debug('[+] '+str(len(qs)) + ' questions.')

    for q in qs:
        resp = dns.message.make_response(msg)
        resp.flags |= dns.flags.AA
        resp.set_rcode(0)
        if(resp):
            response_data = get_response_data(str(q.name))
            if response_data:
                rrset = dns.rrset.from_text(q.name, 7600,dns.rdataclass.IN, dns.rdatatype.TXT, response_data)
                resp.answer.append(rrset)
                logging.debug('[+] Response created - sending TXT payload: '+response_data)
                s.sendto(resp.to_wire(), address)
            else:
                logging.debug('[-] No more data - item requested exceeds range')
                return
        else:
            logging.error('[x] Error creating response, not replying')
            return

#Handle incoming requests on port 53
def requestHandler(address, message):
    serving_ids = []

    #Don't try to respond to the same request twice somehow - track requests
    message_id = ord(message[0]) * 256 + ord(message[1])
    logging.debug('[+] Received message ID = ' + str(message_id))
    if message_id in serving_ids:
        # This request is already being served
        logging.debug('[-] Request already being served - aborting')
        return

    serving_ids.append(message_id)

    msg = dns.message.from_wire(message)
    op = msg.opcode()
    if op == 0:
        # standard and inverse query
        qs = msg.question
        if len(qs) > 0:
            q = qs[0]
            logging.debug('[+] DNS request is: ' + str(q))
            handle_query(msg,address)
    else:
        # not implemented
        logging.error('[x] Received invalid request')
    
    serving_ids.remove(message_id)
 


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--file",help="File to split up and serve")
    parser.add_argument("-s","--startValue",default=0,type=int,help='Start value for subdomain request ids. This MUST match the value set in the client, default 0')
    parser.add_argument("-q","--quiet",action='store_true',default=False,help='Disable server informational/debugging output.')
    args = parser.parse_args()

    if(len(sys.argv) < 2):
        parser.print_help()
        sys.exit(0)

    inFile = open(args.file, "rb").read()
    inData = b2a_base64(inFile)
    dataItems=list(chunks(inData,200))

    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    else:
        logging.basicConfig(level=logging.DEBUG)

    logging.debug('[+] There are '+str(len(dataItems)-1)+' parts to this file')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 53))
    logging.debug('[+] Bound to UDP port 53.')
    serving_ids = []

    while True:
        logging.debug('[+] Waiting for request...')
        message, address = s.recvfrom(1024)
        logging.debug('[+] Request received, serving')
        requestHandler(address, message)
