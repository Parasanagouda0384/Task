import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. API Configuration ---
API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'  # Placeholder for API Key
CITIES = ['London', 'New York', 'Tokyo', 'Paris', 'Mumbai']
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather_data(cities):
    weather_list = []
    for city in cities:
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'  # Fetching temperature in Celsius
        }
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extracting relevant fields
            weather_list.append({
                'City': city,
                'Temperature': data['main']['temp'],
                'Humidity': data['main']['humidity'],
                'Pressure': data['main']['pressure'],
                'Condition': data['weather'][0]['main']
            })
        except Exception as e:
            print(f"Error fetching data for {city}: {e}")
            
    return pd.DataFrame(weather_list)

# --- 2. Data Processing ---
df = fetch_weather_data(CITIES)

# --- 3. Visualization ---
# Setting the visual style
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Weather Data Visualization Dashboard', fontsize=20)

# Plot 1: Temperature Comparison (Bar Chart)
sns.barplot(x='City', y='Temperature', data=df, ax=axes[0, 0], palette='coolwarm')
axes[0, 0].set_title('City vs Temperature (°C)')
axes[0, 0].set_ylabel('Temperature (°C)')

# Plot 2: Humidity Levels (Bar Chart)
sns.barplot(x='City', y='Humidity', data=df, ax=axes[0, 1], palette='Blues_d')
axes[0, 1].set_title('City vs Humidity (%)')
axes[0, 1].set_ylabel('Humidity (%)')

# Plot 3: Humidity Distribution (Pie Chart)
axes[1, 0].pie(df['Humidity'], labels=df['City'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
axes[1, 0].set_title('Humidity Distribution Share')

# Plot 4: Pressure Comparison (Scatter/Point Plot)
sns.scatterplot(x='City', y='Pressure', size='Temperature', data=df, ax=axes[1, 1], color='orange', sizes=(100, 400))
axes[1, 1].set_title('City vs Atmospheric Pressure (hPa)')

# Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# --- 4. Export ---
plt.savefig('weather_visualization.png')
print("Visualization saved as 'weather_visualization.png'")

# Display the plot
plt.show()
