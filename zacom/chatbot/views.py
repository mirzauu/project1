from django.shortcuts import render
from products.models import Product_Variant
from django.core import serializers
import json
import random
# Create your views here.
# views.py

from django.http import JsonResponse
import requests

from django.shortcuts import render
from chatbot.forms import ChatForm
from wit import Wit

def webhook_view(request):

    if 'chat_history' in request.session:
        chat_history = request.session['chat_history']
    else:
        chat_history = {}

    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('messages')
        WIT_ACCESS_TOKEN = 'Z6VMMBMMZUSCUFM6USZWY54HPF2O2Q6A'
        client = Wit(WIT_ACCESS_TOKEN)
        response = client.message(user_message)

        print('intents',response['intents'])
        print('entities',response['entities'])

        intents = response['intents']
        entities = response['entities']


        available=False
        link = '#'

        if intents:
            intent_name = intents[0]['name']
            print(f"Intent: {intent_name}")  

            if intent_name == 'SearchProduct':
                print('hi')
                response = search_product(intent_name, entities)
                bot_response=response[0]
                link=response[1]
                available=response[2]

            elif intent_name == 'SearchOrder':
                print('ordeer')
                # bot_response = search_order(intent_name, entities)
                bot_response="i didn't get that 😔" 
            else:
                bot_response="i didn't get that 😔,its not in my control"   


        if entities:
            for entity_name, entity_values in entities.items():
                print(f"Entity: {entity_name}")
                for entity_value in entity_values:
                    print(f"Value: {entity_value['value']}, Confidence: {entity_value['confidence']}")
        
        chat_history[user_message]=bot_response
        request.session['chat_history'] = chat_history  # Update chat_history in the session

        return JsonResponse({'message': bot_response,'available':available,'link':link})
    
    else:

        return JsonResponse({'error': 'Only POST requests are allowed'})

def search_product(intent, entities):

    for entity_name, entity_values in entities.items():
            print(f"Entity: {entity_name}")
            for entity_value in entity_values:
                print(f"Value: {entity_value['value']}, Confidence: {entity_value['confidence']}")
                product_search=entity_value['value']
                Confidence=entity_value['confidence']
                
   
    try:
        products = Product_Variant.objects.filter(product__product_name__icontains=product_search).first()
       
        if products is not None:  # Check if any matching products were found
            if Confidence > 0.8:
                product=generate_random_response(products.product.product_name, products.sale_price)
            elif Confidence < 0.8:
                product = f": {products.product.product_name}, of price : {products.sale_price} this is the similar product "
            else:
                pass
            available=True
            link = products.product_variant_slug
        else:
            product = 'No products available '
            available=False
            link = '#'

    except Product_Variant.DoesNotExist:
        product = None

    if not product:
        product = 'No products available 😞'
        available=False
        link = '#'
    return product,link,available

def search_order(intent, entities):

    for entity_name, entity_values in entities.items():
            print(f"Entity: {entity_name}")
            for entity_value in entity_values:
                print(f"Value: {entity_value['value']}, Confidence: {entity_value['confidence']}")
                product_search=entity_value['value']
                Confidence=entity_value['confidence']
                print
   
    try:
        products = Product_Variant.objects.filter(product__product_name__icontains=product_search).first()
        available=True
        link = products.product_variant_slug
        if products is not None:  # Check if any matching products were found
            if Confidence > 0.8:
                product=generate_random_response(products.product.product_name, products.sale_price)
            elif Confidence < 0.8:
                product = f": {products.product.product_name}, of price : {products.sale_price} this is the similar product "
            else:
                pass
            link = "https://example.com"
        else:
            product = 'No products available'

    except Product_Variant.DoesNotExist:
        product = None

    if not product:
        product = 'No products available'

    return product,link,available




def generate_random_response(product_name, sale_price):
    responses = [
        f"Yes, it's available 😊: {product_name}, price: {sale_price}",
        f"We have it in stock 😊: {product_name}, priced at {sale_price}",
        f"Sure, we've got it 😊: {product_name}, costs {sale_price}",
        f"Available now 😊: {product_name}, selling for {sale_price}",
        f"In stock 😊: {product_name}, priced {sale_price}",
        f"You're in luck! We have it 😊: {product_name}, price: {sale_price}",
        f"It's here! 😊: {product_name}, priced at {sale_price}",
        f"Yes, we've got it! 😊: {product_name}, price is {sale_price}",
        f"Good news! It's available 😊: {product_name}, price: {sale_price}",
        f"It's ready for you! 😊: {product_name}, priced {sale_price}"
    ]
    return random.choice(responses)