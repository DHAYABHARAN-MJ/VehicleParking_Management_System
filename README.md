# 🚗 Vehicle Parking Management System with Real-time Motion Surveillance
# link: https://vehicleparkingmanagement.netlify.app/

## 🌟 Overview
The **Vehicle Parking Management System** is a modern, automated solution integrating **real-time motion surveillance** and **automatic number plate detection**. It efficiently tracks vehicle **entry & exit**, calculates **parking fees**, and manages **available slots** dynamically.

---

## 🔧 Features & Modules

### 📌 1. Database Creation
✅ SQL Table Includes:
- 🚘 **Car Number**
- ⏳ **In Time & Out Time**
- 📅 **Date**
- ⏱️ **Total Hours Parked**
- 💰 **Parking Rate**

### 🌐 2. Web Page Creation
🔹 **Login Page**: Secure login with Permanent ID & Password (modifiable in future).  
🔹 **Main Dashboard**:
- 🔍 **Search & Sort Vehicles**
- 📊 **Live Tracking of Parked Vehicles**
- 📂 **Date-range Filter**
- 📑 **Real-time Table Display:**
  - 🚗 Car Number
  - ⏳ In/Out Time
  - ⏱️ Total Hours
  - 💰 Parking Rate

### 📷 3. Number Plate Detection
- 🏷️ **EasyOCR-based License Plate Recognition**
- 🔄 **Auto-logs Car Number & Timestamp in SQL Database**

---

## 🚀 How It Works

### 🔹 **Entry Process**
1️⃣ Camera captures **vehicle plate**.  
2️⃣ OCR processes the plate & updates the **database**.  
3️⃣ Available **parking slots** are updated in real-time.  

### 🔹 **Admin Dashboard**
📌 Displays **Total Parking Slots**.  
📌 Updates slot count as vehicles enter/exit.  

### 🔹 **Exit Process**
1️⃣ Exit camera scans **plate number**.  
2️⃣ Fetches **entry time** & calculates **parking fee**.  
3️⃣ Displays **amount to be paid** before exit.  
4️⃣ Opens gate & logs **exit timestamp**.  

---

## 🛠️ Tech Stack
✅ **Backend**: PHP, MySQL  
✅ **Frontend**: HTML, CSS, JavaScript  
✅ **OCR**: EasyOCR (Python)  
✅ **Server**: XAMPP / Apache  
✅ **Version Control**: GitHub  

---

## 📥 Installation & Setup
1️⃣ **Clone the Repository:**  
   ```sh
   git clone https://github.com/DHAYABHARAN-MJ/VehicleParking_Management_System.git
   ```
2️⃣ **Navigate to Project Directory:**  
   ```sh
   cd VehicleParking_Management_System
   ```
3️⃣ **Set Up the Database:**  
   - Import the provided SQL file into MySQL.  
4️⃣ **Install Dependencies:**  
   ```sh
   pip install easyocr
   ```
5️⃣ **Run the Server:**  
   ```sh
   php -S localhost:8000
   ```
6️⃣ **Access the System:**  
   🌐 Open: `http://localhost:8000`

---

## 🚀 Future Enhancements
✅ **Mobile App Integration** 📱  
✅ **AI-based Parking Slot Detection** 🤖  
✅ **Payment Gateway for Auto-Billing** 💳  

---
