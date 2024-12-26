# App - Analysis

**Project Overview**

This Flask application is designed for exploring and analyzing app data from the Google Play Store and Apple App Store, leveraging MongoDB for data storage. It offers functionalities such as:

- **App Search:** Users can search for apps in either store or both, receiving details, user feedback (simulated, with sentiment analysis), and comparisons between stores (if applicable).
- **Analysis:** Visualize app genre distribution in both stores.
- **EDA (Exploratory Data Analysis):** (Optional) Perform more in-depth analysis on app ratings and reviews (requires `perform_eda` function implementation).
- **Helobot Conversation:** Interact with a basic chatbot using the `chain` library. (Optional, may require additional setup)
- **Image Classifier:** (Placeholder) Future integration for image classification functionality. (Placeholder HTML template provided)

**Technical Stack**

- **Flask:** Microframework for building web applications
- **Flask-PyMongo:** Connects Flask to MongoDB
- **PyMongo/MongoClient:** Python driver for interacting with MongoDB
- **Jinja2:** Templating engine for generating HTML pages dynamically

**Code Breakdown**

**1. Imports:**

```python
from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
import random
from bson import ObjectId
from sentimental import get_sentiment  # Function for sentiment analysis
from analysis import load_and_process_data  # Function for data loading and processing
from Eda import perform_eda  # Function for EDA (optional, implementation required)
from helobot import chain  # Library for chatbot (optional)
from langchain_ollama import OllamaLLM  # Library for advanced chatbot (optional)
from langchain_core.prompts import ChatPromptTemplate  # Library for chatbot prompts (optional)
```

- **Flask and related libraries:** Enable web app development and functionalities like templating, data handling, and user interaction.
- **MongoDB libraries:** Connect to and interact with a MongoDB database.
- **`random`:** Used for random feedback selection.
- **`bson`:** Handles data types specific to MongoDB (e.g., `ObjectId`).
- **External libraries (optional):**
    - `sentimental`: Analyzes sentiment of user feedback (implementation required).
    - `analysis`: Loads and processes data for analysis (implementation required).
    - `Eda`: Performs more in-depth analysis (implementation required).
    - `helobot`: Provides basic chatbot functionality.
    - `langchain_ollama` and `langchain_core.prompts`: Libraries for advanced chatbot development (optional, setup required).

**2. Flask App Initialization and Mongo Configuration:**

```python
app = Flask(__name__)

# Configure MongoDB connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/Store"  # Update with your MongoDB connection details
mongo = PyMongo(app)
```

- Creates a Flask application instance (`app`) and sets the name (`__name__`).
- Configures the Mongo connection URI in `app.config`. Replace `mongodb://localhost:27017/Store` with your actual connection details.
- Initializes a PyMongo instance (`mongo`) to connect to the database.

**3. Feedback Loading:**

```python
def load_feedback():
    with open('positive.txt', 'r') as file:
        positive_feedback = [line.strip() for line in file.readlines()]
    with open('negative.txt', 'r') as file:
        negative_feedback = [line.strip() for line in file.readlines()]
    return positive_feedback, negative_feedback

positive_feedback, negative_feedback = load_feedback()
```

- Loads simulated positive and negative user feedback from text files (`positive.txt` and `negative.txt`).
- Stores the feedback lists in `positive_feedback` and `negative_feedback` variables.

**4. Helo AI Route (Optional):**

```python
@app.route("/heloai", methods=["POST"])
def heloai():
    data = request.get_json()
    user_input = data["question"]
    context = ""  # Context can be stored and updated as per your needs
    result = chain.invoke({"context": context, "question": user_input})
    return jsonify({"answer": result})
```

- Processes POST requests to `/heloai`.
- Extracts the user's question from the JSON data.
- Provides a placeholder for context storage (optional).
- Uses the `chain` library

Certainly, here's the remaining code details:

**5. Helper Function: `convert_objectid_to_str`**

```python
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
```

- This function recursively converts `ObjectId` instances to strings within nested dictionaries and lists. This is crucial for rendering data in templates, as `ObjectId` objects are not directly serializable to JSON.

**6. Home Route (`/`)**

