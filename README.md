# Route Recommendation System (In development)

A comprehensive route recommendation system for that provides personalized route suggestions based on user preferences, traffic conditions, and Points of Interest (POIs).

## Overview

This project implements a data-driven route recommendation system that considers multiple factors when suggesting optimal routes:

- **User Preferences**: Time, distance, safety, scenery, and route simplicity
- **Traffic Conditions**: Real-time traffic simulation based on time of day and road type
- **Points of Interest**: Proximity to parks, restaurants, gas stations, hospitals, and other amenities
- **Road Network Features**: Road type, speed limits, lanes, and other infrastructure characteristics

## Features

### 1. Road Network Processing

- Downloads road networks from OpenStreetMap using OSMnx
- Extracts road features (speed, length, road type, lanes, etc.)
- Supports multiple network types (drive, walk, bike)
- Saves data in multiple formats (GraphML, Pickle, GeoPackage)

### 2. Points of Interest (POIs)

- Downloads various POI categories:
  - Parks and recreational areas
  - Restaurants and cafes
  - Gas stations
  - Hospitals and healthcare facilities
  - Schools and educational institutions
  - Banks and financial services
  - Historic sites and tourist attractions
- Calculates proximity metrics for routes

### 3. User Profile System

- Generates diverse user profiles with different preference archetypes:
  - **Time-focused**: Prioritizes fastest routes
  - **Safety-focused**: Prioritizes safer roads
  - **Scenic-focused**: Prioritizes scenic routes
  - **Simple-focused**: Prefers routes with fewer turns
  - **Balanced**: Balanced preferences across all factors
- Tracks user route history
- Supports preference updates and constraints

### 4. Traffic Simulation

- Simulates traffic conditions based on:
  - Time of day (rush hours, off-peak, late night)
  - Day of week (weekday vs weekend patterns)
  - Road type (motorway, primary, secondary, residential)
- Applies traffic multipliers to travel times
- Supports real-time traffic updates

### 5. Visualization

- Interactive network visualization using Folium
- Static network plots using OSMnx
- Network statistics and analysis
