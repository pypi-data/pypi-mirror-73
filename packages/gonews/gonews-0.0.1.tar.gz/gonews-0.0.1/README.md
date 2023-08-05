# GoNews CLI
    
    A simple to use CLI for viewing Google News top stories and searching for specific stories

# Install

    pip3 install gonews
   
# Examples

<h2>Print top stories from google news</h2>
    
    $ gonews top-stories

!['top-stories-gif'](examples/gonews-top-stories.gif)
    
<br>

<h2>Print top stories by location from google news</h2>

    $ gonews top-stories-by-location --city austin --state texas

!['top-stories-by-location-gif'](examples/gonews-top-stories-by-location.gif)
<br>

<h2>Print top stories based on search criteria</h2>

    $ gonews search-stories --query <search term>

    $ gonews search-stories --query Technology --has-word Apple --exclude-word Airpods --exclude-word ipod --timeframe 7d

!['search-stories-gif'](examples/gonews-search-stories.gif)