# Negative and Edge Case Tests for SauceDemo

## Setup and Installation

### Prerequisites
- Install Python (>=3.7)
- Install Google Chrome
- Install ChromeDriver (matching your Chrome version)

### Install Dependencies
1. Clone this repository:
   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Tests
To execute the test suite, run the following command:
```sh
pytest
```
For detailed reports:
```sh
pytest -v --html=report.html
```
## Viewing the Report

After running the tests with the HTML report option, open report.html in a web browser to view the detailed test results.

## Assumptions and Constraints
- The tests assume that the SauceDemo website (https://www.saucedemo.com/) is accessible and functional.
- ChromeDriver should be correctly installed and available in the system PATH.
- The tests cover negative and edge cases such as invalid logins, missing checkout details, and logout scenarios.
- Tests are written using Selenium with Pytest as the test framework.
- The UI structure of SauceDemo should not change significantly, or tests may require updates.

## Notes
- If a test fails due to an element not being found, verify that the website is not experiencing downtime.
- The browser is controlled by automated test software, so user input is not required during execution.
- All form fields are cleared before inputting values to prevent residual data issues.

