import time
import re
import logging
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from models import db, Property
from app import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# City IDs in Yad2
CITIES = {
    "Tel Aviv": 5000,
    "Holon": 6600
}

def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    # Use standard window size to behave normally
    options.add_argument('--window-size=1920,1080')
    driver = uc.Chrome(options=options, version_main=120) 
    # version_main typically falls back to the locally installed chrome version safely
    return driver

def scrape_yad2_category(driver, city_name, city_id, category):
    """
    category: 'forsale' or 'rent'
    returns: list of dictionaries with property data
    """
    url = f"https://www.yad2.co.il/realestate/{category}?city={city_id}"
    logger.info(f"Navigating to {url}")
    
    driver.get(url)
    
    # Wait for Cloudflare/Radware challenge or React to render
    # Add a scrolling behavior to trigger lazy loading if any
    time.sleep(8)
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 1500);")
    time.sleep(2)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Fallback to broad class search for the feed items container
    items = []
    
    feed_items = soup.find_all('div', attrs={"data-test-id": "feed-item-info"})
    
    if not feed_items:
        feed_items = soup.select('div[class*="feeditem"]')
        
    if not feed_items:
        feed_items = soup.select('div.feed-item')
        
    # If still none, Yad2 might have a new list structure. Try finding anything that looks like a card
    if not feed_items:
        feed_items = soup.select('div[class*="item_card"]')

    # Extremely robust fallback: Check all divs for prices directly
    if not feed_items:
        all_divs = soup.find_all('div')
        # We will filter divs that contain a price string
        feed_items = [d for d in all_divs if "₪" in d.get_text() and len(d.get_text()) < 1000 and len(d.get_text()) > 20]
        
    logger.info(f"Found {len(feed_items)} potential items on the page.")

    for item in feed_items:
        if len(items) >= 10:
            break
            
        try:
            full_text = item.get_text(separator=' | ', strip=True)
            
            # Robust Price Extraction using Regex
            # Matches formats like "12,000 ₪" or "5000₪"
            price_match = re.search(r'([\d,]+)\s*₪', full_text)
            if not price_match:
                continue
                
            price_str = price_match.group(1).replace(',', '')
            if not price_str.isdigit():
                continue
            
            price = int(price_str)
            
            # Subtitle/Title guessing
            pieces = [p for p in full_text.split(' | ') if len(p) > 2]
            title = pieces[0] if pieces else f"Property in {city_name}"
            # Ensure title isn't ridiculously long
            if len(title) > 80:
                title = title[:77] + "..."
                
            description = " - ".join(pieces[1:5]) if len(pieces) > 1 else full_text
            
            prop_type = "Buy" if category == "forsale" else "Rent"
            
            image_url = f"https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&q=80"
            if category == 'forsale':
                image_url = "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80"
                
            # Deduplicate by checking if price and title already in items
            if any(i['price'] == price and i['title'] == title for i in items):
                continue
                
            items.append({
                "title": title[:100], 
                "description": description[:500],
                "city": city_name,
                "type": prop_type,
                "price": price,
                "image_url": image_url
            })
            
        except Exception as e:
            logger.error(f"Error parsing item: {e}")
            continue
            
    return items

def main():
    try:
        driver = setup_driver()
    except Exception as e:
        logger.error(f"Failed to setup undetected_chromedriver: {e}")
        return

    all_properties = []
    
    try:
        for city_name, city_id in CITIES.items():
            for category in ['rent', 'forsale']:
                logger.info(f"Scraping category: {category} for {city_name}...")
                items = scrape_yad2_category(driver, city_name, city_id, category)
                logger.info(f"Successfully extracted {len(items)} items.")
                all_properties.extend(items)
                time.sleep(5) # Be polite to the server
                
    finally:
        driver.quit()
        
    save_to_db(all_properties)
        
def save_to_db(properties):
    if not properties:
        logger.error("No properties were scraped, aborting DB seed.")
        return
        
    logger.info(f"Seeding database with {len(properties)} properties from Yad2...")
    with app.app_context():
        # Clear existing mock data
        db.drop_all()
        db.create_all()
        
        for data in properties:
            prop = Property(**data)
            db.session.add(prop)
            
        db.session.commit()
    logger.info("Database successfully seeded with live Yad2 data!")

if __name__ == "__main__":
    main()
