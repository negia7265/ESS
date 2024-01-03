from flask import Flask, request, jsonify
from geopy.geocoders import GoogleV3
from geopy.distance import geodesic
app = Flask(__name__)

api_key = 'AIzaSyALB6uQiBGnyZAJMiS1MAT8ViJmRQea8W0'
geolocator = GoogleV3(api_key=api_key)


@app.route('/get_threshold_distances', methods=['POST'])
def get_threshold_distances():
    data = request.json
    source_name = data.get('source_name', '')
    destination_name = data.get('destination_name', '')
    office_name = data.get('office_name', '')
    # source_name = "2722+5RC, Kasturba Nagar 3rd Cross St, Venkata Rathnam Nagar Extension,Venkata Rathinam Nagar, Adyar, Chennai"
    # destination_name = "24, Gangadhar Chetty Rd, Rukmani Colony, Sivanchetti Gardens, Bengaluru, Karnataka 560042"
    # office_name = "AMR Tech Park II, No. 23 & 24, Hongasandra, Hosur Main Road, Bengaluru, Karnataka 560068"

    # Perform geocoding for both locations
    location1 = geolocator.geocode(source_name)
    location2 = geolocator.geocode(destination_name)
    location3 = geolocator.geocode(office_name)
    source_to_destination = geodesic(
        (location1.latitude, location1.longitude), (location2.latitude, location2.longitude)).meters
    source_to_office = geodesic((location1.latitude, location1.longitude),
                                (location3.latitude, location3.longitude)).meters
    destination_to_office = geodesic(
        (location2.latitude, location2.longitude), (location3.latitude, location3.longitude)).meters

    if location1 and location2:
        print(f"Location 1: {source_name}")
        print(
            f"Latitude: {location1.latitude}, Longitude: {location1.longitude}")
        print(f"Address: {location1.address}")

        print(f"\nLocation 2: {destination_name}")
        print(
            f"Latitude: {location2.latitude}, Longitude: {location2.longitude}")
        print(f"Address: {location2.address}")

        print(f"\nLocation 2: {office_name}")
        print(
            f"Latitude: {location3.latitude}, Longitude: {location3.longitude}")
        print(f"Address: {location3.address}")

        # Calculate the straight line distance between the source and destination
        print(f"\nStraight Line Distance: {source_to_destination:.2f} meters")
        print(f"\nStraight Line Distance: {source_to_office:.2f} meters")
        print(f"\nStraight Line Distance: {destination_to_office:.2f} meters")

        return jsonify({
            "source_to_destination": source_to_destination,
            "source_to_office": source_to_office,
            "destination_to_office": destination_to_office
        })
    else:
        return jsonify({"error": "Geocoding failed for one or both locations"}), 400


if __name__ == '__main__':
    app.run(debug=True)
