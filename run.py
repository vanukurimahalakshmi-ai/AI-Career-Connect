from app import create_app

app = create_app()



if __name__ == '__main__':
    print("==================================================")
    print(" 🚀 AI CAREER CONNECT SERVER RUNNING")
    print(" 📍 Local URL: http://127.0.0.1:5000")
    print(" ==================================================")
    app.run(host='0.0.0.0', port=5000, debug=True)
