import folium
import pandas as pd
volcanoData = pd.read_csv('Volcanoes.txt')
import json
# with open('world.json',encoding='utf-8-sig') as world:
#     data=json.load(world)

latList = list(volcanoData['LAT'])
longList = list(volcanoData['LON'])
elevList = list(volcanoData['ELEV'])
nameList = list(volcanoData['NAME'])
locList = list(volcanoData['LOCATION'])

def giveColor(ele):
    if ele < 1000:
        return "green"
    elif 1000 <= ele < 2000:
        return "blue"
    else:
        return "red"

def markupPopup(name,loc,elev):
    return f"""<div style="color:#000;font-weight:bold">
	<p>Volcano Name: {name}</p>
	<p>Location: {loc}</p>
	<p>Elevation: {elev} m</p>
</div>"""

mp = folium.Map(location=[38.58,-99.89], zoom_start=6, tiles="Stamen Terrain")
fgm = folium.FeatureGroup(name="Volcano Marker")
fgw = folium.FeatureGroup(name="Population and Demarcation")
for la,lo,el,nm,lc in zip(latList,longList,elevList,nameList,locList):
    iframe = folium.IFrame(html=markupPopup(nm,lc,el), width=240, height=10)
    fgm.add_child(folium.CircleMarker(location=[la,lo],radius=8,popup=folium.Popup(iframe),
                                      fill_color=giveColor(el),color="gray",fill_opacity=0.7,fill=True))
with open('world.json',encoding='utf-8-sig') as world:
    data = json.load(world)
    fgw.add_child(folium.GeoJson(data=data,style_function = 
                                 lambda x : { 'fillColor' : 'green' if x['properties']['POP2005']<10000000
                                            else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
                                            else 'red'}))

mp.add_child(fgw)
mp.add_child(fgm)
mp.add_child(folium.LayerControl())
mp.save('Map.html')

