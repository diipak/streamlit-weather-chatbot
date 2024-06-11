#!/usr/bin/env python
# coding: utf-8

# In[16]:


import streamlit as st
from python_weather import Client
import asyncio
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to get weather
async def get_weather(location, intent):
    async with Client() as client:
        weather = await client.get(location)
        
        if intent == "get_temperature":
            return (
                weather.temperature,
                weather.description,
                weather.humidity,
                weather.wind_speed,
                weather.pressure,
                weather.feels_like,
                weather.precipitation,
                weather.datetime.strftime("%Y-%m-%d"),
            )
        elif intent == "get_humidity":
            return weather.humidity, None, None, None, None, None, None, weather.datetime.strftime("%Y-%m-%d")
        elif intent == "get_wind_speed":
            return weather.wind_speed, None, None, None, None, None, None, weather.datetime.strftime("%Y-%m-%d")
        elif intent == "get_rain":
            return weather.precipitation, None, None, None, None, None, None, weather.datetime.strftime("%Y-%m-%d")
        else:
            return None, None, None, None, None, None, None, None

# Function to get intent and entities from user question
def get_intent_and_entities(question):
    doc = nlp(question)
    intent = "unknown"
    location = None


    # Intent recognition using keywords and patterns
    for token in doc:
        if token.lemma_.lower() in ["temperature", "weather", "hot", "cold", "warm"]:
            intent = "get_temperature"
        elif token.lemma_.lower() in ["humidity"]:
            intent = "get_humidity"
        elif token.lemma_.lower() in ["wind", "windy"]:
            intent = "get_wind_speed"
        elif token.lemma_.lower() in ["rain"]:
            intent = "get_rain"

    # Extract entities
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Geopolitical Entity (location)
            location = ent.text

    return intent, location

# Main function
def main():
    st.title("Weather Query Bot")

    location = st.text_input("Enter a location:", "Hamburg")  # Default to Hamburg
    question = st.text_input("Ask a weather question:")

    if st.button("Get Weather"):
        if not location:
            st.warning("Please enter a location.")
        else:
            intent, _ = get_intent_and_entities(question.lower())
            st.write(f"Recognized intent: {intent}, Location: {location}")
            result, description, humidity, wind_speed, pressure, feels_like, precipitation, date_retrieved = asyncio.run(get_weather(location, intent))
            if result is not None:
                if intent == "get_temperature":
                    st.write(f"The current weather in {location} on {date_retrieved} is {result}°C with {description}.")
                    st.write(f"Humidity: {humidity}%, Rain: {precipitation} mm, Wind Speed: {wind_speed} m/s, Pressure: {pressure} hPa, Feels Like: {feels_like}°C")
                elif intent == "get_humidity":
                    st.write(f"The humidity in {location} on {date_retrieved} is {result}%.")
                elif intent == "get_wind_speed":
                    st.write(f"The wind speed in {location} on {date_retrieved} is {result} m/s.")
                elif intent == "get_rain":
                    st.write(f"The rain in {location} on {date_retrieved} is {result} mm.")
            else:
                st.write("I'm sorry, I didn't understand your question.")

if __name__ == "__main__":
    main()


# In[ ]:




