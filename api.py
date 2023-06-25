from flask import Flask
from flask import request
import flask
import vertexai
from vertexai.language_models import TextGenerationModel
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app, resources={f"/*": {"origins": "*"}})

vertexai.init(project="tattico-website", location="us-central1")
parameters = {
    "temperature": 0.2,
    "max_output_tokens": 256,
    "top_p": 0.8,
    "top_k": 40
}

@app.route("/generation", methods=["POST"])

def generate_listing():
    prompt = request.json["prompt"]
    description = palm_generate_description_response(prompt)
    price = palm_generate_price_response(prompt)
    title = palm_generate_title_response(prompt)
    shipping_option = palm_generate_shipping_option_response(prompt)


    response = flask.jsonify({
        "title": title,
         "price": price,
        "description": description,
        "shipping_option": shipping_option
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def palm_generate_description_response(prompt):
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        f"""
            Please generate a sales copy for a classifieds listing on an e-commerce website based on a user-given description of the object that they are trying to sell. This description should espouse the benefits the object that is being sold and try to sell it 
            input: {prompt}
            output: """,**parameters
    )
    return f"{response.text}"
def palm_generate_price_response(prompt):
    model = TextGenerationModel.from_pretrained("text-bison")
    response = model.predict(
        f"""I\'m wanting to either extract or estimate the price of various items for an e-commerce website based off of a short description of the object, the prices should just be returned by themselves. Please find these prices by looking up the product themselves and then estimating based on the provided condition. Please look up specific prices for New Zealand stores as New Zealand prices are typically much higher than a standard usd-NZD conversion would suggest, due to smaller economy of scale as well as shipping costs.
            If the price is given within the prompt, that price should be returned, otherwise provide an estimate based off of a google search and/or any information you have
        input: 2021 m1 MacBook Pro 16gb ram 500gb ssd good condition used for 1 year, pick up in Auckland
        output: 3000

        input: Brand new Lego Harry Potter Hogwarts castle, set number 71043. Box is in perfect condition and sealed, pick up only
        output: 750

        input: Apple studio display brand new in box - never used
        output: 3000

        input: brand new banana selling for 50000 pick up only
        output: 50000

        input: {prompt}
        output: 
        """,
        **parameters
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
if __name__ == "__main__":
    app.run(debug=True)




