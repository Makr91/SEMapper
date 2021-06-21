#!/usr/bin/env python3
## Libraries and Defintions
import os
import sys
import csv
import ast 
import re
import json
import math
from base64 import b64encode
import yaml
import dash
import dash_core_components as dcc
import dash_html_components as html
import subprocess
from dash.dependencies import Input, Output
import discord
from discord.ext.commands import Bot
from datetime import date
import plotly.express as px
import plotly.graph_objects as go
from numpy.random import seed, rand
import numpy as np
from pprint import pprint
fileConf=open('conf.yaml','r')
cfg = yaml.load(fileConf, Loader=yaml.FullLoader)
GUILD = cfg['discord']['GUILD']
today = date.today()
mapLocations =  ["PLANETOIDS",     "MOONS",   "ASTEROIDS",   "TRADE_STATIONS",  "INTERESTS_POINTS",  "STRANGE_MATTER_OBSERVATORY","ASTEROID_FIELD","PARTROL_LOCALITIES", "NEBULAE"]
Clusters=[]
def annot(xcrd,ycrd, zcrd, txt, yancr='bottom'):
    strng=dict(showarrow=False, x=xcrd, y=ycrd, z=zcrd, text=txt, yanchor=yancr, font=dict(color=cfg['plot']['annotation']['COLOR'],size=cfg['plot']['annotation']['SIZE']))
    return strng

def spheres(size, clr, X, Y , Z): 
    # Set up 100 points. First, do angles
    theta = np.linspace(0,2*np.pi,100)
    phi = np.linspace(0,np.pi,100)
    # Set up coordinates for points on the sphere
    x0 =  X + size * np.outer(np.cos(theta),np.sin(phi))
    y0 =  Y + size * np.outer(np.sin(theta),np.sin(phi))
    z0 =  Z + size * np.outer(np.ones(100),np.cos(phi))
    # Set up trace
    trace=go.Surface(x=x0, y=y0, z=z0, colorscale=[[0,clr], [1,clr]])
    trace.update(showscale=False)
    return trace

def clusters(data): 
    X = []
    Y = []
    Z = []
    C = []
    
    for locations in data:
        C.append(locations[1])
        X.append(locations[2])
        Y.append(locations[3])
        Z.append(locations[4])
    trace=go.Mesh3d(
       x=X,
       y=Y,
       z=Z,
       color=C[0],
       opacity=cfg['plot']['objects']['NEBULAE']['OPACITY']
    )
    Clusters.append(trace)

def nebulae(size, clr, X, Y , Z): 
    np.random.seed(size)
    # Generate data
    x0 = X + size * np.random.normal(2, 0.45, cfg['plot']['objects']['NEBULAE']['DENSITY']['X'])
    y0 = Y + size * np.random.normal(2, 0.45, cfg['plot']['objects']['NEBULAE']['DENSITY']['Y'])
    z0 = Z + size * np.random.normal(2, 0.45, cfg['plot']['objects']['NEBULAE']['DENSITY']['Z'])
    # Set up trace
    trace=go.Scatter3d(
          x=x0,
          y=y0,
          z=z0,
          mode='markers',
          marker=dict(
                 color=clr,
                 opacity=cfg['plot']['objects']['NEBULAE']['OPACITY'],
                 size=cfg['plot']['objects']['NEBULAE']['SIZE'],
                 colorscale=cfg['plot']['objects']['NEBULAE']['COLORSCALE']
         )
    )
    return trace

