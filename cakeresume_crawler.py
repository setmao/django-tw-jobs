import requests
from bs4 import BeautifulSoup

base_url = 'https://www.cake.me'
url = base_url + "/jobs/{}?page={}"

keyword = "django"

companies = {}

page = 1
while True:

    resp = requests.get(url.format(keyword, page))
    soup = BeautifulSoup(resp.text, "html.parser")

    job_list = soup.select('div[class^="JobSearchItem_container"]')

    if not job_list:
        break

    for job in job_list:
        job_link_element = job.select_one('a[class^="JobSearchItem_jobTitle"]')
        company_element = job.select_one('a[class^="JobSearchItem_companyName"]')

        title = job_link_element.text
        link = base_url + job_link_element["href"]

        description = job.select_one('div[class^="JobSearchItem_description"]').text

        company_name = company_element.text
        if company_name not in companies:
            companies[company_name] = {}
            companies[company_name]["jobs"] = []
            companies[company_name]["cakeresume_link"] = base_url + company_element["href"]

        job = {
            "title": title,
            "link": link,
            "description": description,
            "labels": labels,
        }
        print(job)
        companies[company_name]["jobs"].append(job)

    page += 1

mkd = "## Django TW jobs"
for company in companies:
    mkd += "\n- {}".format(company)
    mkd += "\n  - [{}]({})".format("cakeresume", companies[company]["cakeresume_link"])
    for job in companies[company]["jobs"]:
        mkd += "\n    - [{}]({})".format(job["title"], job["link"])

with open("README.md", "w+") as f:
    f.write(mkd)
