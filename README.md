# Simple article scraper

## How it works

1. Clears out the response based on tags and classes provided in config.json 
2. Finds lowest tag containing the most amount of paragraph tags and assumes it as main content
3. If <a> tags are present, appends url to the end and "unwraps" tag, leaving just text
4. Constructs path from the url and saves file as .txt 
