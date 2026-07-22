import musicbrainzngs

# Set up the MusicBrainz client
musicbrainzngs.set_useragent("Spotify Data Analysis", "0.7.1", contact="None")

# Get all info for an artist
def get_artist_info(artist_name):
    try:
        # Search for the artist by name
        result = musicbrainzngs.search_artists(artist=artist_name, limit=1)
        if result['artist-count'] > 0:
            artist = result['artist-list'][0]
            artist_id = artist['id']
            # Get detailed information about the artist, including tags
            artist_info = musicbrainzngs.get_artist_by_id(artist_id, includes=["tags"])
            return artist_info
        else:
            print(f"No artist found with name: {artist_name}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

# get the first 2 tags for an artist
def get_artist_tags(artist_name):
    artist_info = get_artist_info(artist_name)
    if artist_info and 'artist' in artist_info and 'tag-list' in artist_info['artist']:
        tags = artist_info['artist']['tag-list']  # Sort tags by count in descending order
        # print(tags)
        return tags[:2]  # Return the top 2 tags
    else:
        # print(f"No tags found for {artist_name}.")
        return None
  

if __name__ == "__main__":
    artist_name = "Flyleaf"
    tags = get_artist_tags(artist_name)
    if tags:
        print(f"Top 2 tags for {artist_name}:")
        for tag in tags:
            print(f"- {tag['name']} (count: {tag['count']})")
    else:
        print("No tags found.")
