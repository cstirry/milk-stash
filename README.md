# Milk Stash Calculator app

Streamlit app calculates milk stash requirements based on various inputs
including current storage, expected weaning schedule, and expected consumption.

### Prerequisites

- Docker

### Installing

1. Clone the repository
2. Build the Docker image:

`docker build -t milk_calc .`

3. Run the container:

`docker run -p 8501:8501 milk_calc`

The app should now be running on [http://localhost:8501](http://localhost:8501).