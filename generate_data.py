import json
import os
import random
import time
from openai import OpenAI

# Initialize the OpenAI client - you'll need to set your API key as an environment variable
client = OpenAI(api_key="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")

def generate_city_entry(existing_cities=None):
    if existing_cities is None:
        existing_cities = []
    
    # Create a prompt for OpenAI to generate a new city entry
    prompt = f"""
    Generate a single JSON object for a city with the following structure:
    {{
        "city": "CityName",
        "country": "CountryName",
        "clues": [
            "First clue about the city that hints at a famous landmark.",
            "Second clue about what the city is known for."
        ],
        "fun_fact": [
            "An interesting and surprising fact about the city!",
            "A second fun fact about the city."
        ],
        "trivia": [
            "A piece of trivia about local food or culture.",
            "A historical or geographical trivia fact about the city."
        ]
    }}
    
    Rules:
    1. Use a real city that is not in this list: {', '.join(existing_cities)}
    2. Make sure the clues are distinctive enough to identify the city
    3. Ensure fun facts are surprising and not commonly known
    4. Make the trivia interesting and educational
    5. Return ONLY the JSON object with no other text
    """
    
    # Call the OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # or use "gpt-3.5-turbo" for a less expensive option
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates travel information data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        # Extract the JSON from the response
        city_data_str = response.choices[0].message.content.strip()
        
        # Handle cases where the API might include markdown formatting
        if city_data_str.startswith("```json"):
            city_data_str = city_data_str.replace("```json", "", 1)
        if city_data_str.endswith("```"):
            city_data_str = city_data_str[:-3]
        
        city_data_str = city_data_str.strip()
        
        # Parse the JSON
        city_data = json.loads(city_data_str)
        return city_data
    
    except Exception as e:
        print(f"Error generating city entry: {e}")
        return None

def generate_cities_dataset(num_cities=100):
    cities_data = []
    existing_city_names = []
    
    # First, add the three example cities
    example_cities = [
        {
            "city": "Paris",
            "country": "France",
            "clues": [
                "This city is home to a famous tower that sparkles every night.",
                "Known as the 'City of Love' and a hub for fashion and art."
            ],
            "fun_fact": [
                "The Eiffel Tower was supposed to be dismantled after 20 years but was saved because it was useful for radio transmissions!",
                "Paris has only one stop sign in the entire city—most intersections rely on priority-to-the-right rules."
            ],
            "trivia": [
                "This city is famous for its croissants and macarons. Bon appétit!",
                "Paris was originally a Roman city called Lutetia."
            ]
        },
        {
            "city": "Tokyo",
            "country": "Japan",
            "clues": [
                "This city has the busiest pedestrian crossing in the world.",
                "You can visit an entire district dedicated to anime, manga, and gaming."
            ],
            "fun_fact": [
                "Tokyo was originally a small fishing village called Edo before becoming the bustling capital it is today!",
                "More than 14 million people live in Tokyo, making it one of the most populous cities in the world."
            ],
            "trivia": [
                "The city has over 160,000 restaurants, more than any other city in the world.",
                "Tokyo's subway system is so efficient that train delays of just a few minutes come with formal apologies."
            ]
        },
        {
            "city": "New York",
            "country": "USA",
            "clues": [
                "Home to a green statue gifted by France in the 1800s.",
                "Nicknamed 'The Big Apple' and known for its Broadway theaters."
            ],
            "fun_fact": [
                "The Statue of Liberty was originally a copper color before oxidizing to its iconic green patina.",
                "Times Square was once called Longacre Square before being renamed in 1904."
            ],
            "trivia": [
                "New York City has 468 subway stations, making it one of the most complex transit systems in the world.",
                "The Empire State Building has its own zip code: 10118."
            ]
        }
    ]
    
    cities_data.extend(example_cities)
    existing_city_names = [city["city"] for city in example_cities]
    
    # Generate the remaining cities
    remaining_cities = num_cities - len(cities_data)
    print(f"Generating {remaining_cities} new city entries...")
    
    for i in range(remaining_cities):
        print(f"Generating city {i+1}/{remaining_cities}...")
        
        city_data = None
        retry_count = 0
        max_retries = 3
        
        while city_data is None and retry_count < max_retries:
            city_data = generate_city_entry(existing_city_names)
            
            if city_data is not None:
                # Check if this city is already in our list
                if city_data["city"] in existing_city_names:
                    print(f"Duplicate city generated: {city_data['city']}. Retrying...")
                    city_data = None
                    retry_count += 1
                else:
                    cities_data.append(city_data)
                    print(city_data)
                    existing_city_names.append(city_data["city"])
                    # Add a small delay to avoid rate limits
                    time.sleep(0.5)
            else:
                retry_count += 1
                time.sleep(1)  # Wait a bit longer if there was an error
        
        if city_data is None:
            print(f"Failed to generate city after {max_retries} retries. Skipping.")
    
    # Save the data to a JSON file
    with open("cities_data.json", "w", encoding="utf-8") as f:
        json.dump(cities_data, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(cities_data)} city entries saved to 'cities_data.json'")
    return cities_data

if __name__ == "__main__":    
    generate_cities_dataset(100)