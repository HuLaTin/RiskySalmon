import folium
import asyncio
import websockets
import json
from datetime import datetime, timezone
from keys import apiKey, boundingBox1, watchList, ship_names_dict
target_ship_id = watchList[0]

async def connect_ais_stream():
    async with websockets.connect("wss://stream.aisstream.io/v0/stream") as websocket:
        subscribe_message = {"APIKey": apiKey, "BoundingBoxes": [[[boundingBox1[0], boundingBox1[1]], [boundingBox1[2], boundingBox1[3]]]]}
        subscribe_message_json = json.dumps(subscribe_message)
        await websocket.send(subscribe_message_json)
        
        m = folium.Map(location=[boundingBox1[0], boundingBox1[1]], zoom_start=9)
        ships = folium.FeatureGroup(name="Ships")

        async for message_json in websocket:
            message = json.loads(message_json)
            message_type = message["MessageType"]

            if message_type == "PositionReport":
                ais_message = message['Message']['PositionReport']
                
                # Check if the ship is the target ship
                if ais_message['UserID'] == target_ship_id:
                    # Center the map on the target ship
                    m = folium.Map(location=[ais_message['Latitude'], ais_message['Longitude']], zoom_start=9)
                    
                if ais_message['UserID'] in watchList:
                    color = 'red'
                    ship_name = "Unknown Ship"
                    if ais_message['UserID'] in ship_names_dict:
                        ship_name = ship_names_dict[ais_message['UserID']]
                else:
                    color = 'blue'
                    ship_name = "Unknown Ship"
                    if ais_message['UserID'] in ship_names_dict:
                        ship_name = ship_names_dict[ais_message['UserID']]

                folium.CircleMarker(
                    location=[ais_message['Latitude'], ais_message['Longitude']],
                    radius=5,
                    color=color,
                    fill=True,
                    fill_color=color,
                    popup=ship_name
                ).add_to(ships)

            ships.add_to(m)
            m.save(r"Data\ships.html")

if __name__ == "__main__":
    asyncio.run(connect_ais_stream())
