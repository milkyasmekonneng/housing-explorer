# 🏠 Capital Crest Housing Explorer

An interactive real-estate analytics dashboard built with **Python, Shiny for Python, Pandas, and Plotly**.

The application allows users to explore properties in Addis Ababa, filter listings, analyze the housing market, compare properties, estimate mortgage payments, and save favorite properties.

## 🚀 Live Demo

**Live application:** Add your Posit Connect Cloud URL here

## ✨ Features

* 🔎 Property search and filtering
* 📍 Location-based property exploration
* 🏠 Property type filtering
* 💰 Maximum price filtering
* 📊 Interactive market analytics
* 🗺️ Interactive property location map
* 🏡 Detailed property information
* ❤️ Save favorite properties
* 💵 Mortgage payment estimator
* 📅 Request-a-viewing form
* 📱 Responsive design for desktop and mobile
* 📥 Download saved properties as CSV

## 🛠️ Technologies

* **Python**
* **Shiny for Python**
* **Pandas**
* **Plotly**
* **ShinyWidgets**
* **HTML**
* **CSS**
* **Git & GitHub**

## 📂 Project Structure

```text
housing-explorer/
├── app.py
├── requirements.txt
├── README.md
└── www/
    └── static assets
```

## ⚙️ Run Locally

Clone the repository:

```bash
git clone https://github.com/milkyasmekonneng/housing-explorer.git
cd housing-explorer
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
python -m shiny run --reload --port 8001 app.py
```

Then open the local URL shown in the terminal.

## 📊 Application Sections

### Market Overview

Displays key housing-market indicators including:

* Number of properties
* Average property price
* Lowest property price
* Highest property price

### Featured Properties

Users can browse available properties and view detailed information including:

* Location
* Property type
* Price
* Bedrooms
* Bathrooms
* Size
* Amenities

### Property Locations

An interactive map displays the geographical distribution of properties.

### Market Analytics

Interactive Plotly visualizations help users understand:

* Property type distribution
* Relationship between property size and price

### Mortgage Estimator

Users can estimate monthly mortgage payments by entering:

* Property price
* Down payment
* Interest rate
* Loan term

### Saved Properties

Users can save properties and download their saved listings as a CSV file.

## 🎯 Project Goals

This project demonstrates practical skills in:

* Python application development
* Data manipulation with Pandas
* Interactive data visualization
* Reactive web application development
* User interface design
* Git and GitHub workflow
* Cloud deployment

## 🔮 Future Improvements

Possible future improvements include:

* Real property database integration
* User authentication
* Database storage
* Advanced property search
* Real-time property listings
* Email notifications
* Agent and property-owner accounts
* Production API integration

## 👨‍💻 Author

**Milkyas Mekonnen**

GitHub: https://github.com/milkyasmekonneng

---

⭐ If you find this project interesting, feel free to explore the repository.
