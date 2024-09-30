import os
import requests
import json
import pandas as pd
from tqdm import tqdm
import time
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def sanitize_title(title):
    # Replace or remove special characters
    return re.sub(r'[<>:"/\\|?*]', '_', title)


def generate_wiki_content(project_name, summary, website):
    # Generate wiki content based on the project summary
    content = f"""= {project_name} =

{summary}

== External Links ==
* [{website} {project_name} Website]
"""
    return content


def archive_website(url):
    # Archive the website using the Wayback Machine
    archive_url = f"https://web.archive.org/save/{url}"
    try:
        response = requests.get(archive_url)
        if response.status_code == 200:
            return archive_url
    except Exception as e:
        print(f"Error archiving {url}: {str(e)}")
    return None


def create_wiki_page(title, content):
    # Use the custom user agent in your requests
    headers = {
        'User-Agent': 'IERetrv/1.0 (impactevaluationfoundation@gmail.com)'
    }
    
   
    url = "https://impact.miraheze.org/w/api.php"

    # First, we need to get a csrf token
    params = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }

    try:
        responseLgTtokn = requests.get(url, headers=headers, params=params)
        responseLgTtokn.raise_for_status()
        login_token  = responseLgTtokn.json()['query']['tokens']['logintoken']

        login_params = {
            "action": "login",
            "lgname": os.getenv("MIRAHEZE_BOT_USERNAME"),
            "lgpassword": os.getenv("MIRAHEZE_BOT_PASSWORD"),
            "format": "json",
            "lgtoken": login_token 
        }

        login_response = requests.post(url, headers=headers, data=login_params)
        login_response.raise_for_status()
        cookies = login_response.cookies

        csrf_token_params = {
        "action": "query",
        "meta": "tokens",
        "format": "json"
        }
        csrf_token_response = requests.get(url, params=csrf_token_params, headers=headers, cookies=cookies)
        csrf_token = csrf_token_response.json()['query']['tokens']['csrftoken']


        # Creating a page
        data = {
            "action": "edit",
            "title": title,
            "text": content,
            "summary": "Creating an IEF Article automatically",
            "createonly": "1",
            "format": "json",
            "token": csrf_token
        }

        response = requests.post(url, data=data, headers=headers, cookies=cookies)
        response.raise_for_status()

        result = response.json()
        if 'error' in result:
            print(f"Error creating wiki page for {title}: {result['error']['info']}")
        elif 'edit' in result and result['edit']['result'] == 'Success':
            print(f"Successfully created page: {title}")
        else:
            print(f"Unexpected response for {title}: {result}")

    except requests.exceptions.RequestException as e:
        print(f"Error creating wiki page for {title}: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")


def main():
    # Read the CSV file
    df = pd.read_csv("resources/mixed_data.csv")

    # Create a directory to store wiki pages locally
    os.makedirs("wiki_pages", exist_ok=True)

    for _, row in tqdm(
        df.iterrows(), total=len(df), desc="Processing projects", leave=False
    ):
        project_name = row["Name"]
        website = row["Website"]
        summary_file = f"summaries/{sanitize_title(project_name)}.txt"

        if os.path.exists(summary_file):
            with open(summary_file, "r", encoding="utf-8") as f:
                summary = f.read()

            # Archive the website
            # archived_url = archive_website(website)

            # Generate wiki content
            wiki_content = generate_wiki_content(sanitize_title(project_name), summary, website)

            # Create the wiki page
            create_wiki_page(project_name, wiki_content)

            # small delay
            time.sleep(1)


if __name__ == "__main__":
    main()
