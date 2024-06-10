#!/usr/bin/env python
# coding: utf-8

# In[90]:


import streamlit as st
from python_weather import Client
import asyncio
import spacy
import openai
import config

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


# Set your OpenAI API key 
openai.api_key = config.OPENAI_API_KEY


# Function to get weather
async def get_weather(location):
    async with Client() as client:
        weather = await client.get(location)
        # Extract necessary attributes and store them in a dictionary
        weather_data = {
            "temperature": weather.temperature,
            "description": weather.description,
            "datetime": weather.datetime,
            "feels_like": weather.feels_like,
            "humidity": weather.humidity,
            "wind_speed": weather.wind_speed,
            "kind": weather.kind,
            "uv": weather.ultraviolet,
            "daily_forecasts": []
        }

        for daily in weather.daily_forecasts:
            daily_forecast = {
                "date": daily.date,
                "highest_temperature": daily.highest_temperature,
                "hourly_forecasts": daily.hourly_forecasts,
                "locale": daily.locale,
                "lowest_temperature": daily.lowest_temperature,
                "moon_illumination": daily.moon_illumination,
            }
            weather_data["daily_forecasts"].append(daily_forecast)

        return weather_data


# Function to generate weather response using GPT (updated)
async def get_weather_response(location, question):
    weather_data = await get_weather(location)
    
    # Access the necessary values directly from the dictionary
    temperature = weather_data["temperature"]
    description = weather_data["description"]
    forecast_datetime = weather_data["datetime"]
    feels_like = weather_data["feels_like"]
    humidity = weather_data["humidity"]
    wind_speed = weather_data["wind_speed"]
    kind = weather_data["kind"]
    uv = weather_data["uv"]

    prompt = f"""
    You are a weather chatbot. Given the following weather information and a question, provide a concise and informative answer.

    Location: {location}
    Temperature: {temperature}°C
    Description: {description}
    Date: {forecast_datetime}
    Feels Like: {feels_like}°C
    Humidity: {humidity}%
    Wind Speed: {wind_speed} km/h
    Kind: {kind}
    UV Index: {uv}

    Daily Forecasts:
    """
    
    for daily in weather_data['daily_forecasts']:
        prompt += f"""
        Date: {daily['date']}
        Highest Temperature: {daily['highest_temperature']}°C
        Lowest Temperature: {daily['lowest_temperature']}°C
        Moon Illumination: {daily['moon_illumination']}
        """
        
        # hourly forecasts
        for hourly in daily['hourly_forecasts']:
            prompt += f"""
            Time: {hourly.time}, Temperature: {hourly.temperature}°C, Description: {hourly.description}
            """
            
    prompt += f"""       
    Question: {question}
    Answer:
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()  # Updated response extraction


# Main function
def main():
    st.set_page_config(page_title="Weather Chatbot 🌤️", layout="wide")  # Set page config for wider layout

    # Weather Chatbot Header
    st.markdown(
        """
        <div id="weather-chatbot-header">
            <h1>Weather Chatbot 🌤️</h1>
            <div id="location-container">
                <span id="current-location">Default location: Berlin</span> 
                <i class="fa fa-info-circle" aria-hidden="true"></i>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    # Initialize location (default: Hamburg)
    if "location" not in st.session_state:
        st.session_state.location = "Berlin"

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input (updated to handle location changes)
    if prompt := st.chat_input("Ask me about the weather..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Location Change Detection (using spaCy for NER)
        doc = nlp(prompt)
        for ent in doc.ents:
            if ent.label_ == "GPE":  # GPE = Geopolitical Entity (location)
                new_location = ent.text
                st.session_state.location = new_location
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Location changed to {new_location}. Here's the weather forecast:"
                })
                break  # Stop after the first location is found
    
        # Get weather response
        response = asyncio.run(get_weather_response(st.session_state.location, prompt))  # Use updated location


        # Append bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

        # Scroll to the bottom of the chat container after new message
        st.markdown(
            """
            <script>
                const chat_container = document.querySelector('.css-ytpt3y.e1fqkh3o11');
                if (chat_container) {
                    chat_container.scrollTop = chat_container.scrollHeight;
                }
            </script>
            """,
            unsafe_allow_html=True,
        )
    
        # CSS for Fixed Header and Location Container
        st.markdown(
            """
            <style>
                #weather-chatbot-header {
                    position: initial;
                    top: 0;
                    width: 100%;
                    z-index: 1000;
                    background-color: #222326;
                    padding: 5px;
                }
                #location-container {
                    margin-left: 20px; 
                }
                .stApp { 
                    margin-top: 0px; 
                }
                #current-location {
                  color:white;
                }
                #location-instruction {
                    color:white;
                }
    
                .css-ytpt3y.e1fqkh3o11 {
                    overflow-y: auto;
                    height: 300px; /* or any height that you prefer */
                }
                .st-emotion-cache {
                    width: 100%;
                    inset: 1%;
                    min-width: auto;
                    max-width: initial;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )



if __name__ == "__main__":
    main()


# In[ ]:




