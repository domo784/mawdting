import os
import gzip
import xml.etree.ElementTree as ET
import requests

# Constants
NAME = "daddylive-channels"
SAVE_AS_GZ = True

# Directory and file paths
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "epgs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

TVG_IDS_FILE = os.path.join(os.path.dirname(__file__), f"{NAME}-tvg-ids.txt")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"{NAME}-epg.xml")
OUTPUT_FILE_GZ = OUTPUT_FILE + '.gz'

def fetch_and_extract_xml(url):
    """
    Fetches XML data from the given URL and extracts it.
    
    Args:
    url (str): The URL of the XML data.
    
    Returns:
    xml.etree.ElementTree.Element: The extracted XML data, or None if failed.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None

    if url.endswith('.gz'):
        try:
            decompressed_data = gzip.decompress(response.content)
            return ET.fromstring(decompressed_data)
        except Exception as e:
            print(f"Failed to decompress and parse XML from {url}: {e}")
            return None
    else:
        try:
            return ET.fromstring(response.content)
        except Exception as e:
            print(f"Failed to parse XML from {url}: {e}")
            return None

def filter_and_build_epg(urls):
    """
    Filters and builds the EPG data from the given URLs.
    
    Args:
    urls (list): A list of URLs to fetch EPG data from.
    """
    with open(TVG_IDS_FILE, 'r') as file:
        valid_tvg_ids = set(line.strip() for line in file)

    root = ET.Element('tv')

    for url in urls:
        print(f"Fetching XML ({url})...")
        epg_data = fetch_and_extract_xml(url)
        if epg_data is None:
            continue

        for channel in epg_data.findall('channel'):
            tvg_id = channel.get('id')
            if tvg_id in valid_tvg_ids:
                print(f"tvg-id -> {tvg_id}")
                root.append(channel)

        for programme in epg_data.findall('programme'):
            tvg_id = programme.get('channel')
            if tvg_id in valid_tvg_ids:
                title = programme.find('title')
                if title is not None:
                    title_text = title.text if title is not None else 'No title'

                    if title_text == 'NHL Hockey' or title_text == 'Live: NFL Football':
                        subtitle = programme.find('sub-title')
                        subtitle_text = subtitle.text if subtitle else 'No subtitle'
                        programme.find('title').text = title_text + " " + subtitle_text

                    root.append(programme)

    tree = ET.ElementTree(root)
    tree.write(OUTPUT_FILE, encoding='utf-8', xml_declaration=True)
    print(f"New EPG saved to {OUTPUT_FILE}")

    if SAVE_AS_GZ:
        with gzip.open(OUTPUT_FILE_GZ, 'wb') as f:
            tree.write(f, encoding='utf-8', xml_declaration=True)
        print(f"New EPG saved to {OUTPUT_FILE_GZ}")

if __name__ == "__main__":
    urls = [
    "http://m3u4u.com/xml/5g28nezee8sv3dk7yzpe",
    "https://epgshare01.online/epgshare01/epg_ripper_AR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_AU1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_BEIN1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_BG1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_BR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_CA1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_CL1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_CO1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_CR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_CY1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_DE1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_DK1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_ES1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_FANDUEL1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_FANDUEL1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_FR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_GR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_HR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_IL1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_IN4.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_IT1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_MX1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_MY1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_NL1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_NZ1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_PK1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_PL1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_PT1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_RO1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_RO2.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_SA1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_SE1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_TR1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_UK1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_US1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_US_LOCALS2.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_UY1.xml.gz",
    "https://epgshare01.online/epgshare01/epg_ripper_ZA1.xml.gz",
]

if __name__ == "__main__":
    filter_and_build_epg(urls)
