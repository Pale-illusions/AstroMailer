import requests

def fetch_nasa_apod(api_key: str):
    """获取 NASA Astronomy Picture of the Day 数据"""

    response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={api_key}")
    if response.status_code == 200:
        apod_data = response.json()
        return apod_data
    else:
        raise Exception("Failed to fetch NASA APOD data")