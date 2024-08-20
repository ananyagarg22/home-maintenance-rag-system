# Getting Started with Home Improvement Assistant

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `python doc_loader.py`

This command will run the `doc_loader.py` script to prepare a vector database using ChromaDB and the vector embeddings using the pdf files in the `documents` folder. These database data will be stored in the `chromadb` folder.

### `python app.py`

This command will run the Flask server at [http://localhost:5000](http://localhost:5000) to be ready to search the prepared ChromaDB vector database using the query obtained from the React frontend and prepare a context according to the top 3 similar vector embedding in the database. Both this context and query will be then sent to the OpenAI GPT-4o-mini API to fetch the response in a human like language.

### `npm start`

Runs the React app in the development mode.

Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes. You may also see any lint errors in the console.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.