```python
@app.route('/')
def home():
    return render_template('home.html')
```

- Renders the `home.html` template when the root URL (`/`) is accessed.

**7. Infinite Scroll Route (`/infiniteScroll`)**

```python
@app.route('/infiniteScroll')
def infinite_scroll():
    return render_template('infiniteScroll.html')
```

- Renders the `infiniteScroll.html` template, likely for a feature that loads data dynamically as the user scrolls.

**8. App Search Route (`/AppSearch`)**

```python
@app.route('/AppSearch', methods=['GET', 'POST'])
def index():
    # ... (Code for handling app search and displaying results) ...
```

- Handles GET and POST requests to the `/AppSearch` route.
- If a POST request is received:
    - Extracts the app name and store selection from the form data.
    - Queries the MongoDB database for the app in the specified store(s).
    - Retrieves app information, generates random feedback, and performs sentiment analysis.
    - Handles cases where the app is not found in the specified store(s).
- Renders the `app.html` template with the retrieved data, error messages (if any), and feedback information.

**9. Analysis Route (`/analysis`)**

```python
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
```

- Loads and processes data using the `load_and_process_data` function.
- Renders the `analysis.html` template with the processed data for visualization (e.g., genre counts).

**10. About Us Route (`/about-us`)**

```python
@app.route('/about-us')
def about_us():
    return render_template('about_us.html')
```

- Renders the `about_us.html` template.

**11. EDA Route (`/eda`)**

```python
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
```

- Performs EDA using the `perform_eda` function (implementation required).
- Renders the `eda.html` template with the EDA results.

**12. Helobot Route (`/helobot`)**

```python
@app.route("/helobot")
def helobot():
    return render_template("helobot.html")
```

- Renders the `helobot.html` template for interacting with the chatbot.

**13. Image Classifier Route (`/imageclassify`)**

```python
@app.route('/imageclassify', methods=['POST', 'GET'])
def imageclassify():
    return render_template("image_classifier.html")
```

- Renders the `image_classifier.html` template (placeholder for future image classification functionality).

**14. API Routes:**

- Provides API endpoints to retrieve data for external use or for use in JavaScript for dynamic updates in the frontend.

**15. App Run**

```python
if __name__ == '__main__':
    app.run(debug=True)
```

- Starts the Flask development server in debug mode.
---

This function fetches and processes data from the Google Play Store and Apple App Store collections in the MongoDB database. It extracts key information such as:

- **Top 10 genres** in each store (with count limits for better visualization).
- **Top 10 apps** based on reviews (Play Store) and rating count (App Store).

**Code Breakdown:**

1. **Database Access:**
   - `db = mongo.db`: Establishes a connection to the database using the `mongo` instance provided.

2. **Google Play Store Processing:**
   - **Genre Counts:**
      - `pipeline_playstore_genres`: Defines an aggregation pipeline with the following stages:
         - **`$match`:** Filters documents where the `Category` field exists, is not `None`, and is not empty.
         - **`$group`:** Groups documents by `Category` and counts the number of occurrences.
         - **`$sort`:** Sorts the groups in descending order of count.
         - **`$limit`:** Limits the output to the top 10 genres.
      - `playstore_genre_counts`: Executes the aggregation pipeline and converts the result to a list.
      - **Count Limiting:** Limits the count of each genre to a maximum of 5000 for better visualization.
   - **Top Apps:**
      - `pipeline_playstore_apps`: Defines an aggregation pipeline to:
         - **`$sort`:** Sorts documents in descending order of `Reviews`.
         - **`$group`:** Groups documents by `App` and selects the first occurrence of each field (App, Reviews, Category, Rating, Installs) for each group.
         - **`$sort`:** Sorts the groups again by `Reviews` in descending order.
         - **`$limit`:** Limits the output to the top 10 apps.
      - `playstore_top_apps`: Executes the aggregation pipeline and converts the result to a list.

3. **Apple App Store Processing:**
   - **Genre Counts:**
      - `pipeline_applestore_genres`: Defines an aggregation pipeline similar to the Play Store, but uses `prime_genre` as the grouping field.
      - `applestore_genre_counts`: Executes the pipeline and limits the count of each genre to 5000.
   - **Top Apps:**
      - `applestore_top_apps`: Directly queries the `applestore_collection`, sorts by `rating_count_tot` in descending order, and limits the output to the top 10 apps.
      - Extracts `track_name` and `rating_count_tot` for each app.

