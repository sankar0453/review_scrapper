import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import traceback
import logging
import pandas as pd

# Configure the logger
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')




def find_page_count(url):
    response=requests.get(url)
    soup=BeautifulSoup(response.content,"html.parser")
    
    page_count_element = soup.select_one('#container > div > div._2tsNFb > div > div > div._1YokD2._3Mn1Gg.col-9-12 > div:nth-child(13) > div > div > span:nth-child(1)')
    page_count=0
    if page_count_element is not None:
        page_count_text = page_count_element.get_text(strip=True)
        parts = page_count_text.split()
        page_count = int(parts[-1])
    
    return page_count

def element_text(ele,class_name):
    ele_val=ele.find(class_=class_name)
    if ele_val is not None:
        return ele_val.get_text(strip=True)
    else:
        return ""
def page_data(page_num):
    try:
        url=f"https://www.flipkart.com/apple-iphone-14-pro-max-deep-purple-128-gb/product-reviews/itm5256789ae40c7?pid=MOBGHWFHCWHXRZZJ&lid=LSTMOBGHWFHCWHXRZZJ1FSXCM&marketplace=FLIPKART&page={page_num}"
        response=requests.get(url)
        soup=BeautifulSoup(response.content,"html.parser")
        page_info_elements = soup.find_all(class_='_1AtVbE col-12-12')
        del page_info_elements[0]
        del page_info_elements[-1]
    
        # Initialize lists to store data
        ratings = []
        titles = []
        reviews = []
        names = []
        for index, review_div in enumerate(page_info_elements):
            cols = review_div.find_all(class_='col _2wzgFH K0kLPL')
            for row in cols:
                rating = element_text(row,'_3LWZlK _1BLPMq')
                title = element_text(row,'_2-N8zT')  
                review = element_text(row,'t-ZTKy')  
                name = element_text(row,'_2sc7ZR _2V5EHH')  
                
                ratings.append(rating)
                titles.append(title)
                reviews.append(review)
                names.append(name)
        return True, names, ratings, titles, reviews
    except Exception as e:
        logger.error("Error occurred while scraping page %d:\n%s", page_num, traceback.format_exc())
        return False, [], [], [], []


def main():
    # Initialize lists to store data
    all_names = []
    all_ratings = []
    all_titles = []
    all_reviews = []
    
    try:
        logging.info("Flipkar reviews scrapping intiated....")
        
        product_name="apple-iphone-14-pro-max-deep-purple-128-gb"
        url=f"https://www.flipkart.com/{product_name}/product-reviews/itm5256789ae40c7?pid=MOBGHWFHCWHXRZZJ&lid=LSTMOBGHWFHCWHXRZZJ1FSXCM&marketplace=FLIPKART&page=1"
        
                
        page_count=find_page_count(url)
        logging.info(f"Number of pages for given URL {page_count}")
        if page_count !=0:
            for i in range(1, page_count + 1):
                logging.info("Scraping page %d", i)
                success, names, ratings, titles, reviews=page_data(i)
                if success:
                    all_names.extend(names)
                    all_ratings.extend(ratings)
                    all_titles.extend(titles)
                    all_reviews.extend(reviews)
        else:   
            logging.info("No reviews to scrape")
        
        # Create a DataFrame using pandas
        data = {
            'Name': all_names,
            'Rating': all_ratings,
            'Title': all_titles,
            'Review': all_reviews
        }

        df = pd.DataFrame(data)
        # Save the DataFrame to a CSV file
        df.to_csv('reviews.csv', index=False)

        print("Data saved to 'reviews.csv'")            
    except Exception as e:
        logging.error(e)
                                     
               
            

   
if __name__ == "__main__":
    main()
