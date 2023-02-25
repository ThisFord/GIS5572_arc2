from flask import Flask, jsonify
import psycopg2
app = Flask(__name__)

# Connect to the PostgreSQL database

#make a dictionary of credentials
pg_connect_dict = {
    'dbname' : 'lab0',
    'user' : 'postgres',
    'password' : 'your_pw',
    'host' : 'your_ip'
}

#unpack the dict above in the correct format using the ** method
conn = psycopg2.connect(**pg_connect_dict) 

#define the decorators
@app.route('/') #python decorator
def hello_world(): #function that app.route decorator references
  response = hello()
  return response

def hello():
  return "hello, world"

#define another decorator
@app.route('/geojson', methods=['POST', 'GET'])
def get_geojson():
    # Execute a query to retrieve the polygon from the database
    cursor = conn.cursor()
    cursor.execute("SELECT ST_AsGeoJSON(new_polygon.*) FROM new_polygon;")
    result = cursor.fetchall()
    return result[0][0]
    
    if result is None:
        return jsonify({'error': 'Polygon not found'}), 404
    else:
        return jsonify({'geojson': result[0]})
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

@app.route('/polygon/<polygon_id>', methods=['POST', 'GET'])
#define another page decorator
def get_polygon(polygon_id):
    
    cursor = conn.cursor()
    cursor.execute("SELECT ST_AsGeoJSON(geometry) FROM my_polygon WHERE polygon_id = %s;", (polygon_id,))
    result = cursor.fetchone()

 # Return the result as a GeoJSON object
    if result is None:
        return jsonify({'error': 'Polygon not found'}), 404
    else:
        return jsonify({'geojson': result[0]})
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