4. **Return Results:**

   - Returns a dictionary containing the extracted data:
      - `playstore_top_apps`: List of top 10 apps from the Play Store.
      - `applestore_top_apps`: List of top 10 apps from the App Store.
      - `playstore_genre_counts`: List of top 10 genres and their counts in the Play Store.
      - `applestore_genre_counts`: List of top 10 genres and their counts in the App Store.

This function provides the core data for the analysis and visualization features of the web application.

---

**Functionality:**

1. **Database Connection:**
   - Connects to the MongoDB database using the provided `mongo_client` object.
   - Accesses the `googleplaystore` and `applestore` collections.

2. **Data Fetching:**
   - Extracts data from both collections and creates Pandas DataFrames.

3. **Data Cleaning (Google Play Store):**
   - Defines functions to convert:
      - `Size` from string to numeric value (MB or KB).
      - `Installs` from string format (e.g., "10,000,000+") to integer.
      - `Rating` from string to float.
   - Applies these functions to the corresponding columns in the DataFrame.
   - Drops rows with missing values in critical fields (`Size`, `Installs`, `Rating`).
   - Raises an error if the DataFrame is empty after cleaning.

4. **Data Cleaning (Apple App Store):**
   - Defines functions to convert:
      - `user_rating` from string to float.
      - `price` from string to float.
   - Applies these functions to the corresponding columns.

5. **Data Preprocessing (Both Stores):**
   - Removes duplicates based on `App` and `track_name` columns for Google Play Store and Apple App Store, respectively.
   - Selects the top 10 apps by `Installs` (Google Play) and `rating_count_tot` (Apple) for comparison.
   - Renames columns for consistency: `App`, `Category`, `Rating`.

6. **Machine Learning Modeling (Optional):**
   - **Google Play Store:**
      - Defines `X_googleplay` (features) and `y_googleplay` (target variable - assuming 'Category').
      - Encodes the target variable using `pd.factorize`.
      - Checks for sufficient samples to perform train-test split.
      - Splits the data using `train_test_split`.
      - Trains a Random Forest Classifier model.
      - Calculates and stores the accuracy score on the test set.
   - **Apple App Store:**
      - Similar steps as Google Play, with `X_apple` and `y_apple` (target variable - assuming 'prime_genre').

7. **Results Preparation:**
   - Creates a dictionary `results` containing:
      - Model accuracy (rounded) for both stores.
      - HTML tables showing the top 10 apps with category and rating information for each store, generated using `to_html` with appropriate formatting.

8. **Return Results:**
   - Returns the `results` dictionary containing the prepared data for the HTML template.

**Example Usage:**

- The provided code snippet demonstrates how to use `perform_eda` outside the Flask application:
   - Creates a MongoDB client.
   - Calls `perform_eda` with the client.
   - Prints the returned results dictionary.

---

**1. Imports:**

- `from langchain_ollama import OllamaLLM`: Imports the `OllamaLLM` class from the `langchain_ollama` library, which allows you to interact with the Ollama language model.
- `from langchain_core.prompts import ChatPromptTemplate`: Imports the `ChatPromptTemplate` class from the `langchain_core.prompts` library, used to define and structure prompts for conversational AI.

**2. Prompt Template Definition:**

```python
template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""
```

- Defines a template for the prompts that will be sent to the Ollama model. 
- The template includes placeholders for:
    - `{context}`: Stores the previous conversation history.
    - `{question}`: The user's input.
- This structure helps the model understand the context and generate relevant responses.

**3. Model and Chain Initialization:**

```python
model = OllamaLLM(model="llava")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
```

- `model = OllamaLLM(model="llava")`: Creates an instance of the `OllamaLLM` class, specifying the desired model ("llava" in this case).
- `prompt = ChatPromptTemplate.from_template(template)`: Creates a `ChatPromptTemplate` object using the defined template.
- `chain = prompt | model`: Creates a `LLMChain` by combining the `prompt` and the `model`. This chain will be used to generate responses by first formatting the input using the prompt template and then passing it to the model.

