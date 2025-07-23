# tiny_url

## Description
This project is a Python API application that allows to create a short url that can redirect to a longer url when called.  
Two endpoints are exposed:  
- The first one allows the creation and storage of the short url (POST: /url/generate_slug)
- The second allows the redirection  (GET: /url/{slug})


## Installation
Clone the repository: 
git clone https://github.com/Julien-Ortonovi/tiny_url.git

Install dependencies:  
```
pip install --upgrade pip
pip install poetry
poetry install
```

Run:
```
uvicorn tiny_url.main:local_app --port {PORT}
```

To check routes documentation:
```
http://127.0.0.1:{PORT}/docs
```

## Todo next
- Unit test:
  - Test both routes, succes and failures
  - Test database creation
- Features:
  - Shortening the same url returns the same short Url
  - Retry on duplicated slug_url
