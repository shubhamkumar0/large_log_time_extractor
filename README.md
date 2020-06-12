# large_log_time_extractor
Python script for exracting log for a paricular time interval from large log files. #100TB

I have divided the file into smaller buckets of equal no. of lines.
I am using the first element as a representation of that bucket, on which I apply binary search to search for the required time interval.

Would love your feedback!
