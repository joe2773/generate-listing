from flask import Flask
from flask import request
import flask
import vertexai
from vertexai.language_models import TextGenerationModel
from flask_cors import CORS, cross_origin
import re
from google.cloud import storage
from google.oauth2 import service_account

app = Flask(__name__)
CORS(app, resources={f"/*": {"origins": "*"}})

# Replace the following lines with the path to your service account JSON key file


vertexai.init(credentials=service_account.Credentials.from_service_account_file("<path-to-your-file>.json"),project="listing-generation", location="us-central1")
vertexai.init(project="listing-generation", location="us-central1")
parameters = {
    "temperature": 0.2,
    "max_output_tokens": 256,
    "top_p": 0.8,
    "top_k": 40
}

@app.route("/generation", methods=["POST"])
def generate_listing():
    prompt = request.json["prompt"]
    response = palm_generate_listing_response(prompt)
    description = extract_field(response,"description")
    price = extract_field(response,"price")
    title = extract_field(response,"title")
    shipping_option = extract_field(response,"shipping_option")


    response = flask.jsonify({
        "title": title,
         "price": price,
        "description": description,
        "shipping_option": shipping_option
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def palm_generate_listing_response(prompt):
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        f"""
            I\'m wanting to generate a number of fields for a listing for an e-commerce website. These fields should be generated based off of two things: a prompt provided as a string, AND a boolean field representing each of the listing fields which indicate whether that field should be generated or not. 
            The possible fields are as follows:
            title,
            description,
            price,
            shipping_option
            I will now provide context for each of the fields:

            title: I\'m wanting to create a title for my e-commerce website classifieds listing that will help me sell the given object, it should be less than 50 characters long and give a succinct and catch overview of the object that is being sold.

            description:
            Please generate a sales copy for a classifieds listing on an e-commerce website based on a user-given description of the object that they are trying to sell. This description should espouse the benefits the object that is being sold and try to sell it, maximum length is 500 characters and it should be engaging and entertaining while also being accurate and providing all the necessary information about the product

            price: 
            I\'m wanting to either extract or estimate the price of various items for an e-commerce website based off of a short description of the object, the prices should just be returned by themselves. Please find these prices by looking up the product themselves and then estimating based on the provided condition. Please look up specific prices for New Zealand stores as New Zealand prices are typically much higher than a standard usd-NZD conversion would suggest, due to smaller economy of scale as well as shipping costs.
            If the price is given within the prompt, that price should be returned, otherwise provide an estimate based off of a google search and/or any information you have

            shipping_option
            I'm wanting to determine the shipping options for a classified listing that a user is wanting to list on my e-commerce website. The shipping options are as follows: pick up only, shipping nationwide only, pick up or shipping available the default should be pick up or shipping available if nothing explicit is mentioned around shipping

            input: Brand new Lego Harry Potter Hogwarts castle, set number 71043. Box is in perfect condition and sealed, pick up only
            output: title: Lego Harry Potter hogwarts brand new sealed set number 71043
            price: 750
            description: Discover the magic of LEGO Harry Potter with the highly sought-after Hogwarts Castle set (71043)! Brand new and sealed in its original box, this enchanting masterpiece awaits its rightful owner. Immerse yourself in the world of wizardry as you build and explore the intricately detailed castle, complete with iconic locations from the beloved series. This collector\'s item is a must-have for any Harry Potter enthusiast or LEGO collector. Don\'t miss your chance to own this timeless treasure—unlock your imagination and embark on an extraordinary journey today! Limited stock available. Order now and experience the magic of LEGO Harry Potter firsthand!
            shipping_option: pick up only

            input: 1998 porsche 911 10000kms good condition metallic blue, pick up only in Auckland
            output: title: 1998 Porsche 911
            price: 100000
            description: 1998 Porsche 911 in metallic blue with 10000kms on the clock. This car is in excellent condition and has been well maintained. It is a pleasure to drive and is sure to turn heads wherever you go. This car is being sold for pick up only in Auckland.
            shipping_option: pick up only


            input: lego saturn v in great condition brand new pick up or shipping available from Auckland
            output: title: Lego Saturn V
            price: 500
            description: Lego Saturn V in great condition, brand new. This is a great set for any Lego fan or space enthusiast. It is also a great gift for any occasion. This set is pick up or shipping available from Auckland.
            shipping_option: pick up or shipping available

            input: {prompt}
            output:
        """,
        **parameters
    )
    return f"{response.text}"
def palm_generate_description_response(prompt):
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        f"""
            Please generate a sales copy for a classifieds listing on an e-commerce website based on a user-given description of the object that they are trying to sell. This description should espouse the benefits the object that is being sold and try to sell it, it should be engaging and entertaining while also being accurate and providing all the necessary information about the product
            input: {prompt}
            output: """,**parameters
    )
    return f"{response.text}"
def palm_generate_price_response(prompt):
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
       {prompt}
    )
    return f"{response.text}"

def palm_generate_title_response(prompt):
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        f""" I\'m wanting to create a title for my e-commerce website classifieds listing that will help me sell the given object, it should be less than 50 characters long and give a succinct and catch overview of the object that is being sold.
        input: Im wanting to sell a 2021 M1 macbook pro 16 inch 16gb memory 500gb SSD, cash only pickup auckland. It is in great condition and I've only used for a year, selling as I have upgraded to the latest M2 macbook pro , no issues at all on this computer and 3 months warranty remaining. Can provide receipts.
        ouput: 2021 M1 Macbook pro 16-inch great condition 16gb RAM 500gb ssd
        input: {prompt}
        output:
          """,
          **parameters
    )
    return f"{response.text}"

def palm_generate_shipping_option_response(prompt):
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        f""" I\'m wanting to determine the shipping options for a classified listing that a user is wanting to list on my e-commerce website. The shipping options are as follows: pick up only, shipping nationwide only, pick up or shipping available the default should be pick up or shipping available if nothing explicit is mentioned around shipping
        input: I am selling a vintage collection of coke cans for 500$ asking price, they are available for pick up only in auckland central, perfect condition never opened
        output: pick up only

        input: I am selling a vintage porsche 911 1998 50000kms
        output: pick up or shipping available

        input: selling a lego saturn v brand new condition, shipping available to north or south islands
        output: shipping nationwide only
        
        input: {prompt}
        output: """,
        
        **parameters
    )
    return f"{response.text}"

def extract_field(string, field_name):
    """Extracts the value of the specified field from the string.

    Args:
        string: The string to extract the field from.
        field_name: The name of the field to extract.

    Returns:
        The value of the field.
    """

    regex = r"{field_name}: (.*)".format(field_name=field_name)
    match = re.search(regex, string)
    if match is not None:
        return match.group(1)
    
if __name__ == "__main__":
    app.run(debug=True)
