from playwright.sync_api import sync_playwright


def has_price(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Navigate to the page and wait for it to load completely
            page.goto(url, wait_until="load", timeout=20000)
            
            # List of keywords to check for
            keywords = [
                "Courses", "Fees", "Pricing", "Cost", "Plans",
                "Packages", "Driving Programs", "Services",
                "Our Services", "Courses and Fees"
            ]
            
            for keyword in keywords:
                try:
                    # Wait for the keyword element to be present
                    page.wait_for_selector(f'text="{keyword}"', timeout=8000)
                    
                    if page.locator(f'text="{keyword}"').count() > 0:
                        # Click the first matching element
                        page.locator(f'text="{keyword}"').first.click()
                        print(f"Navigating to: {page.url}")
                        return page.url
                
                except Exception as e:
                    print(f"Keyword '{keyword}' not found or not clickable. Error: {e}")

            # If no matching elements are found, return the original URL
            print(f"Keyword not found, staying on: {url}")
            return url

        except Exception as e:
            print(f"Error processing {url}: {e}")

        finally:
            browser.close()

