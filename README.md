# 🌤️ Streamlit Weather Chatbot

This is an interactive weather chatbot built using Streamlit and OpenAI's GPT-3.5-turbo model. Chat with the bot to get real-time weather information and forecasts for various locations.

## Features

* **Natural Language Understanding:** Ask questions about the weather in a conversational way.
* **Real-time Weather Data:** Get up-to-date weather conditions (temperature, description, humidity, etc.).
* **Daily Forecasts:** See the weather outlook for the next few days.
* **Hourly Forecasts:** Get detailed hourly forecasts for the current day.
* **Location Updates:** Easily change the location for which you want weather information (just ask the chatbot).

## How to Use

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/diipak/streamlit-weather-chatbot.git](https://github.com/diipak/streamlit-weather-chatbot.git)

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt

3. **Set Up OpenAI API Key:**

* Create a config.py file in the project root directory.
* Add the following line, replacing YOUR_API_KEY with your actual OpenAI API key:

   ```Python
   OPENAI_API_KEY = 'YOUR_API_KEY'

4. **Run the App:**

   ```bash
   streamlit run weather_bot1.py

* If you are using localtunnel to make your app accessible, in another terminal:

   ```bash
   lt --port 8501 

5. **Start Chatting!**

* Type your questions about the weather in the chat input area. For example:
   * "What's the weather in Hamburg?"
   * "What's the forecast for tomorrow in Berlin?"
   * "Will it rain today?"
 

* **Technologies Used**
* Streamlit: For creating the interactive web application.
* python-weather: For fetching weather data from a reliable source.
* OpenAI's GPT-3.5-turbo: For natural language understanding and response generation.
* spaCy: For Named Entity Recognition (NER) to extract location information.




