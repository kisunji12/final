import json
import requests
import os.path

url = 'https://bg.annapurnapost.com/api/search?title=%E0%A4%96%E0%A5%87%E0%A4%B2%E0%A4%95%E0%A5%81%E0%A4%A6'

# MANUALLY ENTER THE NUMBER MORE THAN NUMBER SAVED IN PAGE.TXT FILE.
# IF PAGE.TXT NOT EXIST THEN ENTER 0.

pageno = 0

#  PUT THE NUMBER AS YOUR REQUIREMENT FOR SCRAPING TO CHECK THE CONDITION
# HOW MANY PAGE YOU WANT TO SCRAPE, FOR NOW IT'S 4.


count = 1
while count <= 3:

    # CHECK WHETHER THE FILE EXIST OR NOT. IF NOT CREATE ONE.
    try:
        if not os.path.exists('page.txt' and 'jsondata.json'):
            with open('page.txt', 'w') as fp:
                fp.write(str(pageno))

            with open('jsondata.json', 'w+') as fp:
                fp.write('[]')

        # <------------------------------------------------------>

        else:
            with open('page.txt', 'r+') as fp:
                page_data = int(fp.read())

                pageno = (1+page_data)

                res = requests.get(url)

                # SEEK HELPS TO BRING THE POINTER TO FIRST.
                fp.seek(0)
                fp.write(str(pageno))

                # WRITE THE JSON FILE IN ORDER TO SAVE THE REQUIRED DATA.
                with open('jsondata.json', 'r+', encoding='utf-8') as fp:

                    datalist = json.loads(fp.read())
                    fp.seek(0)

                    for jd in res.json()['data']['items']:
                        entry_dict = {
                            'title': jd['title'],
                            'author': jd['author'],
                            'content': jd['content'],
                            'publishDate': jd['publishOn']
                        }
                        datalist.append(entry_dict)

                    json.dump(datalist, fp, ensure_ascii=False, indent=4)
                    print('Done!!!')

    except requests.ConnectionError:
        print("Connection Lost..")

    count += 1

# Read all the scraped data title outside while loop separately
for data in datalist:
    print(data['title'])
