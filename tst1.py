import requests

def test_set_background():
    # Define the URL to change the background color
    url = "http://localhost:5000/set_background/47ab37"  # This sets the background to orange

    # Send a request to the Flask app
    response = requests.get(url)

# Run the test
test_set_background()
"""
:root {
  --red: #33a540;
  /*--red: #ff0000;*/
  --green: #47ab37;
  --white: #ffffff;
  --cellsize: 40px;
  --black: #030300;
  --abstand: 10px;
}"""