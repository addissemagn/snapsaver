## Bugs 
[x] Submitting with '/#first' fails b/c router handling only '/'
[] "uploads/" must already exist for file upload via web to work which just isn't ideal

## Improvements
[x] Command line args parsing
[] Add metadata to files
[] Add download status tracking to terminal
[] Add log of each file's download status to a .txt file
[] Download status page to website
[x] Store links in dicts; avoid duplicate downloads
[] Different structures for downloads i.e. all in one folder vs folders for year/month
[] Add date range selector
[] Settings for what folders to delete i.e. uploads/, downloads/, zips/
[] Save download status to a file; before starting download check if that file exists to resume download
[] Make into python package
[] Multi-threading for faster downloads?
[] Storage! Anyway to store in user's browser/computer or create a file that initiates the download process? 
[] Clean up directories
[] Setup and launch on AWS EC2 instance
[] Captcha?
 
## Error handling
[] If the file uploaded is not correct i.e. memories_history.json

## Tests/optimizations
[] Write tests
[] Test downloading different media types
[] Security i.e. email + leave as little (ideally zero) footprint of user data as possible
[] Performance with muliple simultaneous downloads
