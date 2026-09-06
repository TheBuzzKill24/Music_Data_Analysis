## Name
Music Data Analysis

## Description
This program allows you to upload a JSON file received from Spotify to construct a raw data table using Python and the MusicBrainz API to support analysis, including most favorite genre, most-listened-to song identification, and top-artist ranking. You can also download an CSV file for sharing and review.

## Installation
This project requires you to have Python installed on your system.
This project also has both pandas and MusicBrainz installed.
To install this project, run the following commands in your terminal:

```bash
git clone https://github.com](https://github.com/TheBuzzKill24/Music_Data_Analysis.git
cd your-repo-name
python -m venv .venv
.venv\Scripts\activate
pip install pandas musicbrainzngs
```


## Usage
For use, simply run app.py and after clicking the 'Load JSON File' button, upload your Spotify music data or use the example JSON provided. From there, it would show three buttons that would display different tables based on what was clicked. On each table, there is another button that will allow you to save the table as a CSV onto your system.
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.


## Roadmap
In the future, I would like to improve the performance of retrieving the genre table, as it takes a while for MusicBrainz to get all of the artist's tags. On top of that, I may add a waiting animation while it is processing. I would also like to implement numpy to show off this data on a graph for better visualization.



## Project status
Currently, I'm not focusing too much on this project due to college, but may come back to work on this project from time to time.
