import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Spotify API credentials
CLIENT_ID = "2866b57e3bd446ca8b3216d48bc77146"
CLIENT_SECRET = "c79768b5a9e34981b23af810af1204a9"


# Spotify authentication
client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

sp = spotipy.Spotify(auth_manager=client_credentials_manager)


# Function to fetch album cover
def get_song_album_cover_url(song_name, artist_name):

    query = f"track:{song_name} artist:{artist_name}"

    results = sp.search(q=query, type="track", limit=1)

    if results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        return track["album"]["images"][0]["url"]

    return "https://i.postimg.cc/0QNxYz4V/social.png"


# Recommendation function
def recommend(song):

    index = music[music['song'] == song].index[0]

    distances = sorted(
        list(enumerate(similar[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_music_names = []
    recommended_music_posters = []

    for i in distances[1:6]:

        artist = music.iloc[i[0]].artist
        song_name = music.iloc[i[0]].song

        recommended_music_names.append(song_name)

        recommended_music_posters.append(
            get_song_album_cover_url(song_name, artist)
        )

    return recommended_music_names, recommended_music_posters


# Streamlit UI
st.header("Music Recommender System")


# Load data
music = pickle.load(open("df.pkl", "rb"))
similar = pickle.load(open("similar.pkl", "rb"))


music_list = music["song"].values


# Dropdown selection
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)


# Show recommendations
if st.button("Show Recommendation"):

    names, posters = recommend(selected_song)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.caption(names[0])
        st.image(posters[0], use_column_width=True)

    with col2:
        st.caption(names[1])
        st.image(posters[1], use_column_width=True)

    with col3:
        st.caption(names[2])
        st.image(posters[2], use_column_width=True)

    with col4:
        st.caption(names[3])
        st.image(posters[3], use_column_width=True)

    with col5:
        st.caption(names[4])
        st.image(posters[4], use_column_width=True)