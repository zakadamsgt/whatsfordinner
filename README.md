# What in the World is for Dinner?

Welcome to my project! The goal is to leverage AI to create a recipe generator that utilizes available ingredients in your house and provides local or ethnic dish recommendations based on your address.

## How It Works
This application allows you to input your available ingredients and location. It then generates recipe suggestions tailored to your preferences and the local cuisine.

## Current Status
The current script is functional but needs significant updates:
- Improved formatting for LLM responses
- Nutrional calculation per serving
- Ability to save generated recipes into a project folder

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/whatsfordinner.git
   cd whatsfordinner

2. Create a `.env` file in the project directory and include your own API keys:

   ```bash
   OPENAI_API_KEY=your_openai_api_key
   OPENCAGE_API_KEY=your_opencage_api_key
   OPENWEATHER_API_KEY=your_openweather_api_key


3. Run the application to get recipe suggestions based on your inputs.



