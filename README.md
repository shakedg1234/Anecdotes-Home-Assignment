# Anecdotes Home Assignment

This plugin simulates an integration with a third-party API, collecting compliance evidence from the DummyJSON API.  

## What it does

The plugin performs:

1. Connectivity Test – Authenticates using DummyJSON's login endpoint.
2. Evidence Collection:
   - E1: Authenticated user details
   - E2: A list of 60 posts
   - E3: Comments for each post

## How to run

1. Clone the repository

2. Install dependencies using pip:
   pip install requests

3. Run the plugin:
   python main.py

4. The output will be saved to a file named:
   output.json

