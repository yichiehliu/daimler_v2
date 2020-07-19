# Fleet-MMA
The availability-check match-making algorithm of Fleet.io

## Installation
To deploy the MMA server on your system, please refer to the following instructions:

1. Clone this project and `cd` to it
2. Install [Python](https://www.python.org) > 3.5
3. Create a virtual environment:
    - Mac / Ubuntu:
      ```
      python3 -m venv venv
      ```
    - Windows:
      ```
      py -3 -m venv venv
      ```
4. Activate the virtual environment
    - Mac / Ubuntu:
      ```
      . venv/bin/activate
      ```
    - Windows:
      ```
      venv\Scripts\activate
      ```
5. Install dependencies
    ```
    pip install -r requirements.txt
    ```

## How to Run
1. Initialize database
    ```
    flask initdb
    ```
    This will generate a SQLite database named `data.sqlite` (The database name can be configured in `config.py`)
2. Generate fake data
    ```
    flask forge
    ```
    To edit data, install SQLite3 and open the database using it
3. Run the MMA server
    ```
    flask run -h <ip> -p <port>
    ```
4. Send request to the server according to API described in `api_ref.md`