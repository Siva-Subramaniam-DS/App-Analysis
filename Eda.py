import pandas as pd
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

def perform_eda(mongo_client):
    # Connect to the MongoDB database and collections
    db = mongo_client['Store']
    googleplaystore_collection = db['googleplaystore']
    applestore_collection = db['applestore']

    # Fetch data from MongoDB
    googleplaystore_df = pd.DataFrame(list(googleplaystore_collection.find()))
    applestore_df = pd.DataFrame(list(applestore_collection.find()))

    if googleplaystore_df.empty:
        raise ValueError("The Google Play Store DataFrame is empty after fetching data from MongoDB. Please check the data source.")

    # Data cleaning and conversion for Google Play Store
    def convert_size(size_str):
        if isinstance(size_str, str):
            try:
                if 'M' in size_str:
                    return float(size_str.replace('M', '').strip()) * 1024 * 1024
                elif 'k' in size_str:
                    return float(size_str.replace('k', '').strip()) * 1024
                return float(size_str)
            except ValueError:
                return None
        return None

    def convert_installs(installs_str):
        if isinstance(installs_str, str):
            try:
                return int(installs_str.replace(',', '').replace('+', ''))
            except ValueError:
                return None
        return None

    def convert_rating(rating_str):
        try:
            return float(rating_str)
        except (ValueError, TypeError):
            return None

    googleplaystore_df['Size'] = googleplaystore_df['Size'].apply(convert_size)
    googleplaystore_df['Installs'] = googleplaystore_df['Installs'].apply(convert_installs)
    googleplaystore_df['Rating'] = googleplaystore_df['Rating'].apply(convert_rating)

    # Drop rows with missing values for critical fields
    googleplaystore_df.dropna(subset=['Size', 'Installs', 'Rating'], inplace=True)

    if googleplaystore_df.empty:
        raise ValueError("The Google Play Store DataFrame is empty after cleaning. Check your data processing steps.")

    # Data cleaning and conversion for Apple App Store
    def convert_apple_rating(rating):
        try:
            return float(rating)
        except ValueError:
            return None

    def convert_apple_price(price):
        try:
            return float(price)
        except ValueError:
            return None

    applestore_df['user_rating'] = applestore_df['user_rating'].apply(convert_apple_rating)
    applestore_df['price'] = applestore_df['price'].apply(convert_apple_price)

    # Remove duplicates based on 'App' column for Google Play Store
    googleplaystore_df.drop_duplicates(subset='App', inplace=True)
    # Select the top 10 apps by number of installs
    top_googleplaystore_apps = googleplaystore_df.sort_values(by='Installs', ascending=False).head(10)[['App', 'Category', 'Rating']]

    # Remove duplicates based on 'track_name' column for Apple App Store
    applestore_df.drop_duplicates(subset='track_name', inplace=True)
    # Select the top 10 apps by rating count
    top_applestore_apps = applestore_df.sort_values(by='rating_count_tot', ascending=False).head(10)[['track_name', 'prime_genre', 'user_rating']]

    # Rename columns to match the desired format
    top_googleplaystore_apps.rename(columns={'App': 'App', 'Category': 'Category', 'Rating': 'Rating'}, inplace=True)
    top_applestore_apps.rename(columns={'track_name': 'App', 'prime_genre': 'Category', 'user_rating': 'Rating'}, inplace=True)

    # Model Training (Google Play Store)
    X_googleplay = googleplaystore_df[['Size', 'Installs', 'Rating']]
    y_googleplay = googleplaystore_df['Category']  # Assuming 'Category' is the target variable

    # Encode the target variable
    y_googleplay_encoded = pd.factorize(y_googleplay)[0]

    # Check if there are enough samples to perform a train-test split
    if len(X_googleplay) <= 1:
        raise ValueError("Not enough samples to perform train-test split. Increase your dataset size or adjust test_size.")

    # Perform train-test split
    X_train_googleplay, X_test_googleplay, y_train_googleplay, y_test_googleplay = train_test_split(X_googleplay, y_googleplay_encoded, test_size=0.2, random_state=42)

    # Train the model
    model_googleplay = RandomForestClassifier()
    model_googleplay.fit(X_train_googleplay, y_train_googleplay)
    y_pred_googleplay = model_googleplay.predict(X_test_googleplay)
    accuracy_googleplay = accuracy_score(y_test_googleplay, y_pred_googleplay)

    # Model Training (Apple App Store)
    X_apple = applestore_df[['user_rating', 'price']]
    y_apple = applestore_df['prime_genre']

    # Encode the target variable
    y_apple_encoded = pd.factorize(y_apple)[0]

    # Check if there are enough samples to perform a train-test split
    if len(X_apple) <= 1:
        raise ValueError("Not enough samples to perform train-test split. Increase your dataset size or adjust test_size.")

    # Perform train-test split
    X_train_apple, X_test_apple, y_train_apple, y_test_apple = train_test_split(X_apple, y_apple_encoded, test_size=0.2, random_state=42)

    # Train the model
    model_apple = RandomForestClassifier()
    model_apple.fit(X_train_apple, y_train_apple)
    y_pred_apple = model_apple.predict(X_test_apple)
    accuracy_apple = accuracy_score(y_test_apple, y_pred_apple)

    # Prepare results to be passed to the HTML template
    results = {
        'playstore_accuracy': round(accuracy_googleplay, 2),
        'playstore_report': top_googleplaystore_apps.to_html(classes='table table-striped', index=False),
        'applestore_accuracy': round(accuracy_apple, 2),
        'applestore_report': top_applestore_apps.to_html(classes='table table-striped', index=False)
    }

    return results

# Example usage
if __name__ == "__main__":
    # Create a MongoDB client
    client = MongoClient('mongodb://localhost:27017/')
    eda_results = perform_eda(client)
    print(eda_results)
