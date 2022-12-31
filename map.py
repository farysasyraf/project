import folium
import branca
import pandas as pd
import geopandas
from folium import plugins
from folium.plugins import Search
print(folium.__file__)
print(folium.__version__)

df_crime = pd.read_csv('https://raw.githubusercontent.com/farysasyraf/project/main/Nilai_Crime_Data.csv')
df_crime.head()

states = geopandas.read_file(
    "https://raw.githubusercontent.com/farysasyraf/project/main/nilai-cities.json",
    driver="GeoJSON",
)

#create map and add plugins
map = folium.Map(location=[5.200073, 108.870154], zoom_start=6)

#fullscreen plugin
plugins.Fullscreen(
    position="topleft",
    title="Expand me",
    title_cancel="Exit me",
    force_separate_button=True,
).add_to(map)

#search plugin
stategeo = folium.GeoJson(
    states,
    name="Nilai"
).add_to(map)

statesearch = Search(
    layer=stategeo,
    geom_type="Polygon",
    placeholder="Search for location",
    collapsed=False,
    search_label="name",
    weight=3,
    position="topright"
).add_to(map)

#minimap plugin
minimap = plugins.MiniMap()
map.add_child(minimap)

#lat lng popup plugin
map.add_child(folium.LatLngPopup())

#add tile layer
folium.TileLayer('Stamen Terrain').add_to(map)
folium.TileLayer('Stamen Toner').add_to(map)
folium.TileLayer('Stamen Water Color').add_to(map)
folium.TileLayer('cartodbpositron').add_to(map)
folium.TileLayer('cartodbdark_matter').add_to(map)
folium.LayerControl().add_to(map)

#apply latitude & longitude
df_crime_locations = df_crime[['Latitude', 'Longitude']]

#df_crime_locations
crime_location_list = df_crime_locations.values.tolist()

def fancy_html(row):
    i = row

    ID = df_crime['ID'].iloc[i]
    Case_Number = df_crime['Case Number'].iloc[i]
    Date = df_crime['Date'].iloc[i]
    Primary_Type = df_crime['Primary Type'].iloc[i]
    Description = df_crime['Description'].iloc[i]
    Location_Description = df_crime['Location Description'].iloc[i]
    Arrest = df_crime['Arrest'].iloc[i]

    left_col_colour = "#2A799C"
    right_col_colour = "#C5DCE7"

    html = """<!DOCTYPE html>
<html>

<head>
<h4 style="margin-bottom:0"; width="300px">{}</h4>""".format(Date) + """

</head>
    <table style="height: 126px; width: 300px;">
<tbody>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">ID</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(ID) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Case Number</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Case_Number) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Date</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Date) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Primary Type</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Primary_Type) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Description</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Description) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Location Description</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Location_Description) + """
</tr>
<tr>
<td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">Arrest</span></td>
<td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(Arrest) + """
</tr>
</tbody>
</table>
</html>
"""
    return html

for point in range(0, len(crime_location_list)):
    html = fancy_html(point)

    iframe = branca.element.IFrame(html=html, width=400, height=300)
    popup = folium.Popup(iframe, parse_html=True)

    folium.Marker(crime_location_list[point],
                  popup=popup,
                  icon=folium.Icon(color='red', icon='pushpin')).add_to(map)

map