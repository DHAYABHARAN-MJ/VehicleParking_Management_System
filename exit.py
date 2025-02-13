import easyocr
import cv2
import mysql.connector
from datetime import datetime
import re
import tkinter as tk
from tkinter import messagebox

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'vehicle_parking'
}

# Initialize EasyOCR
reader = easyocr.Reader(['en'])

def is_valid_plate(text):
    # Improved regex pattern for Indian plate format (supports optional spaces)
    pattern = r'^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$'
    return re.match(pattern, text)

def calculate_rate(duration_minutes):
    rate_per_hour = 60 # Example rate per hour
    return (duration_minutes / 60) * rate_per_hour

def process_exit(car_number):
    # Remove spaces and convert to uppercase for consistency
    car_number = car_number.replace(" ", "").upper()

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Fetch the in_time for the car from the database
        cursor.execute("SELECT in_time FROM parking_records WHERE car_number = %s AND out_time IS NULL", (car_number,))
        result = cursor.fetchone()

        if result:
            in_time = result[0]
            out_time = datetime.now()
            duration = (out_time - in_time).total_seconds() / 60  # Duration in minutes
            rate = calculate_rate(duration)

            # Update the out_time in the database
            cursor.execute("UPDATE parking_records SET out_time = %s WHERE car_number = %s", (out_time, car_number))
            conn.commit()

            # Display details using Tkinter
            show_details_in_ui(car_number, in_time, out_time, duration, rate)
        else:
            print(f"No entry found for car number: {car_number}")
            messagebox.showinfo("Info", f"No entry found for car number: {car_number}")
        
        cursor.close()
        conn.close()
    except mysql.connector.Error as error:
        print("Database error:", error)
        messagebox.showerror("Error", f"Database error: {error}")

def show_details_in_ui(car_number, in_time, out_time, duration, rate):
    # Create a Tkinter window
    root = tk.Tk()
    root.title("Parking Details")

    # Convert duration to hours for display
    duration_hours = duration / 60

    # Create labels to display parking details
    tk.Label(root, text=f"Car Number: {car_number}", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5)
    tk.Label(root, text=f"In Time: {in_time}", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5)
    tk.Label(root, text=f"Out Time: {out_time}", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5)
    tk.Label(root, text=f"Total Duration (hrs): {duration_hours:.2f}", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=5)
    tk.Label(root, text=f"Total Cost: ₹{rate:.2f}", font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=5)

    # Add a button to close the window
    tk.Button(root, text="Close", command=root.destroy, font=("Arial", 12)).grid(row=5, column=0, pady=10)

    root.mainloop()

def preprocess_image(frame):
    """Preprocess image to improve OCR accuracy."""
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Increase contrast using histogram equalization
    enhanced = cv2.equalizeHist(blurred)

    return enhanced

# Initialize the camera feed
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame to improve OCR results
    preprocessed_frame = preprocess_image(frame)

    # Run EasyOCR on the preprocessed frame
    results = reader.readtext(preprocessed_frame)

    print("Detected text:", [text for (_, text, _) in results])  # Debugging output

    for (bbox, text, prob) in results:
        text = text.replace(" ", "").upper()  # Clean up detected text
        if is_valid_plate(text):
            print(f"Detected plate: {text} with confidence {prob:.2f}")
            process_exit(text)
            
            # Release the camera and close OpenCV windows
            cap.release()
            cv2.destroyAllWindows()
            break

    # Display the video feed
    cv2.imshow("Exit Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
