import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# URL for Selenium Playground Table Search Demo
URL = "https://www.lambdatest.com/selenium-playground/table-sort-search-demo"

@pytest.fixture(scope="function")
def setup_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

def test_search_functionality(setup_driver):
    driver = setup_driver
    driver.get(URL)

    # Locate search box and enter "New York"
    search_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "(//input[@type='search'])[1]")))
    search_box.send_keys("New York")

    # Wait for the results to load
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//tbody//tr[@role='row']//td[3]")))

    # Locate the result table and rows
    result_table = driver.find_element(By.XPATH, "//table[@id='example']")
    result_rows = result_table.find_elements(By.XPATH, "//tbody//tr[@role='row']//td[3]")

    # Validate the number of search results
    assert len(result_rows) == 5, f"Expected 5 search results, but found: {len(result_rows)}"

    # Use a for loop to validate each row contains "New York"
    for row in result_rows:
        row_text = row.text
        assert "New York" in row_text, f"Expected 'New York' in row, but found: {row_text}"

    # Verify total entries count
    total_entries_text = driver.find_element(By.XPATH, "(//div[@id='example_info'])[1]").text
    assert "Showing 1 to 5 of 5 entries (filtered from 24 total entries)" in total_entries_text, "total entries count is correct"

if __name__ == "__main__":
    pytest.main(["-v", __file__])