**4. Conversation Handling Function:**

```python
def handle_conversation():
    context = ""
    print("Welcome to the HeloAI ChatBot. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        
        result = chain.invoke({"context": context, "question": user_input})
        print("HeloAI: ", result)
        context += f"User: {user_input}\nAI: {result}\n"
```

- Initializes an empty string `context` to store the conversation history.
- Prints a welcome message and instructions.
- Enters a loop:
    - Prompts the user for input.
    - Checks if the user entered "exit" to quit the conversation.
    - Uses the `chain` to generate a response by invoking it with the current `context` and the `user_input`.
    - Prints the generated response from the model.
    - Updates the `context` by appending the user's input and the model's response.

**5. Main Execution Block:**

```python
if __name__ == "__main__":
    handle_conversation()
```

- Calls the `handle_conversation()` function to start the interactive chatbot session.

**Key Features:**

- **Conversational Context:** The code maintains and utilizes conversation history to generate more relevant and coherent responses.
- **Ollama Integration:** Leverages the Ollama language model for powerful and informative responses.
- **User-Friendly Interface:** Provides a simple command-line interface for user interaction.
- **Exit Functionality:** Allows users to gracefully exit the conversation.

This code demonstrates a basic implementation of a chatbot using the Ollama language model and the `langchain` library. You can further enhance it by:

- Adding more sophisticated conversation management features.
- Implementing more advanced prompt engineering techniques.
- Integrating with other components like memory or retrieval mechanisms.
- Deploying the chatbot as a web application or a conversational agent.

---

**1. Import necessary libraries:**

- `from textblob import TextBlob`: Imports the `TextBlob` class from the `textblob` library, which provides tools for natural language processing, including sentiment analysis.
- `import random`: Imports the `random` module for sampling feedback from the lists.

**2. `get_sentiment()` function:**

- This function takes a list of feedback comments as input.
- Initializes a dictionary `sentiment_counts` to store the counts of positive, neutral, and negative sentiments.
- Iterates through each feedback comment:
    - Creates a `TextBlob` object from the comment.
    - Determines the sentiment polarity of the comment:
        - If polarity > 0, it's considered 'Positive'.
        - If polarity == 0, it's considered 'Neutral'.
        - If polarity < 0, it's considered 'Negative'.
    - Increments the corresponding count in the `sentiment_counts` dictionary.
- Calculates the percentage of each sentiment by dividing the count by the total number of feedback comments.
- Returns a dictionary containing the calculated sentiment percentages.

**3. `sample_feedback()` function:**

- This function loads positive and negative feedback comments from the specified files (`positive.txt` and `negative.txt`).
- Samples 5 comments randomly from each list (or fewer if the list has less than 5 comments).
- Combines the sampled positive and negative comments into a single list.
- Calls the `get_sentiment()` function to analyze the sentiment of the combined sample.
- Returns the sentiment percentages calculated by `get_sentiment()`.

**Key Features:**

- **Sentiment Analysis:** Utilizes the `TextBlob` library to perform sentiment analysis on text data.
- **Random Sampling:** Ensures a diverse and unbiased sample of feedback for analysis.
- **Percentage Calculation:** Provides a clear and concise representation of sentiment distribution.
- **Flexibility:** The `sample_feedback()` function can be easily modified to sample different numbers of comments or use different sampling strategies.

**Example Usage:**

```python
# Example usage
sentiment_percentages = sample_feedback()
print(sentiment_percentages) 
```

This code would:

1. Load positive and negative feedback from files.
2. Sample 5 comments from each.
3. Analyze the sentiment of the combined sample.
4. Print the resulting sentiment percentages (e.g., {'Positive': 40.0, 'Neutral': 20.0, 'Negative': 40.0}).

---

## Image Classification Flask App with Sentiment Analysis

This Flask application provides a web interface for image classification and keeps track of overall sentiment through uploaded images.

**Components:**

1. **Libraries:**
   - Flask: Web framework for building the application.
   - TensorFlow: Deep learning library for image classification.
   - Keras: High-level API for building and training neural networks (used with TensorFlow).
   - Other libraries for image manipulation and session management.

