# Milk Stash Calculator app

This is a repository for a Streamlit app designed to calculate estimated needs for formula and pumped milk storage,
aiding in effective planning and resource management.

You can interact with the web interface by either using the deployed Streamlit app or running the app locally.

### Run the app locally with Docker

1. Clone the repository
2. Build the Docker image:

`docker build -t milk_calc .`

3. Run the container:

`docker run -p 8501:8501 milk_calc`

The app should now be running on [http://localhost:8501](http://localhost:8501).