def generate_Map():
## Read GPS Coordinate Map File
        mapCoordinatefileData = []
        mapCooridnates = []
        mapCooridnatesColor = []
        mapCooridnatesColorData = []
        mapCooridnateMarkerSize = []
        mapCooridnateType = []
        mapCooridnatesX=[]
        mapCooridnatesY=[]
        i=0
        Annot=[]
        Tracer=[]
        mapCooridnatesZ=[]
        mapAnnotations=[]
        mapFCluster=[]
        mapNCluster=[]
        mapSCluster=[]
        mapCooridnateMarkerTypeArray = []
        marker=[]
        trace=[]
        count = len(open(cfg['plot']['file']).readlines(  ))
        print('There are ' + str(count) + ' Objects to Map')
        with open(cfg['plot']['file'], 'r') as coordinateFile:
             coordinateReader = csv.reader(coordinateFile)
             for coordinateRow in coordinateReader:
                GPSLocation = coordinateRow[0].split(":")
                if (coordinateRow[0].split(":")[0] == "GPS"):
                    isGPS = "true"
                    mapCooridnatesColor = GPSLocation[5]
                    mapCooridnatesColorData.append(mapCooridnatesColor)
                    mapAnnotations.append(GPSLocation[1])
                    mapCooridnatesX.append(GPSLocation[2])
                    mapCooridnatesY.append(GPSLocation[3])
                    mapCooridnatesZ.append(GPSLocation[4])
                    ###  Set Marker and Color based on Marker Type
                    if  GPSLocation[6] in [mapLocations[0]]:
                        mapCooridnateMarkerSize.append(cfg['plot']['sizeMarkers']['PLANETOIDS'])
                        mapCooridnateType.append(mapLocations[0])
                    elif GPSLocation[6] in [mapLocations[1]]:
                        mapCooridnateMarkerSize.append(cfg['plot']['sizeMarkers']['MOONS'])
                        mapCooridnateType.append(mapLocations[1])
                    elif GPSLocation[6] in [mapLocations[2]]:
                        mapCooridnateMarkerSize.append(cfg['plot']['sizeMarkers']['ASTEROIDS'])
                        mapCooridnateType.append(mapLocations[2])
                    elif GPSLocation[6] in [mapLocations[3]]:
                        mapCooridnateMarkerSize.append(cfg['plot']['sizeMarkers']['TRADE_STATIONS'])
                        mapCooridnateType.append(mapLocations[3])
                    elif GPSLocation[6] in [mapLocations[4]]:
                        mapCooridnateMarkerSize.append(cfg['plot']['sizeMarkers']['INTERESTS_POINTS'])
                        mapCooridnateType.append(mapLocations[4])
                    elif GPSLocation[6] in [mapLocations[5]]:
                        mapCooridnateMarkerSize.append(cfg['plot']['sizeMarkers']['STRANGE_MATTER_OBSERVATORY'])
                        mapCooridnateType.append(mapLocations[5])
                    elif GPSLocation[6] in [mapLocations[6]]:
                        mapCooridnateMarkerSize.append(cfg['plot']['sizeMarkers']['ASTEROID_FIELD'])
                        mapCooridnateType.append(mapLocations[6])
                    elif GPSLocation[6] in [mapLocations[7]]:
                        mapCooridnateMarkerSize.append(cfg['plot']['sizeMarkers']['PARTROL_LOCALITIES'])
                        mapCooridnateType.append(mapLocations[7])
                    elif GPSLocation[6] in [mapLocations[8]]:
                        mapCooridnateMarkerSize.append(cfg['plot']['sizeMarkers']['NEBULAE'])
                        mapCooridnateType.append(mapLocations[8])
                    else:
                        mapCooridnateMarkerSize.append(100)
                        mapCooridnateType.append("OTHER")
                    ###  Set Set Faction Clustering Cooridnate 
                    try:
                        if not bool(GPSLocation[7]):
                            mapFCluster.append('no')
                        else:
                          mapFCluster.append(GPSLocation[7])
                    except IndexError:
                        mapFCluster.append('no')                   
                    except ValueError:
                        mapFCluster.append('no')
                        
                    ###  Set Set Nation Clustering Cooridnate   
                    try:
                        if not bool(GPSLocation[8]):
                            mapNCluster.append('no')
                        else:
                          mapNCluster.append(GPSLocation[8])
                    except IndexError:
                        mapNCluster.append('no')                   
                    except ValueError:
                        mapNCluster.append('no')
                        
                    try:
                        if not bool(GPSLocation[9]):
                            mapSCluster.append('no')
                        else:
                          mapSCluster.append(GPSLocation[9])
                    except IndexError:
                        mapSCluster.append('no')                   
                    except ValueError:
                        mapSCluster.append('no')
                else:
                    isGPS = "false"
                    print( "Somehow, your mangled cooridnates got past my sanitization checks! Not a GPS! INVALID . . INVALID . .")


        ## Get X, Y, Z
        X, Y, Z, C, S, T, FG, NG, SG = mapCooridnatesX, np.array(mapCooridnatesY), np.array(mapCooridnatesZ), np.array(mapCooridnatesColorData), mapCooridnateMarkerSize, mapCooridnateType,  mapFCluster, mapNCluster, mapSCluster
        coordinateData = [X, Y, Z, C, S, T, FG, NG, SG]

        ## Check if All Arrays Line up
        it = iter(coordinateData)
        the_len = len(next(it))
        if not all(len(l) == the_len for l in it):
             raise ValueError('Not all lists have same length! I should report this to the User to let them know something is afoul!')


        Factions=[]
        Sectors=[]
        Nations=[]
        FactionsLoc=[]
        SectorsLoc=[]
        NationsLoc=[]
        ## Map each Celestial Object
        for i in range(count):
            if mapCooridnateType[i] == 'PLANETOIDS':
                 Tracer.append(spheres(S[i],C[i],float(X[i]),float(Y[i]),float(Z[i])))
            elif mapCooridnateType[i] == 'MOONS':
                 Tracer.append(spheres(S[i],C[i],float(X[i]),float(Y[i]),float(Z[i])))
            elif mapCooridnateType[i] == 'ASTEROIDS':
                 Tracer.append(spheres(S[i],C[i],float(X[i]),float(Y[i]),float(Z[i])))
            elif mapCooridnateType[i] == 'TRADE_STATIONS':
                 Tracer.append(spheres(S[i],C[i],float(X[i]),float(Y[i]),float(Z[i])))
            elif mapCooridnateType[i] == 'INTERESTS_POINTS':
                 Tracer.append(spheres(S[i],C[i],float(X[i]),float(Y[i]),float(Z[i])))
            elif mapCooridnateType[i] == 'STRANGE_MATTER_OBSERVATORY':
                 Tracer.append(spheres(S[i],C[i],float(X[i]),float(Y[i]),float(Z[i])))
            elif mapCooridnateType[i] == 'PARTROL_LOCALITIES':
                 Tracer.append(spheres(S[i],C[i],float(X[i]),float(Y[i]),float(Z[i])))
            elif mapCooridnateType[i] == 'OTHER':
                 Tracer.append(spheres(S[i],C[i],float(X[i]),float(Y[i]),float(Z[i])))
            elif mapCooridnateType[i] == 'NEBULAE':
                 Tracer.append(nebulae(S[i],C[i],float(X[i]),float(Y[i]),float(Z[i])))
            ## Define Sectors
            if not mapFCluster[i] == 'no':
                 if not mapFCluster[i] in Factions:
                       Factions.append(mapFCluster[i]) 
                 FactionsLocTemp=(mapFCluster[i],S[i],C[i],float(X[i]),float(Y[i]),float(Z[i])) 
                 FactionsLoc.append([FactionsLocTemp])
                 
            if not mapNCluster[i] == 'no':
                 if not mapNCluster[i] in Nations: 
                       Nations.append(mapNCluster[i]) 
                 NationsLocTemp=(mapNCluster[i],S[i],C[i],float(X[i]),float(Y[i]),float(Z[i])) 
                 NationsLoc.append([NationsLocTemp])
                 
            if not mapSCluster[i] == 'no': 
                 if not mapSCluster[i] in Sectors:
                       Sectors.append(mapSCluster[i]) 
                 SectorsLocTemp=(mapSCluster[i],S[i],C[i],float(X[i]),float(Y[i]),float(Z[i])) 
                 SectorsLoc.append([SectorsLocTemp])
                 
            Annot.append(annot(float(X[i]), float(Y[i]), float(Z[i]), mapAnnotations[i] ))

        ## Create Sector Meshs       
        ## For each Faction Create Trace
        for faction in Factions:
            factionlocs=[]
            for i in range(len(FactionsLoc)):
                for j in range(len(FactionsLoc[i])):
                    if FactionsLoc[i][j][0] in faction:
                        factionlocs.append([FactionsLoc[i][j][1],FactionsLoc[i][j][2],FactionsLoc[i][j][3],FactionsLoc[i][j][4],FactionsLoc[i][j][5]])
            print()
            print("faction Locations")
            print(factionlocs)
            clusters(factionlocs)

        ## For each Nation Create Trace
        
        for nation in Nations:
            nationlocs=[]
            for a in range(len(NationsLoc)):
                for j in range(len(NationsLoc[a])):
                    if NationsLoc[a][j][0] in nation:
                        print(NationsLoc[a][j][0])
                        nationlocs.append([NationsLoc[a][j][1],NationsLoc[a][j][2],NationsLoc[a][j][3],NationsLoc[a][j][4],NationsLoc[a][j][5]])
            print()
            print()
            print("nation Locations")
            print(nationlocs)
            print()
            clusters(nationlocs)
            
        for sector in Sectors:
            sectorlocs=[]
            for i in range(len(SectorsLoc)):
                for j in range(len(SectorsLoc[i])):
                    if SectorsLoc[i][j][0] in sector:
                        sectorlocs.append([SectorsLoc[i][j][1],SectorsLoc[i][j][2],SectorsLoc[i][j][3],SectorsLoc[i][j][4],SectorsLoc[i][j][5]])
            print()
            print("Sector Locations")
            print(sectorlocs)
            clusters(sectorlocs)
        

        layout=go.Layout(width = cfg['plot']['width'], height = cfg['plot']['height'], title = cfg['plot']['title'], showlegend=cfg['plot']['legend']['show'], margin=dict(l=cfg['plot']['margin']['l'], r=cfg['plot']['margin']['r'], t=cfg['plot']['margin']['t'], b=cfg['plot']['margin']['b']),
                          paper_bgcolor = cfg['plot']['paper']['COLOR'],
                          scene = dict(xaxis=dict(title='Draconis', 
                                                  titlefont_color=cfg['plot']['sector']['COLOR']['X'], 
                                                  backgroundcolor=cfg['plot']['background']['COLOR']['X'],
                                                  color=cfg['plot']['axis']['COLOR']['X'],
                                                  gridcolor=cfg['plot']['grid']['COLOR']['X']
                                                 ),
                                       yaxis=dict(title='Draconis',
                                                  titlefont_color=cfg['plot']['sector']['COLOR']['Y'],
                                                  backgroundcolor=cfg['plot']['background']['COLOR']['Y'],
                                                  color=cfg['plot']['axis']['COLOR']['Y'],
                                                  gridcolor=cfg['plot']['grid']['COLOR']['Y']
                                                 ),
                                       zaxis=dict(title='Draconis', 
                                                  titlefont_color=cfg['plot']['sector']['COLOR']['Z'],
                                                  backgroundcolor=cfg['plot']['background']['COLOR']['Z'],
                                                  color=cfg['plot']['axis']['COLOR']['Z'], 
                                                  gridcolor=cfg['plot']['grid']['COLOR']['Z']
                                                 ),
                                       annotations=Annot
                                       ))

        config = {'displaylogo': False}
        fig = go.Figure(data = Tracer, layout = layout)
        # Add Clusters
        for cluster in Clusters:
            fig.add_trace(cluster)   
        fig.write_image("image.png")
        fig.write_html("map/index.html", config=config)
