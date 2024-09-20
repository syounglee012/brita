# brita
A Code Documentation Generator


## Development

### Setting Up the Development Environment
1. Clone the repository:
   ```bash
   git clone https://github.com/rumatveev/brita.git
   cd brita
   ```

2. Install project dependencies using Poetry:
    ```bash
    poetry install
    ```

### Run the  app locally

1. Activate the virtual environment and run the app:
    ```bash
    poetry run streamlit run app/app.py
    ```


### Run the app in a container

1. Building a container:
    ```bash
    make build
    ```
   
2. Running a container:
    ```bash
    make run
    ```
   
3. Cleaning up:
    ```bash
    make delete
    ```
