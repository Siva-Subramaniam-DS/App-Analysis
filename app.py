from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
import random
from bson import ObjectId
from sentimental import get_sentiment
from analysis import load_and_process_data
from Eda import perform_eda
from helobot import chain
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)

# Configure MongoDB connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/Store"
mongo = PyMongo(app)

def load_feedback():
    with open('positive.txt', 'r') as file:
        positive_feedback = [line.strip() for line in file.readlines()]
    with open('negative.txt', 'r') as file:
        negative_feedback = [line.strip() for line in file.readlines()]
    return positive_feedback, negative_feedback

positive_feedback, negative_feedback = load_feedback()


@app.route("/heloai", methods=["POST"])
def heloai():
    data = request.get_json()
    user_input = data["question"]
    context = ""  # Context can be stored and updated as per your needs
    result = chain.invoke({"context": context, "question": user_input})
    return jsonify({"answer": result})

def convert_objectid_to_str(data):
    if isinstance(data, list):
        for item in data:
            convert_objectid_to_str(item)
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            elif isinstance(value, dict):
                convert_objectid_to_str(value)
            elif isinstance(value, list):
                convert_objectid_to_str(value)
    return data

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/infiniteScroll')
def infinite_scroll():
    return render_template('infiniteScroll.html')




@app.route('/AppSearch', methods=['GET', 'POST'])
def index():
    app_info = None
    playstore_info = None
    applestore_info = None
    comparison = False
    error_message = None
    feedback_playstore = None
    feedback_applestore = None
    feedback_sentiment_playstore = None
    feedback_sentiment_applestore = None
    playstore_comparison = None
    applestore_comparison = None

    if request.method == 'POST':
        app_name = request.form.get('app_name')
        store = request.form.get('store')

        if app_name and store:
            db = mongo.db
            if store == 'playstore':
                filtered_playstore = db.googleplaystore.find_one({"App": {"$regex": app_name, "$options": "i"}})
                if filtered_playstore:
                    playstore_info = filtered_playstore
                    feedback_playstore = random.choice(positive_feedback + negative_feedback)
                    feedback_sentiment_playstore = get_sentiment([feedback_playstore])
                else:
                    error_message = "App not found in Google Play Store."

            elif store == 'applestore':
                filtered_applestore = db.applestore.find_one({"track_name": {"$regex": app_name, "$options": "i"}})
                if filtered_applestore:
                    applestore_info = filtered_applestore
                    feedback_applestore = random.choice(positive_feedback + negative_feedback)
                    feedback_sentiment_applestore = get_sentiment([feedback_applestore])
                else:
                    error_message = "App not found in Apple App Store."

            elif store == 'both':
                filtered_playstore = db.googleplaystore.find_one({"App": {"$regex": app_name, "$options": "i"}})
                filtered_applestore = db.applestore.find_one({"track_name": {"$regex": app_name, "$options": "i"}})
                
                if filtered_playstore and filtered_applestore:
                    playstore_info = filtered_playstore
                    applestore_info = filtered_applestore
                    comparison = True
                    feedback_playstore = random.choice(positive_feedback + negative_feedback)
                    feedback_applestore = random.choice(positive_feedback + negative_feedback)
                    feedback_sentiment_playstore = get_sentiment([feedback_playstore])
                    feedback_sentiment_applestore = get_sentiment([feedback_applestore])
                elif not filtered_playstore:
                    error_message = "App not found in Google Play Store."
                elif not filtered_applestore:
                    error_message = "App not found in Apple App Store."
                else:
                    error_message = "App not found in both stores."

    return render_template(
        'app.html',
        playstore_info=playstore_info,
        applestore_info=applestore_info,
        comparison=comparison,
        error_message=error_message,
        feedback_playstore=feedback_playstore,
        feedback_applestore=feedback_applestore,
        feedback_sentiment_playstore=feedback_sentiment_playstore,
        feedback_sentiment_applestore=feedback_sentiment_applestore,
        playstore_comparison=playstore_comparison,
        applestore_comparison=applestore_comparison
    )

@app.route('/analysis')
def analysis():
    try:
        data = load_and_process_data(mongo)
    except Exception as e:
        return f"An error occurred: {str(e)}"

    return render_template(
        'analysis.html',
        playstore_genre_counts=data['playstore_genre_counts'],
        applestore_genre_counts=data['applestore_genre_counts']
    )

@app.route('/about-us')
def about_us():
    return render_template('about_us.html')

@app.route('/eda')
def eda():
    try:
        # Perform EDA
        eda_results = perform_eda(mongo.cx)  # mongo.cx returns the client instance
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
    return render_template('eda.html', 
                           playstore_accuracy=eda_results['playstore_accuracy'], 
                           playstore_report=eda_results['playstore_report'], 
                           applestore_accuracy=eda_results['applestore_accuracy'], 
                           applestore_report=eda_results['applestore_report'])
    
    
@app.route("/helobot")
def helobot():
    return render_template("helobot.html")    

@app.route('/imageclassify', methods=['POST', 'GET'])
def imageclassify():
    return render_template("image_classifier.html")


@app.route('/api/playstore_top_apps', methods=['GET'])
def get_playstore_top_apps():
    try:
        data = load_and_process_data(mongo)
        return jsonify(data['playstore_top_apps'])
    except KeyError as e:
        return jsonify({'error': f'KeyError: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/applestore_top_apps', methods=['GET'])
def get_applestore_top_apps():
    try:
        data = load_and_process_data(mongo)
        return jsonify(data['applestore_top_apps'])
    except KeyError as e:
        return jsonify({'error': f'KeyError: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/playstore_genre_counts', methods=['GET'])
def get_playstore_genre_counts():
    try:
        data = load_and_process_data(mongo)
        return jsonify(data['playstore_genre_counts'])
    except KeyError as e:
        return jsonify({'error': f'KeyError: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/applestore_genre_counts', methods=['GET'])
def get_applestore_genre_counts():
    try:
        data = load_and_process_data(mongo)
        return jsonify(data['applestore_genre_counts'])
    except KeyError as e:
        return jsonify({'error': f'KeyError: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
