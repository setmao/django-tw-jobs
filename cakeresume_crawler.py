import requests
from bs4 import BeautifulSoup

url = "https://www.cakeresume.com/jobs?q={}&page={}"

keyword = "django"

companies = {}

break_flag = False

page = 1
while True:

    if break_flag:
        break

    resp = requests.get(url.format(keyword, page))
    soup = BeautifulSoup(resp.text, "html.parser")

    job_list = soup.findAll("div", class_="job")

    for job in job_list:
        job_link_element = job.find("a", "job-link")
        company_element = job.find("h5", "page-name").find("a")

        title = job_link_element.text
        link = job_link_element["href"]

        description = job.find("p", "job-desc").text

        label_elements = job.find_all("a", class_="label")
        labels = [element.text for element in label_elements]

        if all([keyword not in i.lower() for i in [title, description] + labels]):
            break_flag = True
            break

        company_name = company_element.text
        if company_name not in companies:
            companies[company_name] = {}
            companies[company_name]["jobs"] = []
            companies[company_name]["cakeresume_link"] = company_element["href"]

        companies[company_name]["jobs"].append({
            "title": title,
            "link": link,
            "description": description,
            "labels": labels,
        })

    page += 1

mkd = "## Django TW jobs"
for company in companies:
    mkd += "\n- {}".format(company)
    mkd += "\n  - [{}]({})".format("cakeresume", companies[company]["cakeresume_link"])
    for job in companies[company]["jobs"]:
        mkd += "\n    - [{}]({})".format(job["title"], job["link"])

with open("README.md", "w+") as f:
    f.write(mkd)
