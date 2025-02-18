import requests 
from bs4 import BeautifulSoup
import re  
from urllib.parse import urljoin 

# Defining a function

def scrapy():  
    while True:  # For multiple inputs
        url = input("Please input the URL of a site (writting 'No' stops the inputs): ").strip()  # User inputs URL 
        if url.lower() == "no":  
            break  # Ending loop if user said no 

        try:  # Error handling
            response = requests.get(url, timeout=10) 
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")  # Creates a BeautifulSoup object 

            #### Phone number extraction

            phone_numbers = set()  
            phone_pattern = r"\+?\d[\d\s\-\(\)\/]{7,15}"  

            for a in soup.find_all("a", href=True):
                href = a["href"].lower() 
                if "tel:" in href or "fax:" in href or "phone:" in href:  
                    phone = a["href"].replace("tel:", "").strip() 
                    cleaned_phone = re.sub(r"[^\d\+\(\)-]", "", phone) 
                    phone_numbers.add(cleaned_phone)  

            if not phone_numbers: 
                for tag in soup.find_all(["a", "p", "span", "div"]):
                    text = tag.get_text(strip=True)  
                    match = re.search(phone_pattern, text)  
                    if match:  
                        phone = match.group(0)  
                        cleaned_phone = re.sub(r"[^\d\+\(\)-]", "", phone)  
                        phone_numbers.add(cleaned_phone)

            phone_str = ",".join(sorted(list(phone_numbers))) if phone_numbers else "None" 


            #### Logo extraction
            logo_link = None
            for img in soup.find_all("img"):  
                alt_text = img.get("alt", "").lower()  
                if "logo" in alt_text or "logo" in img.get("class", []):  
                    logo_link = urljoin(url, img.get("src")) 
                    break  

            if not logo_link: 
                header = soup.find("header") 
                if header:  
                    logo_tag = header.find("img") 
                    if logo_tag: 
                        logo_link = urljoin(url, logo_tag.get("src")) 

            logo_link_str = logo_link or None 


            ### Output
            print(f"URL: {url}")  
            print(f"Phone number(s): {phone_str}")  
            print(f"Logo: {logo_link_str}")


        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL {url}: {e}") 
            continue 

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            continue

scrapy()