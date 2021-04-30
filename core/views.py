from django.shortcuts import render

def getHtmlContent(city):
    import requests
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    session = requests.Session()
    session.headers = headers
    city = city.replace(' ', '+')
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content

def home(request):
    weather_data = None
    if 'city' in request.GET:
        #fetch weather data
        city = request.GET.get('city')
        html_content = getHtmlContent(city)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        #print(soup.prettify())
        weather_data = dict()
        weather_data['region'] = soup.find('div', attrs={'id': 'wob_loc'}).text
        #print(weather_data)
        weather_data['daytime'] = soup.find('div', attrs={'id': 'wob_dts'}).text
        weather_data['status'] = soup.find('span', attrs={'id': 'wob_dc'}).text
        weather_data['temp'] = soup.find('span', attrs={'id': 'wob_tm'}).text
    return render(request, 'core/home.html', {'weather': weather_data})