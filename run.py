from app import create_app

app     = create_app()

if __name__ == "__main__":
    app.run(debug=True,
            threaded=True,
            host="0.0.0.0",
            port=80)
    
    '''
    crt     = f"/root/main_dev/ssl/cert1.pem"
    key     = f"/root/main_dev/ssl/privkey1.pem"
    app.run(debug=True,
            threaded=True,
            host="0.0.0.0",
            port=8000,
            ssl_context=(crt, key))
        '''
