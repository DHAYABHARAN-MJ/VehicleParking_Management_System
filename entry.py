import easyocr
import cv2
import mysql.connector
from datetime import datetime
import re

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'vehicle_parking'
}   

# Initialize EasyOCR and video feed
reader = easyocr.Reader(['en'])
cap = cv2.VideoCapture(0)  # Use 0 for the default camera

def is_valid_plate(text):
    # Improved regex pattern for Indian number plates (supports spaces)
    pattern = r'^[A-Z]{2}\s?\d{1,2}\s?[A-Z]{1,2}\s?\d{4}$'
    return re.match(pattern, text)

def insert_to_db(plate_text):
    try:
        # Remove spaces from the detected plate text
        cleaned_plate = plate_text.replace(" ", "")
        
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # Get the current time and date
        in_time = datetime.now()
        date = in_time.date()
        
        # SQL query to insert data
        sql = "INSERT INTO parking_records (car_number, in_time, date) VALUES (%s, %s, %s)"
        values = (cleaned_plate, in_time, date)
        cursor.execute(sql, values)
        connection.commit()
        print(f"Data inserted successfully: {cleaned_plate}")
    except mysql.connector.Error as error:
        print("Failed to insert data into database:", error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Start processing the video feed
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame to improve processing speed
    frame = cv2.resize(frame, (640, 480))

    # Run EasyOCR on the frame
    results = reader.readtext(frame)
    print("Detected text:", [text for (_, text, _) in results])  # Debugging output

    for (bbox, text, prob) in results:
        if is_valid_plate(text):
            print(f"Detected plate: {text} with confidence {prob:.2f}")
            
            # Insert the cleaned plate text to the database
            insert_to_db(text)
            
            # Release resources after detecting the first valid plate
            cap.release()
            cv2.destroyAllWindows()
            break

    # Display the video feed with detected text
    cv2.imshow("Vehicle Parking System", frame)
    
    # Press 'q' to exit the video feed manually
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
