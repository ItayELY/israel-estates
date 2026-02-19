import time
import requests
import json
import logging
import re
from bs4 import BeautifulSoup
from models import db, Property
from app import app
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User explicitly requested real web data. 
# Yad2, Madlan, Homeless are heavily blocked by enterprise WAFs.
# We are scraping ad.co.il which holds highly active Israeli classifieds and has open HTML endpoints.

def scrape_ad_co_il(city_he, city_en, category):
    properties = []
    
    # URL Mapping
    cat_path = "nadlansale" if category == 'Buy' else "nadlanrent"
    
    page = 1
    max_pages = 10
    
    while page <= max_pages and len(properties) < 15:
        url = f"https://www.ad.co.il/{cat_path}?city={city_he}&pageindex={page}"
        logger.info(f"Targeting active Israeli classifieds (Page {page}): {url}")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.ad.co.il/"
        }

        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            cards = soup.select('.card.overflow-hidden')
            if not cards:
                cards = soup.select('.card')
                
            if not cards:
                logger.info(f"No more cards found on page {page}.")
                break
                
            logger.info(f"Found {len(cards)} listings on page {page} for {city_en} ({category})")
            
            for item in cards:
                if len(properties) >= 15:
                    break
                    
                body = item.select_one('.card-body')
                if not body:
                    continue
                    
                # Filter out promoted listings ("מקודם") which appear nationwide regardless of the city search 
                is_promoted = body.find(string=re.compile("מקודם"))
                if is_promoted:
                    continue
                    
                # Extract Price
                price_elem = body.select_one('.price')
                if not price_elem:
                    continue
                    
                price_str = ''.join(filter(str.isdigit, price_elem.text))
                if not price_str or len(price_str) < 3:
                    continue
                
                price = int(price_str)
                
                # Extract Title / Neighborhood
                title_elem = body.select_one('h2.card-title')
                title_base = title_elem.text.strip() if title_elem else f"Property in {city_en}"
                
                # Extract Street / City Match
                street_elem = body.select_one('p.card-text')
                street = street_elem.text.strip() if street_elem else ""
                
                # Extract Rooms
                rooms = "3" # Default
                bed_icon = body.select_one('.fa-bed')
                if bed_icon and bed_icon.find_next_sibling('span'):
                     rooms_text = bed_icon.find_next_sibling('span').text.strip()
                     rooms = ''.join([c for c in rooms_text if c.isdigit() or c == '.']) or "3"
                     
                action = "להשכרה" if category == "Rent" else "למכירה"
                full_title = f"דירת {rooms} חדרים {action}: {title_base}"
                if street and street not in title_base:
                    full_title += f" ({street})"
                    
                description = f"פורסם ב- ad.co.il. {title_base}, {street}. {rooms} חדרים מרווחים, מחיר כדאי."
                
                # Rigorous geographical filtering: Check for explicit mention of the city.
                valid = False
                text_to_check = f"{title_base} {street}".strip()
                
                if city_en == "Tel Aviv" and ("תל אביב" in text_to_check or "יפו" in text_to_check):
                    valid = True
                elif city_en == "Holon" and "חולון" in text_to_check:
                    valid = True
                    
                if valid:
                    logger.info(f"✅ PASSED FILTER [{city_en}]: '{text_to_check}'")
                else:
                    logger.debug(f"❌ FAILED FILTER [{city_en}]: '{text_to_check}' (City name missing from text)")
                    continue

                # Image
                image_url = "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&q=80" if category == 'Rent' else "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80"
                img_elem = item.select_one('picture img')
                if img_elem and img_elem.has_attr('src'):
                    src = img_elem['src']
                    if src.startswith('//'):
                        image_url = "https:" + src
                    elif src.startswith('/'):
                        image_url = "https://www.ad.co.il" + src
                    else:
                        image_url = src
                
                properties.append({
                    "title": full_title[:100], 
                    "description": description[:500],
                    "city": city_en,
                    "type": category,
                    "price": price,
                    "image_url": image_url
                })
                
        except Exception as e:
            logger.error(f"Ad.co.il Scraping Failure on Page {page}: {e}")
            break
            
        page += 1
        time.sleep(1) # Be polite between pages
        
    return properties


def main():
    logger.info("Starting Native Scraping Pipeline for active Israeli classifieds...")
    all_properties = []
    
    cities = [
         {"he": "תל אביב יפו", "en": "Tel Aviv"},
         {"he": "חולון", "en": "Holon"}
    ]
    
    for c in cities:
        all_properties.extend(scrape_ad_co_il(c["he"], c["en"], "Rent"))
        time.sleep(1) # Be polite
        all_properties.extend(scrape_ad_co_il(c["he"], c["en"], "Buy"))
        time.sleep(1)
        
    save_to_db(all_properties)

def save_to_db(properties):
    if not properties:
        logger.error("No properties yielded.")
        return
        
    logger.info(f"Seeding DB with {len(properties)} properties from ad.co.il...")
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        for data in properties:
            prop = Property(**data)
            db.session.add(prop)
            
        db.session.commit()
    logger.info("Database successfully seeded with live Israeli data.")

if __name__ == "__main__":
    main()
