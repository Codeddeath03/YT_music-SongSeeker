import time
from googleapiclient.errors import HttpError
import argparse
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from dotenv import load_dotenv 
import os

load_dotenv()
key = os.environ['key']
DEVELOPER_KEY = key
CLIENT_SECRETS_FILE = 'yt-p.json'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']

def authenticate_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_local_server(port=0)
  return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials = credentials)


def add_songs_to_playlist(youtube, playlist_id, video_ids):
    # Assuming video_ids is a list of video IDs to add to the playlist
    for video_id in video_ids:
       try:
        youtube.playlistItems().insert(
            part='snippet',
            body={
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
        ).execute()    
       except Exception as e:
         pass
            
def create_playlist(youtube,vids, args):
  
  body = dict(
    snippet=dict(
      title=args.title,
      description=args.description
    ),
    status=dict(
      privacyStatus='private'
    ) 
  ) 
    
  playlists_insert_response = youtube.playlists().insert(
    part='snippet,status',
    body=body
  ).execute()

  print ('New playlist ID: %s' % playlists_insert_response['id'])
  playlist_id = playlists_insert_response['id']
  # Add videos to the playlist
#  video_ids_to_add = ['video_id_1', 'video_id_2']  # Replace with actual video IDs
  add_songs_to_playlist(youtube, playlist_id, vids)
  

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=options.q,
    part='id,snippet',
    maxResults=options.max_results
  ).execute()

  videos = []
  channels = []
  playlists = []
  music=[]
  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      #videos.append('%s (%s)' % (search_result['snippet']['title'],
      #                           search_result['id']['videoId']))
      videos.append('%s' % (search_result['id']['videoId']))
      try:
       music.append('https://music.youtube.com/watch?v=%s'% (search_result['id']['videoId']))
      except:
        pass 
    elif search_result['id']['kind'] == 'youtube#channel':
      channels.append('%s (%s)' % (search_result['snippet']['title'],
                                   search_result['id']['channelId']))
    elif search_result['id']['kind'] == 'youtube#playlist':
      playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                    search_result['id']['playlistId']))

  print ('Videos:\n', '\n'.join(music), '\n')
  return videos[0]
 # print ('Channels:\n', '\n'.join(channels), '\n')
 # print ('Playlists:\n', '\n'.join(playlists), '\n')


if __name__ == '__main__':
  

  try:
    heh=input("enter list:")
    heh= """120-sammad, lukka chuppi - seedhe maut, Namastute- seedhe maut, Aisi Waise- wolf.cryman, aisay kaisay- hasan raheem, swah! seedhemaut, SAMBHAV-pho, 
      5-sitara pinjra Sammad, reality Tv- sammad, Third Gear Vasudev, Adidas Papi Vasudev, Sheesha Vasudev, Ateet- Ansh4sure, Ghaziabad- Vasudev, Shaktimaan Seedhe maut,
        Taakat seedhe maut,Raga's interlude,Garam- Chaar diwari, Mera saamaan kahan hai- Chaar diwari, Nike nike nike Vasedev, All nighter Sammad, Groupchat Sammad, KYA- CHAAR DIWARI, Loot(intro) Tarun 3bhk, Kaali Maserati Sammad, MATSYAGANA-3BHK, SUN BE SAMMAD, BABY PATANKAR SAMMAD, RUKDA NAI- SAMMAD,dhong- Tarun. -Topic, Pehlu Yoshi Tanrun. -topic,hoor - natiq,gulabo - arpit bala, ik kudi - wolf.crymaan,Roshni - Bharg Chaar diwari,PANJA- PHO"""
    list = heh.split(',')
    ids=[]
    
    for i in list:
     parser = argparse.ArgumentParser()
     parser.add_argument('--q', help='Search term', default=f"{i}")
     parser.add_argument('--max-results', help='Max results', default=1)
     args = parser.parse_args()
     print(args)
     id = youtube_search(args)
     ids.append(id)
    
    with open('list_songs.json', 'w') as file:
     json.dump(ids, file)
    #this is how ids look
    """ids= [ "3K2Tyk65oXE","oct9a5g6JmM", "1Zk6Jg4QuF0", "gReHU0Tfk70", "OGGCpCdDCiU", 
           "BMFfR8H-EJ8", "sdn9D6t7QYo", "3no38f0EUKA", "KZZ8PV8aoMY", "_aXoxvaPqMw", "zw1znFiAhkA", "rLezWQmeQvI", 
           "owmJhd2Tgho", "2XN7iPJHS7k", "h74rm2HvYl4", "yJq3nX-9Nbo", "tVAfKIyVJ-M", "C8nxICQI5Xo", "6Iox2oVm1sI", "ZUL18pR4RbY"]"""
    
    youtube = authenticate_service()
    playlist_name=input("Enter playlist name:")
    parser = argparse.ArgumentParser()
    parser.add_argument('--title',
      default=f'{playlist_name}',
      help='The title of the new playlist.')
    parser.add_argument('--description',
      default='',
      help='The description of the new playlist.')
    args = parser.parse_args()
    
    try:
     create_playlist(youtube,ids, args)
     add_songs_to_playlist(youtube, 'PL5w-iLxTlTsaWcLQN1hNoOttFV3mPVfy9', ids)
     
    except HttpError as e:
     print ('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)) 
    
  except HttpError as e:
    print ('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))