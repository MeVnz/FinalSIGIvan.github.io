import streamlit as st
import folium
import json
from streamlit.components.v1 import html

st.title("Peta Interaktif Kabupaten Majene")

# Sidebar untuk kontrol interaktif
st.sidebar.header("Kontrol Peta")
location_options = {
    "Lembang": [-3.5396, 118.9867],
    "Labuang": [-3.5459, 118.9742],
    "Baurung": [-3.5536, 118.9895],
    "Labuang Utara": [-3.5367, 118.9755],
    "Tande Timur": [-3.5254, 118.9918],
    "Tande": [-3.5158, 118.9796],
    "Baruga": [-3.5191, 118.9492],
    "Buttu Baruga": [-3.4869, 118.9424],
    "Baruga Dhua": [-3.4822, 118.9560],
}

# Pilihan lokasi
location_choice = st.sidebar.selectbox("Pilih Lokasi", list(location_options.keys()))
default_location = location_options[location_choice]

# Slider untuk mengatur zoom level
zoom_start = st.sidebar.slider("Zoom Level", min_value=5, max_value=15, value=12)

# Skema warna abu-abu dari paling gelap ke paling pudar
colors_gray = [
    "#660000",  # Merah paling gelap
    "#800000",
    "#990000",
    "#b30000",
    "#cc0000",
    "#e60000",
    "#ff0000",
    "#ff3333",
    "#ff6666",
    "#ff9999"  # Merah paling pudar
]

# Membaca data GeoJSON
with open('map.geojson') as f:
    geojson_data = json.load(f)

# Mengambil kepadatan penduduk
densities = [feature['properties']['KEPADATAN'] for feature in geojson_data['features']]
min_density = min(densities)
max_density = max(densities)

# Fungsi untuk membuat popup untuk setiap fitur
def popup_function(feature):
    density = feature['properties']['KEPADATAN']
    return folium.Popup(f"Nama Desa: {feature['properties']['DESA']} KEPADATAN: {density}", parse_html=True)

# Urutkan fitur berdasarkan kepadatan dari tinggi ke rendah
sorted_features = sorted(geojson_data['features'], key=lambda x: x['properties']['KEPADATAN'], reverse=True)

# Buat daftar warna sesuai urutan fitur yang diurutkan
feature_colors = {feature['properties']['DESA']: colors_gray[i] for i, feature in enumerate(sorted_features)}

# Membuat peta Folium
m = folium.Map(location=default_location, zoom_start=zoom_start)

# Menambahkan data GeoJSON ke peta dengan warna abu-abu dan popup
for feature in sorted_features:
    desa_name = feature['properties']['DESA']
    color = feature_colors[desa_name]
    
    style_function = lambda x, color=color: {
        'fillColor': color,
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7,
    }
    
    geojson_layer = folium.GeoJson(
        feature,
        style_function=style_function,
        popup=popup_function(feature)
    )
    geojson_layer.add_to(m)

for loc_name, loc_coords in location_options.items():
    folium.Marker(
        location=loc_coords,
        popup=loc_name,
        icon=folium.Icon(icon="info-sign"),
    ).add_to(m)

# Menyimpan peta ke file HTML sementara
m.save('index.html')

# Membaca konten HTML dari file
with open('index.html', 'r', encoding='utf-8') as f:
    map_html = f.read()

# Menampilkan peta di Streamlit menggunakan komponen HTML
html(map_html, height=600)

# Menampilkan judul untuk peta
st.write("Peta dengan skala warna merah berdasarkan kepadatan penduduk, dari paling gelap ke paling pudar")
