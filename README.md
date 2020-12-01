# Simple article scraper

## How it works

1. Clears out the response based on tags and classes provided in config.json 
2. Finds lowest tag containing the most amount of paragraph tags and assumes it as main content
3. If links are present, appends url to the end in square brackets and "unwraps" tag, leaving just text
4. Constructs path from the initial url of the article and saves file as .txt 
