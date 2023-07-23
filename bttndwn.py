#!python3

import requests
import clipboard
import json
from urllib.parse import urlparse


BUTTONDOWN_API_KEY = "XXXX"


def clean_url_parameters(url):
    # Parse the given URL
    parsed_url = urlparse(url)

    # Remove the URL parameters
    clean_url = parsed_url._replace(query=None).geturl()

    return clean_url
    
    
def expand_hlines(lines):
    rlines = []
    for l in lines.split('\n'):
        if len(l) == 1 and l == '-':
            l = '---'
        rlines.append(l)
        
    return '\n'.join(rlines)
    
    
def embed_magic(lines):
    rlines = []
    for l in lines.split('\n'):
        if l.startswith("https://") or l.startswith("http://"):
            l = "\n\n" + l + "\n\n"
        rlines.append(l)
            
    return "\n".join(rlines)


# written by ChatGPT
# Function to clean Twitter URLs in text
def clean_twitter_urls(text):
    # Split the text into lines
    lines = text.split("\n")

    print(f"Processing {len(lines)} lines...")
    # Iterate over each line
    n = 0
    for i in range(len(lines)):
        # Check if the line is a Twitter URL
        if "twitter.com" in lines[i]:
            # Clean the URL parameters
            lines[i] = clean_url_parameters(lines[i])
            n += 1

    print(f"Cleaned {n} twitter urls.")
    # Return the cleaned text
    return "\n".join(lines)


#
def create_draft(subject, body):
    headers = {
        "Authorization": f"Token {BUTTONDOWN_API_KEY}"
    }
    base_url = "https://api.buttondown.email"
    endpoint = "/v1/emails"
    data = {
        "subject": f"{subject}",
        "body": f"{body}",
        "status": "draft"
    }
    
    rv = requests.post(
        base_url + endpoint,
        headers=headers,
        data=json.dumps(data))
    
    # TODO: error check the rv and return the URL for the draft email
    return rv.json()


def get_title(draft):
    title = draft[:draft.find('\n')]
    
    i = 0
    while title[i] in '# ':
        i += 1
    title = title[i:]
    
    return title
    
    
def process_draft(draft):
    title = get_title(draft)
    body = draft
    
    print("Creating draft: ...")
    print(f"  Title: {title}")
    print(f"  Body: {body[:50]}...")
    
    return create_draft(title, body)


def extract_draft_url(reply):
    try:
        return f"https://buttondown.email/emails/{reply['id']}"
    except Exception as e:
        print(f"Failed to get draft URL: {e}")
        return reply

text = clipboard.get()
text = clean_twitter_urls(text)
text = expand_hlines(text)
text = embed_magic(text)

reply = process_draft(text)
print(f"\nReply: {reply}")

draft_url = extract_draft_url(reply)
print(f"\n   {draft_url}")

clipboard.set(draft_url)

# clipboard.set(str(reply))
