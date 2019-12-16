from scraper import app

def scraper_app():
    app.run(
        host='0.0.0.0',
        port='5002',
        debug=True,
    )
