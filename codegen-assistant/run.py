from app import create_app

app = create_app()

if __name__ == '__main__':
    # Debug modunda çalıştır, üretim ortamında debug=False olmalıdır
    app.run(host='0.0.0.0', port=5001, debug=True) 