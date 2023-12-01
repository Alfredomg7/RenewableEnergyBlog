from app import db
from datetime import datetime

# Define 'Article' class to represent the 'articles' table in the database
class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False)
    author = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"Article: <{self.title}>"