bot = Bot(command_prefix='$')
@bot.event
async def on_ready():
	print(f'Bot connected as {bot.user}')
@bot.event
async def on_message(message):
          if (message.author.bot):
                print("I detected a new message, from myself, I am shutting up now. . .")
                return
          ## If the Message contains ANY GPS looking Cooridnates, Let Take a look at it:
          if re.search("GPS:.+:.+:.+:.+:.+:?(:.+)?(:.+)?(:.+)?", message.content,re.IGNORECASE):
                match=[]
                pattern=[]
                factionID=""
                nationID=""
                sectorID=""
                factionIDlen=0
                currentmapLocation=""
                colorMatch6=False
                colorMatch8=False
                colorMatch8convert=""
                pattern = re.sub(r'^.*?GPS', 'GPS',message.content )
                pattern = re.match("GPS:.+:.+:.+:.+:.+:?(:.+)?(:.+)?(:.+)?", pattern,re.IGNORECASE)
                #### Verify Cooridnates
                userLoc = pattern.group(0).split(":")
                pprint(userLoc)
                keyMatch = re.search('GPS', userLoc[0])
                colorMatch = re.search(r'^#(?:[0-9a-fA-F]{3,4}){1,2}$', userLoc[5])
                colorMatch6 = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', userLoc[5])
                colorMatch8 = re.search(r'^#(?:[0-9a-fA-F]{4}){1,2}$', userLoc[5])
                try:
                   factionID=userLoc[7]
                   print(userLoc[7])
                   factionIDlen=len(factionID)
                   if (factionIDlen == 3):
                      factionID=userLoc[7]
                   else:
                      await message.channel.send('Invalid or No Faction TAG!, nulling field')
                      print('Throwing out User inputted factionID')
                      factionID=""
                except:
                   print('No Faction ID Found')
                   
                                      
                try:
                   nationID=userLoc[8]
                   print(userLoc[8])
                   nationIDlen=len(nationID)
                   if (nationIDlen == 3):
                      nationID=userLoc[8]
                   else:
                      await message.channel.send('Invalid or No Nation TAG!, nulling field')
                      print('Throwing out User inputted nationID')
                      nationID=""
                except:
                   print('No Nation ID Found')
                   
                   
                try:
                   sectorID=userLoc[9]
                   print(userLoc[9])
                   sectorIDlen=len(sectorID)
                   if (sectorIDlen == 6):
                      sectorID=userLoc[9]
                   else:
                      await message.channel.send('Invalid or No Sector TAG!, nulling field')
                      print('Throwing out User inputted sectorID')
                      sectorID=""
                except:
                   print('No Sector ID Found')
                   
                   
                   
                # Check if Map Category is Empty
                try:
                   currentmapLocation=userLoc[6]
                   print(currentmapLocation)
                   if (currentmapLocation in mapLocation):
                      currentmapLocation=userLoc[6]
                   else:
                      await message.channel.send('Improper Category!, So I am ignorning your trash')
                      print('Throwing out User inputted Location Category')
                      currentmapLocation=""
                except:
                   print('No Category Found')

                if keyMatch.group(0):
                   print("")
                else:
                   await message.channel.send('Required Element: Your GPS Entry was managled'  )
                   return
                ###DEV# PH#  Logic to Sanitize Names
                try:
                    userX=userLoc[2]
                    userLoc[2]=float(userLoc[2])
                except ValueError:
                   await message.channel.send('Required Element: Your X Entry does not look like a Number, Please check your GPS'  )
                   return
                try:
                    userY=userLoc[3]
                    userLoc[3]=float(userLoc[3])
                except ValueError:
                   await message.channel.send('Required Element: Your Y Entry does not look like a Number, Please check your GPS'  )
                   return
                try:
                    userZ=userLoc[4]
                    userLoc[4]=float(userLoc[4])
                except ValueError:
                   await message.channel.send('Required Element: Your Z Entry does not look like a Number, Please check your GPS'  )
                   return
                print(colorMatch6, colorMatch8)
                if colorMatch is None: 
                   await message.channel.send('Required Element: Your Hex Color is not Valid'  )
                   return
                elif colorMatch6:
                   print('I think I found a 6 Digit Hex Code')
                   colorLoc = userLoc[5]
                elif colorMatch8:
                   print('I think I found a 8 Digit Hex Code')
                   colorMatch8strip=userLoc[5].lstrip('#')
                   colorMatch8strip=colorMatch8strip[2:]
                   colorMatch8convert= '#' + colorMatch8strip
                   print(colorMatch8convert)
                   colorLoc =  colorMatch8convert
                else:
                   await message.channel.send('Required Element: Your Hex Color is not Valid'  )
                   return
                ### Check if last key is Known Category
                if (currentmapLocation in mapLocations):
                   contained = [x for x in mapLocations if x in userLoc[6]]
                   print(contained)
                else:
                   await message.channel.send('No Category Matched, but . . .')
                await message.channel.send('Recording GPS: GPS:' + userLoc[1] + ":"  + userX + ":"  + userY + ":" + userZ + ":" + colorLoc + ":" + currentmapLocation  + ":" + factionID + ":" + nationID + ":" + sectorID)
                print("Adding GPS Cooridinate")
                mcfWriter = open(cfg['plot']['file'], "a")
                safeLoc = 'GPS:' + userLoc[1] + ":"  + userX + ":"  + userY + ":" + userZ + ":" + colorLoc  + ":" + currentmapLocation + ":" + factionID + ":" + nationID + ":" + sectorID
                print(safeLoc)
                mcfWriter.write(safeLoc)
                mcfWriter.write("\n")
                mcfWriter.close()

          elif "GG:" in  message.content:
                await message.channel.send('Generating GPS Map From current known Cooridnates:')
                generate_Map()
                with open('image.png', 'rb') as f:
                     picture = discord.File(f)
                     await message.channel.send(file=picture)
                     ## Send Map to Web Server:
                     try:
                         process = subprocess.Popen(
                             ['rsync',
                             '-avz',
                             '-e',
                             'ssh -o StrictHostKeyChecking=no -p 22 -i /home/myuser/Documents/Projects/id_rsa',
                             '/home/myuser/Documents/Projects/map',
                             '{}@{}:{}'.format('username', 'somehostoripaddress', '/var/www/html/public_html/')],
                             stdout=subprocess.PIPE
                         )
                         output = process.communicate()[0]
                         if int(process.returncode) != 0:
                             print('Command failed. Return code : {}'.format(process.returncode))
                             exit(1)
#                         return output
                     except Exception as e:
                         print(e)
                         exit(1)
                     await message.channel.send('You can access the updated Live Map here: https://draconis.example.com/map/index.html')
# End Client
bot.run(cfg['discord']['TOKEN'])
