from collections import Counter

import folium
from folium.plugins import HeatMap

long_lat_fn = 'long_lat_data.txt'
data = open(long_lat_fn, 'r').readlines()
data = [ ele.strip() for ele in data]

c = Counter(data)

max_v = 153

result_lst = []
for ele_name in c:
	loc_long, loc_lat = ele_name.split('\t')
	result_lst.append([loc_lat, loc_long, c[ele_name]])
	
#print(result_lst)

map_osm = folium.Map(location=[35,110],zoom_start=5, titles='Monks')    #繪製Map，開始縮放程度是5倍

hm_wide = HeatMap(result_lst, 
                  min_opacity=0.2,
                  max_val=max_v,
                  radius=17, blur=15, 
                  max_zoom=1, 
                 )

#folium.GeoJson(district23).add_to(map_osm)
map_osm.add_child(hm_wide)

file_path = "monk_hmap.html"
map_osm.save(file_path)     # 儲存為html檔案

#webbrowser.open(file_path)  # 預設瀏覽器開啟