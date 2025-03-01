import json
import os
from django.core.management.base import BaseCommand
from destinations.models import Destination

class Command(BaseCommand):
    help = 'Load cities data from cities_data.json into the Destination model'

    def handle(self, *args, **kwargs):
        # Get the path to the JSON file
        json_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), 'the_globetrotter_challenge-Backend/cities_data.json')
        
        self.stdout.write(self.style.SUCCESS(f'Loading data from {json_file_path}'))
        
        # Check if file exists
        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.ERROR(f'File not found: {json_file_path}'))
            return
        
        # Load the data
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                cities_data = json.load(file)
                
                # Track progress
                total = len(cities_data)
                self.stdout.write(self.style.SUCCESS(f'Found {total} cities in the JSON file'))
                
                # Clear existing data if needed
                if Destination.objects.exists():
                    confirm = input("Existing destinations found. Do you want to clear them before importing? (y/n): ")
                    if confirm.lower() == 'y':
                        Destination.objects.all().delete()
                        self.stdout.write(self.style.SUCCESS('Cleared existing destinations'))
                
                # Import the data
                count = 0
                for city_data in cities_data:
                    try:
                        Destination.objects.create(
                            city=city_data['city'],
                            country=city_data['country'],
                            clues=city_data['clues'],
                            fun_facts=city_data['fun_fact'],  # Note: JSON key is 'fun_fact' but model field is 'fun_facts'
                            trivia=city_data['trivia']
                        )
                        count += 1
                        if count % 50 == 0:
                            self.stdout.write(self.style.SUCCESS(f'Imported {count}/{total} cities'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f'Error importing {city_data.get("city", "unknown")}: {str(e)}'))
                
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} cities'))
        
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON file'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}')) 