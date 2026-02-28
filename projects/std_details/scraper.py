import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_student_details():
    # Setup Chrome WebDriver
    driver = webdriver.Chrome()

    try:
        # Navigate to the target website's login page
        login_url = 'https://pulse.itvedant.com/site/login'
        print(f"Opening browser to {login_url}...")
        driver.get(login_url)

        # Pause and wait for the user to manually log in
        print("="*60)
        print("ACTION REQUIRED:")
        print("1. Please log in with your company email ID in the opened browser window.")
        print("2. Once you have successfully logged in and are on the dashboard,")
        print("3. Press Enter here in the console to start scraping pages 1 to 5.")
        print("="*60)
        input("Press Enter to continue scraping...")

        print("Proceeding to scrape details...")

        all_students = []

        # Loop through pages 1 to 5
        for page in range(1, 6):
            page_url = f"http://pulse.itvedant.com/student/active-learners?page={page}&per-page=10"
            print(f"\nScraping page {page}: {page_url}")
            driver.get(page_url)

            # Wait for the table body to load
            wait = WebDriverWait(driver, 10)
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table-bordered tbody tr")))
            except:
                print(f"No data found or timeout on page {page}.")
                continue

            # Give a small pause to let all elements render properly
            time.sleep(2)

            # Find all rows in the table body
            rows = driver.find_elements(By.CSS_SELECTOR, "table.table-bordered tbody tr")
            print(f"Found {len(rows)} students on page {page}.")

            for row in rows:
                try:
                    # Extract Name (from h5 element inside fullname column)
                    try:
                        name_element = row.find_element(By.CSS_SELECTOR, "td.fullname_column h5")
                        # You can remove the "premium" span text if it appears, but .text is usually fine
                        name = name_element.text.replace("\n", " ").strip()
                    except:
                        name = "Not found"

                    # Extract Phone Number (from p element inside fullname column)
                    try:
                        phone = row.find_element(By.CSS_SELECTOR, "td.fullname_column p").text.strip()
                    except:
                        phone = "Not found"

                    # Extract Branch (acting as College / Location based on the HTML)
                    try:
                        branch = row.find_element(By.CSS_SELECTOR, "td.branch_column").text.strip()
                    except:
                        branch = "Not found"

                    # Extract Courses (acting as Degree based on the HTML)
                    try:
                        course_elements = row.find_elements(By.CSS_SELECTOR, "td.courses_column ul li")
                        courses = [c.text.strip() for c in course_elements if c.text.strip()]
                        degree = ", ".join(courses)
                    except:
                        degree = "Not found"

                    print(f"Extracted: {name} | {phone} | {branch} | {degree}")

                    all_students.append({
                        "Name": name,
                        "Phone Number": phone,
                        "Branch": branch,
                        "Courses (Degree)": degree
                    })

                except Exception as row_e:
                    print(f"Error extracting row data: {row_e}")

        # Save the scraped data to a CSV file
        csv_filename = "student_details.csv"
        if all_students:
            print(f"\nSaving {len(all_students)} records to {csv_filename}...")
            with open(csv_filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["Name", "Phone Number", "Branch", "Courses (Degree)"])
                writer.writeheader()
                writer.writerows(all_students)
            print("Data saved successfully!")
        else:
            print("\nNo data to save.")

    except Exception as e:
        print(f"An error occurred during scraping: {e}")

    finally:
        # Keep the browser open for a few seconds before closing
        time.sleep(2)
        print("Closing the browser...")
        driver.quit()

if __name__ == "__main__":
    scrape_student_details()
