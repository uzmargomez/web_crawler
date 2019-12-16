from lda import app

def lda_app():
    app.run(
        host='0.0.0.0',
        port='5001',
        debug=True,
    )
