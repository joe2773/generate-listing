Listing Generation App

This Flask-based application generates various fields for a listing on an e-commerce website based on user prompts. It utilizes the Vertex AI language model for text generation.

Prerequisites:
- Python 3.6 or higher
- pip package manager

Setup:
1. Clone the repository (or just copy the api.py and requirements.txt files):
   git clone <repository-url>
   cd listing-generation-app

2. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate

3. Install the required dependencies:
   pip install -r requirements.txt

4. Set up Google Cloud credentials:
   - Replace <path-to-service-account-key.json> in the code with the actual path to your service account key JSON file.
   - Alternatively, set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your service account key JSON file.

Running the App:
- To start the Flask server, run the following command:
   python app.py
- The app will be accessible at http://127.0.0.1:5000.

Usage:
- Use the /generation endpoint with a POST request to generate the listing fields.
- The request body should include a JSON object with a "prompt" key containing the user prompt.
- The generated fields will be returned as a JSON response.

Example Usage:
- Make a POST request to http://127.0.0.1:5000/generation with the following JSON body:
   {
     "prompt": "Please generate a listing for a brand new iPhone 12 Pro Max."
   }
- The response will include the generated fields:
   {
     "title": "Brand new iPhone 12 Pro Max",
     "price": "1099",
     "description": "Discover the latest iPhone 12 Pro Max, packed with advanced features and stunning design. Capture breathtaking photos, enjoy a vibrant Super Retina XDR display, and experience powerful performance. This top-of-the-line smartphone is the perfect companion for your digital lifestyle.",
     "shipping_option": "Pick up or shipping available"
   }

License: MIT
