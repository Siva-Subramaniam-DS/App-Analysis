# App
Handles both GET and POST requests. When POST is received, it extracts app_name and store from the form. Depending on the store selected, it filters the relevant dataset and retrieves app information. 
If the store is both, it retrieves data from both stores and includes additional comparison data. 
Returns the rendered index.html with the retrieved data and potential errors
