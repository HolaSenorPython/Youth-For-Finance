from main import app, db

# Actually create db
with app.app_context():
    print("Making db...")
    db.create_all()