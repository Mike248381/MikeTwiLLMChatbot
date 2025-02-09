from twibot import app

try: 
    if  __name__ == '__main__':
        app.run(debug=True,port=8080)
except:
    print("Exception occured!")
    from werkzeug.serving import run_simple
    run_simple('localhost', 9000, app)