A simple utility for smartly purging backup directories. 

Read more here: http://www.johnandcailin.com/blog/john/smartly-purge-your-old-backup-files-linux

```
Usage: purgeFiles [OPTION]...
 -h, --help                          Print this help message
 -a, --ages=age1,age2                Desired ages to keep (in days)
 -d, --directory=dir                 Target directory
 -m, --minfiles=num                  Minimum number of files before running
 -p, --pattern=pattern               File pattern to match
 -f, --force                         Force deletion (no simulation mode)

e.g. purgeFiles --ages=1,2,4,40 --directory=/tmp --pattern="*.txt"
This would purge /tmp and try to keep a files ending in .txt of 40 days, 4 days, 2 days and 1 day old. 
Note: this would only do a simulation run. Specify --force to actually delete the files. 

Author: John Quinn, http://johnandcailin.com/john
```

Note: minfiles is currently a weak safety net. It prevents starting if the
minfiles count isn't met for matches in the given directory. It does not
prevent removing files to a number lower than given if the directory starts
with more files.
