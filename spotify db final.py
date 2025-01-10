import mysql.connector
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import re

sp=spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='2f00fe82a50b44b7b4e943e29abcb369',client_secret='e3ba38b4fcf241f1ab7c9857859c2da9'))

#mysql database connection
db_config = {
    'user': 'root',
    'password': 'Sandytris04',
    'host': 'localhost',
    'port':3306,
    'database': 'spotify_db'
}


#connect to database
connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

#read the links 
filepath="\Datasets\spotifytrackslinks.txt"
with open(filepath,'r')as file:
    trackurls=file.readlines()

#process
for trackurl in trackurls:
    trackurl=trackurl.strip()
    try:
        trackid=re.search(r'track/([a-zA-Z0-9]+)',trackurl).group(1)
        track=sp.track(trackid)

        trackdata={'track name' :track['name'],'Artist':track['artists'][0]['name'],'Album':track['album']['name'],'popularity': track['popularity'],'Duration in mins':track['duration_ms']/6000}


    



        insert_query = """
INSERT INTO track_details (track_name, artist, album, popularity, duration_mins)
VALUES (%s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    album = VALUES(album),
    popularity = VALUES(popularity),
    duration_mins = VALUES(duration_mins);
"""
        cursor.execute(insert_query, (trackdata['track name'], trackdata['Artist'], trackdata['Album'], trackdata['popularity'], trackdata['Duration in mins']))
        connection.commit()
        print(f"inserted :{trackdata['track name']} by {trackdata['Artist']}")
    except Exception as e:
        print(f"Error at processing this url : {trackurl},error :{e}")

cursor.close()
connection.close()
print("all data are inserted into the data base")

df = pd.DataFrame([trackdata])
print("trackdata as a df")
print(df)

#csv save
df.to_csv('trackdata.csv',index=False)


#visualize the track details
features=['popularity','Duration in mins']
values =[trackdata['popularity'],trackdata['Duration in mins']]
plt.bar(features,values)
plt.xlabel('Features')
plt.ylabel('Values')
plt.title(f"Track Details for {trackdata['track name']} ")
plt.show()
