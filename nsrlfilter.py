#!/usr/bin/python

from __future__ import print_function
import sys, getopt, string, socket

# Edit the WHITE and BLACK arrays below to map nsrlsvr ports to the lists it houses
# White #1: NSRL = /usr/local/share/nsrlsvr/hashes.txt
# White #2: Redline = /home/sansforensics/Downloads/nsrl/m-whitelist-1.0.txt
# Black #1: VirusShare.com?
# Black #2: Other_blacklist?

NSRLHOST= "infra.hpdis.net"
# Enable additional ports if additional whitelists exist
#WHITE   = [9120, 9121]
WHITE   = [9120]
# Enable blacklist ports if any exist
#BLACK   = [9122, 9123]
BLACK   = []

def error(text):
    print("ERROR: ", text, file=sys.stderr)

def usage():
    error('nsrlprint.py [-b|--black] [-w|--white] [-a|--all] [-s|--skipbad')

def testsocket(HOST,PORT):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((HOST,PORT))
    return result

def main():

    from subprocess import Popen,PIPE,STDOUT

    white=0
    black=0
    errorfound=0
    skipbad=0
    pipe = []

    try:
        opts, args = getopt.getopt(sys.argv[1:],"wbas",["white","black","all",skipbad])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-w" or opt == "--white" or opt == "-a" or opt == "-all":
            white=1
        if opt == "-b" or opt == "--black" or opt == "-a" or opt == "-all":
            black=1
        if opt == "-s" or opt == "--skipbad":
            skipbad=1

    if black==0 and white==0:
        usage()
        sys.exit(2)

    if white==1:
        for PORT in WHITE:
            if testsocket(NSRLHOST, PORT) == 0:
                pipe.append(Popen(['nsrllookup','-u','-s',NSRLHOST,'-p',str(PORT)], stdout=PIPE, stdin=PIPE, stderr=STDOUT))
            else:
		errorfound=1
                error("Whitelist at " + NSRLHOST + " on port " + str(PORT) + " is unavailable")
    if black==1:
        for PORT in BLACK:
            if testsocket(NSRLHOST, PORT) == 0:
	        pipe.append(Popen(['nsrllookup','-k','-s',NSRLHOST,'-p',str(PORT)], stdout=PIPE, stdin=PIPE, stderr=STDOUT))
            else:
		errorfound=1
                error("Blacklist at " + NSRLHOST + " on port " + str(PORT) + " is unavailable")

    if errorfound==1 and skipbad==0:
        sys.exit(1)
    input=sys.stdin.read()
    out = "";
    for inc in pipe:
        out=inc.communicate(input=input)[0]
        input=out
        inc.stdout.close()
    if out:
        print (out)

if __name__ == "__main__":
    main()
