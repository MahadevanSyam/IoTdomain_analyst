from flask import Flask, render_template, Response, jsonify, request
import cv2

app = Flask(_name_)

# Placeholder for sensor data
sensor_data = {'heartRate': 0, 'temperature': 0}

# Placeholder for heart rate history
heart_rate_history = []

@app.route("/")
def IOTpage():
    return render_template("index.html")

def generate_frames():
    camera = cv2.VideoCapture(0)  # Open webcam
    while True:
        success, frame = camera.read()
        if not success:
            break

        # Get sensor data from Arduino
        heart_rate = sensor_data['heartRate']
        temperature = sensor_data['temperature']

        # Draw sensor data on the frame
        cv2.putText(frame, f"Heart Rate: {heart_rate}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, f"Temperature: {temperature}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()  # Release the webcam when done

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/data', methods=['GET', 'POST'])  # Add this route to receive data from ESP32
def handle_data():
    if request.method == 'GET':
        # Return sensor data as JSON
        return jsonify(sensor_data)
    elif request.method == 'POST':
        # Handle POST request to update sensor data
        data = request.json
        sensor_data['heartRate'] = data['heartRate']
        sensor_data['temperature'] = data['temperature']
        heart_rate_history.append(data['heartRate'])  # Add heart rate to history
        return "Data received successfully"

@app.route('/sensor_data')
def get_sensor_data():
    return jsonify(sensor_data)


if _name_ == "_main_":
    app.run(host='0.0.0.0', port=7720, debug=True)