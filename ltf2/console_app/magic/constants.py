HTTP_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD',
                'OPTIONS', 'CONNECT', 'TRACE', 'PATCH']


PAGE_TIMEOUT = 15 * 1000


ACCESS_CONTROL_TYPE = {
    'ASN': 'asn',
    'Cookie': 'cookie',
    'Country': 'country',
    'Country Subdivision (ISO3166-2)': 'sdIso',
    'IP': 'ip',
    'Referrer': 'referer',
    'URL': 'url',
    'User-Agent': 'userAgent'
}


ORIGINS_OVERTIME = "**/api/bff/traffic/origins-overtime"
TRAFFIC_ROUTES = "**/api/bff/traffic/routes"
ORIGINS_COUNTRIES = "**/api/bff/traffic/origins-countries"