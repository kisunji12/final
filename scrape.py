import json
import requests
import os.path

url = 'https://bg.annapurnapost.com/api/search?title=%E0%A4%96%E0%A5%87%E0%A4%B2%E0%A4%95%E0%A5%81%E0%A4%A6&page='

# MANUALLY ENTER THE NUMBER MORE THAN NUMBER SAVED IN PAGE.TXT FILE.
# IF PAGE.TXT NOT EXIST THEN ENTER 0.

pageno = 0
scraped = []

#  PUT THE NUMBER AS YOUR REQUIREMENT FOR SCRAPING TO CHECK THE CONDITION
# HOW MANY PAGE YOU WANT TO SCRAPE, FOR NOW IT'S 4.


count = 1
while count <= 3:

    # CHECK WHETHER THE FILE EXIST OR NOT. IF NOT CREATE ONE.
    try:
        if not os.path.exists('page.txt'):
            with open('page.txt', 'w') as fp:
                fp.write(str(pageno))

        # <------------------------------------------------------>

        else:
            with open('page.txt', 'r+') as fp:
                page_data = int(fp.read())

                pageno = (1+page_data)

                res = requests.get(url+str(pageno))

                if pageno > page_data:
                    # SEEK HELPS TO BRING THE POINTER TO FIRST.
                    fp.seek(0)
                    fp.write(str(pageno))

                    # WRITE THE JSON FILE IN ORDER TO SAVE THE REQUIRED DATA.
                    with open('jsondata.json', 'a+', encoding='utf-8') as fp:
                        for jd in res.json()['data']['items']:
                            entry_dict = {
                                'title': jd['title'],
                                'author': jd['author'],
                                'content': jd['content'],
                                'publishDate': jd['publishOn']
                            }
                            scraped.append(entry_dict)
                        json.dump(scraped, fp, ensure_ascii=False, indent=4)
                        print('Done!!!')

            #    IF PAGE NO IS NOT GREATER THAN PAGE NO SAVED IN PAGE.TXT THEN THIS BLOCK OF CODE EXECUTED.
                else:
                    print("Checking Condition...")

    except requests.ConnectionError:
        print("Connection Lost..")

    count += 1
