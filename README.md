# nsrlfilter  
Wrapper to nsrlsearch for handling multiple whitelists/blacklists  
  
Running a list of samples against NSRL list to find matches and subsequent filtering out of those is simple with nsrllookup -u and -k.  
If you have additional lists to use as whitelists and/or blacklists running on other ports, you need a better client to consistently handle access.  Since DFIR is all about Python, let's do it. This was mostly an effort in learning how to run nsrllookup and handling stdin as a pipe to running nsrllookup.  
  
On your nsrl server, run each list on a different port with nsrlsrv.  
  
# Edit the WHITE and BLACK arrays below to map nsrlsvr ports to the lists it houses  
# White #1: NSRL = /usr/local/share/nsrlsvr/hashes.txt  
# White #2: Redline = /home/sansforensics/Downloads/nsrl/m-whitelist-1.0.txt  
# Black #1: VirusShare.com list  
# Black #2: Other_blacklist?  
  
Example:  
  
NSRLHOST= "your nsrlsrv"  
# Enable additional ports if additional whitelists exist  
WHITE   = [9120, 9121]  
# Enable blacklist ports if any exist  
BLACK   = [9122, 9123]  

  
