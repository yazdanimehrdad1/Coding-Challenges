# Coding-Challenges



* Tested with Python 3.9.4 on Windows

* Must install the "requests" pacakge used for making HTTP requests (pip install requests)

* It wasn't clear to me if the provided URL was expeted to actually return valid results, but it doesn't seem to. I just built a very simple Node server to test my code.

* At the top of main.py there is a section to set some parameters. There you can specify a text file for the program to read input batches from, or you can leave it empty to read input from the command line. You can also set the base URL, any header parameters, and the maximum number of concurrent requests. I've set these to the values provided in the description of the question. Please set to appropriate values to test the code.

* The high level design of the program is that the ItemFetcherUtil class will create worker threads which pick up requests from a concurrent queue to process. The results are placed in a cache (using a dictionary) so that we don't request the same items again. The main method of the utility (lookupItems) returns the results for a batch synchronously. If it's desired for this to be non-blocking we could change it to take a callback provided by the client. 

* The cache doesn't expire. It may be desireable to have a cache timeout (or one may be provided in the server response to be used by the clinet).

* I haven't done much for input validation or handling cases like what to do if the server takes too long to respond, or returns an error, etc. In a real-world application we'll obviously need to deal with all of those situations.
