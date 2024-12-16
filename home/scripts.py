import os
import uuid
import requests
from bs4 import BeautifulSoup
from home.models import News

def download_image(image_url, save_directory, image_name):
  
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    image_path = os.path.join(save_directory, image_name)
    response = requests.get(image_url, stream=True)
    
    if response.status_code == 200:
        with open(image_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return image_path
    else:
        print(f"Failed to download image. Status Code: {response.status_code}")
        return None

def scrape_imdb_news():

    url = "https://www.imdb.com/news/movie/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    news_items = soup.find_all('div', class_='ipc-list-card--border-line')
    
    for item in news_items:
        # Extract title
        title_tag = item.find('a', class_='ipc-link ipc-link--base sc-ed7ef9a2-3 eDjiRr')
        title = title_tag.text.strip() if title_tag else "No title"

        # Extract description
        description_tag = item.find('div', class_='ipc-html-content-inner-div')
        description = description_tag.text.strip() if description_tag else "No description"

        # Extract external link
        external_link = f"https://www.imdb.com{title_tag['href']}" if title_tag and title_tag.has_attr('href') else None

        # Extract image URL
        image_tag = item.find('img', class_='ipc-image')
        image_url = image_tag['src'] if image_tag and image_tag.has_attr('src') else None
        
        # Extract metadata (e.g., date and author)
        metadata_items = item.find_all('li', class_='ipc-inline-list__item')
        date = metadata_items[0].text.strip() if len(metadata_items) > 0 else "No date"
        author = metadata_items[1].text.strip() if len(metadata_items) > 1 else "No author"

        # Download the image if available
        image_path = None
        if image_url:
            image_name = f"image_{uuid.uuid4()}.jpg"
            image_path = download_image(image_url, 'downloads', image_name)
        
        # Save the data into the database if external link is unique
        if external_link and not News.objects.filter(external_link=external_link).exists():
            News.objects.create(
                title=title,
                description=description,
                image=image_path or image_url,  
                external_link=external_link
            )
            print(f"Saved news: {title}")

    print("Scraping completed and data saved to the database.")

