import requests
from bs4 import BeautifulSoup

def check_observatory_status(url):
    # Send a GET request to the observatory's website
    response = requests.get(url)
    response.raise_for_status()  # will raise an HTTPError if the HTTP request returned an unsuccessful status code

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Try to find the observatory status - Adjust the selector as needed
    status_element = soup.find_all(string=lambda text: "OBSERVATORY STATUS" in text)
    
    if status_element:
        # Assuming the status is in a parent element of the found string
        status_text = ' '.join([str(elem.parent.get_text(strip=True)) for elem in status_element])
        return status_text
    else:
        return "Observatory status not found."

# Example usage
# observatory_url = "https://observatory.astro.utah.edu/"
# status = check_observatory_status(observatory_url)
# print(status)
