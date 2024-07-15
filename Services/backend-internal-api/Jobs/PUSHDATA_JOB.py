import requests
import argparse

def job(url, term):

    # Download file
    response = requests.get(url)

    # Make POST request with file as request body
    #url = 'http://django:29990/upload'
    url = 'http://localhost:29990/api/push/'
    files = {'file': response.content}
    term = {'term': term}
    response = requests.post(url, files=files, data=term)
    print(response.content)
    if response.status_code == 200:
        return 'File uploaded successfully'
    else:
        return 'Error uploading file'

#if __name__ == '__main__':

    # Add an arguemnt for the url
    #parser = argparse.ArgumentParser(description='Download a file from a URL and make a POST request with the downloaded file')
    #parser.add_argument('url', type=str, help='The URL to download the file from')
    #parser.add_argument('term', type=str, help='The term to actually use')
    #args = parser.parse_args()

    # Start this job
    #job(args.url, args.term)

job('https://www.ufv.ca/arfiles/includes/202305-timetable-with-changes.htm', 'summer')


