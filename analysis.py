def load_and_process_data(mongo):
    db = mongo.db

    # Google Play Store
    playstore_collection = db.googleplaystore

    # Get the top 10 genre counts, filtering out documents where 'Category' is None, empty, or missing
    pipeline_playstore_genres = [
        {"$match": {"Category": {"$exists": True, "$ne": None, "$ne": ""}}},
        {"$group": {"_id": "$Category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    playstore_genre_counts = list(playstore_collection.aggregate(pipeline_playstore_genres))
    playstore_genre_counts = [{'genre': item['_id'], 'count': min(item['count'], 5000)} for item in playstore_genre_counts]

    # Get the top 10 apps by reviews in Google Play Store
    pipeline_playstore_apps = [
        {"$sort": {"Reviews": -1}},
        {"$group": {
            "_id": "$App",
            "App": {"$first": "$App"},
            "Reviews": {"$first": "$Reviews"},
            "Category": {"$first": "$Category"},
            "Rating": {"$first": "$Rating"},
            "Installs": {"$first": "$Installs"},
        }},
        {"$sort": {"Reviews": -1}},
        {"$limit": 10}
    ]
    playstore_top_apps = list(playstore_collection.aggregate(pipeline_playstore_apps))

    # Apple App Store
    applestore_collection = db.applestore

    # Get the top 10 genre counts, filtering out documents where 'prime_genre' is None, empty, or missing
    pipeline_applestore_genres = [
        {"$match": {"prime_genre": {"$exists": True, "$ne": None, "$ne": ""}}},
        {"$group": {"_id": "$prime_genre", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    applestore_genre_counts = list(applestore_collection.aggregate(pipeline_applestore_genres))
    applestore_genre_counts = [{'prime_genre': item['_id'], 'count': min(item['count'], 5000)} for item in applestore_genre_counts]

    # Get the top 10 apps by rating count in Apple App Store
    applestore_top_apps = list(applestore_collection.find().sort("rating_count_tot", -1).limit(10))
    applestore_top_apps = [{'track_name': item['track_name'], 'rating_count_tot': item['rating_count_tot']} for item in applestore_top_apps]

    return {
        'playstore_top_apps': playstore_top_apps,
        'applestore_top_apps': applestore_top_apps,
        'playstore_genre_counts': playstore_genre_counts,
        'applestore_genre_counts': applestore_genre_counts,
    }