2. **Constants:**
   - `UPLOAD_FOLDER`: Defines the directory where uploaded images are saved.
   - `IMG_SIZE`: Specifies the target size for image resizing.
   - `CLASS_NAMES`: List containing the possible image classifications (e.g., 'Good', 'Bad', 'Neutral').
   - `MODEL_PATH`: Path to the pre-trained image classification model (update with your model's location).
   - `app.secret_key`: Secret key required for session management (replace with your own key).

3. **Model Loading:**
   - Attempts to load the image classification model specified in `MODEL_PATH`.
   - Prints a success message if loaded or an error message if loading fails.

4. **Session Initialization:**
   - The `@app.before_request` decorator ensures this code runs before each request.
   - Initializes a session variable `predictions` to store the classification counts for each class.

5. **Routes:**

   - `/imageclassify (GET)`:
     - Renders the `image_Classifier.html` template, likely containing an image upload form.

   - `/upload (POST)`:
     - Handles image upload requests.
     - Checks for the presence of an uploaded file.
     - Saves the uploaded image to the `uploads` directory.
     - Preprocesses the image (resizing, converting to an array).
     - Makes a prediction using the loaded model.
     - Retrieves the predicted class and confidence score.
     - Updates the session's `predictions` dictionary with the predicted class.
     - Removes the uploaded image after processing.
     - Returns a JSON response containing the predicted class and confidence score, or an error message if processing fails.

   - `/summary (GET)`:
     - Calculates summary metrics based on the stored predictions:
       - Total number of uploaded images.
       - Distribution of image classifications (counts for each class).
       - Percentage distribution of classifications.
     - Returns a JSON response containing these summary metrics, or an error message if no images were uploaded.

6. **Main Execution:**
   - Runs the Flask application in debug mode, allowing for automatic code reloading during development.

This explanation can be further enhanced by:

- Briefly mentioning the specific image classification task.
- Describing how the pre-trained model was generated or obtained.

---

## Infinite Scrolling Image Gallery with Enlarge Functionality

This JavaScript code creates an image gallery that loads images progressively as the user scrolls down the page (infinite scrolling). It also allows users to enlarge individual images.

**Functionality:**

1. **HTML Structure (Assumed):**
   - The code assumes an HTML element with the ID `Container` that will hold the image gallery.
   - It also expects a button element with the ID `x` to control image enlargement.

2. **`getImages` Function:**
   - Takes an integer `n` as input, representing the number of images to load.
   - Loops `n` times:
     - Fetches an image from the free image service "Picsum" using the `fetch` API.
     - Extracts the image URL from the response.
     - Creates a new image element (`img`) and sets its source to the URL.
     - Appends the image element to the `Container` element.
     - Adds a click event listener to the image:
       - When clicked, the image gets a CSS class `enlarged`, which likely styles it to appear larger.
       - The button element (`x`) is displayed inline.

3. **Initial Image Load:**
   - Calls the `getImages` function with `n=9` to load and display  9 images initially.

4. **Enlarge/Minimize Button:**
   - Adds a click event listener to the button (`x`):
     - Retrieves all image elements using `getElementsByTagName("img")`.
     - Loops through all images:
       - Removes the `enlarged` class, presumably shrinking the image back to its original size.
       - Adds a new class `imgs` (likely for basic image styling).
     - Hides the button itself.

5. **Infinite Scrolling:**
   - Attaches a scroll event listener to the window object.
   - Inside the listener:
     - Extracts various scroll position information using destructuring assignment.
       - `clientHeight`: Height of the viewport (visible area of the browser window).
       - `scrollTop`: Current vertical scroll position of the page.
       - `scrollHeight`: Total height of the page content.
     - Logs these values to the console (for debugging purposes, you can remove this in production).
     - Checks if the user has scrolled near the bottom of the page:
       - If the sum of `clientHeight`, `scrollTop`, and 1 (for a small buffer) is greater than or equal to `scrollHeight`, it means the user is near the bottom.
     - If the user is near the bottom, calls `getImages(3)` to load 3 more images.


