from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import json
from tqdm import tqdm
from selenium.common.exceptions import TimeoutException

# Load the JSON file
with open("test_data.json", "r") as file:
    data = json.load(file)

# Extract "corrected_question" values into a list
queries = [item["corrected_question"] for item in data]

# Display the first query (for debugging or verification purposes)
print(queries[0])

# Chrome options setup
options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')  # Run in headless mode (no browser UI)

# Initialize Chrome driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# List to store results
results = []

try:
    # Navigate to the target website
    driver.get("https://tebaqa.demos.dice-research.org/")
    wait = WebDriverWait(driver, 10)

    for query in tqdm(queries, desc="Processing", unit="item"):
        # Input the query into the search bar and execute the search
        search_bar = wait.until(EC.visibility_of_element_located((By.ID, "search-bar")))
        search_bar.clear()
        search_bar.send_keys(query)
        search_bar.send_keys("\n")  # Press Enter to execute search

        time.sleep(60)  # Wait for results to load (adjust if necessary)

        # Wait for the overlay to disappear
        try:
            wait.until(lambda driver: driver.find_element(By.ID, "overlay").value_of_css_property("display") == "none")
        except TimeoutException:
            print("Overlay is still visible after waiting.")

        # Click the specified button (adjust XPath if needed)
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/div[1]/h3/div[1]/div/button")))
        button.click()

        # Retrieve the result text
        try:
            result_text = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div[1]/h3/div[2]/div"))).text
            results.append({"Query": query, "Result": result_text})
            print(result_text)
        except:
            results.append({"Query": query, "Result": "No result"})
            print(f"No result for query: {query}")

finally:
    # Close the browser
    driver.quit()

# Save the results to a CSV file
df = pd.DataFrame(results)
df.to_csv(f"query_results.csv", index=False)
print(f"Search results have been saved to 'query_results.csv'.")
