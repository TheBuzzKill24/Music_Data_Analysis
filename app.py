import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, scrolledtext
import json
from musicAPI import get_artist_tags

# Function to create a DataFrame from the JSON data
def create_dataframe(data):
    df = pd.DataFrame(data)
    df['minutesPlayed'] = df['msPlayed'] / (1000 * 60)
    # df['endTime'] = pd.to_datetime(df['endTime'])
    # df['date'] = df['endTime'].dt.date
    # df['day-of-week'] = df['endTime'].dt.day_name()
    # df['month'] = df['endTime'].dt.month
    # df['hour'] = df['endTime'].dt.hour
    return df

# Function to load the JSON file
def load_json_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                df = create_dataframe(data)
                result_window(df, "Spotify Streaming History Results")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to decode JSON file.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to create a new window with three buttons to display the DataFrames
def result_window(df, title):
    new_window = tk.Toplevel(window)
    new_window.title(title)
    
    # Button to display the main DataFrame
    main_button = tk.Button(new_window, text="Display Main DataFrame", command=lambda: display_dataframe(df, "Main DataFrame"))
    main_button.pack(pady=10)

    # Button to display the Top Artists DataFrame
    summary_button = tk.Button(new_window, text="Display Top Artists", command=lambda: display_dataframe(create_top_artists_dataframe(df), "Top Artists"))
    summary_button.pack(pady=10)

    # Button to display the Top Genres DataFrame
    genres_button = tk.Button(new_window, text="Display Top Genres", command=lambda: display_dataframe(create_top_genres_dataframe(df), "Top Genres"))
    genres_button.pack(pady=10)

def save_dataframe_to_csv(df, title):
    # Ask the user where to save the CSV file
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialfile=title.replace(" ", "_") + ".csv")
    if file_path:
        try:
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", f"DataFrame saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save DataFrame: {str(e)}")

# Function to display a DataFrame in a new window and convert it to a csv file and save it to the download folder
def display_dataframe(df, title):
    display_window = tk.Toplevel(window)
    display_window.title(title)
    
    # Create a table to display the DataFrame in a scrolled text area
    tree = ttk.Treeview(display_window)
    tree.pack(padx=10, pady=10)

    # Add columns to the tree
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    # Add column headings
    for col in df.columns:
        tree.heading(col, text=col)

    # Add data to the tree
    for row in df.itertuples(index=False):
        tree.insert("", "end", values=row)

    




    # text_area = scrolledtext.ScrolledText(display_window, wrap=tk.WORD, width=100, height=30)
    # text_area.pack(padx=10, pady=10)
    
    # # Before df is converted to string, increase index by 1 to start from 1 instead of 0
    # df.index = df.index + 1

    # text_area.insert(tk.END, df.to_string())
    # text_area.configure(state='disabled')  # Make the text area read-only

    # Create a button to save the DataFrame to a CSV file in the download folder
    save_button = tk.Button(display_window, text="Save to CSV", command=lambda: save_dataframe_to_csv(df, title))
    save_button.pack(pady=10)

# Function to create the Top Genres DataFrame
def create_top_genres_dataframe(df):
    song_summary = df.groupby(['artistName']).agg({'minutesPlayed': 'sum'}).sort_values('minutesPlayed', ascending=False).reset_index()
    song_summary = song_summary.head(100)

    artist_genres = []
    for artist in song_summary['artistName'].unique():
        tags = get_artist_tags(artist)
        if tags:
            artist_genres.append({'artistName': artist, 'genre': tags[0]['name'] if len(tags) > 0 else None})
        else:
            artist_genres.append({'artistName': artist, 'genre': 'Indie'})

    artist_genres_df = pd.DataFrame(artist_genres)

    # For each genre, count the number of times it appears and sum the minutes played for that genre
    genre_summary = artist_genres_df.merge(song_summary, on='artistName', how='left')
    genre_summary = genre_summary.groupby(['genre']).agg({'minutesPlayed': 'sum'}).sort_values('minutesPlayed', ascending=False).reset_index()

    return genre_summary

# Function to create the Top Artist DataFrame
def create_top_artists_dataframe(df):
    song_summary = df.groupby(['artistName']).agg({'minutesPlayed': 'sum'}).sort_values('minutesPlayed', ascending=False).reset_index()
    return song_summary

# Create the main window
window = tk.Tk()
window.title("Spotify Data Analysis")
window.geometry("400x200")


# Create a button to load the JSON file
load_button = tk.Button(window, text="Load JSON File", command=load_json_file)
load_button.pack(pady=20)


window.mainloop()