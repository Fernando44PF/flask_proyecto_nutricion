class Config:
    SECRET_KEY = 'clave_secreta_super_segura'
    
    # MySQL Configuration
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '54321'
    MYSQL_DB = 'gestion_nutricion'
    MYSQL_CURSORCLASS = 'DictCursor'
    
    # YouTube API
    YOUTUBE_API_KEY = 'AIzaSyCv07KwHW3vgHk7-7sSAvncX4ILNHNkKlQ' 
    
    # OpenStreetMap / Nominatim Configuration
    OSM_USER_AGENT = 'NutriApp/1.0 (contacto@nutriapp.com)'  # Identificador único [citation:2][citation:7]
    OSM_TIMEOUT = 10  # Timeout para solicitudes [citation:2]
    
    
