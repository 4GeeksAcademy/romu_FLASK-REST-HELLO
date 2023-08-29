from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(60), unique=False, nullable=False)
    phone = db.Column(db.String(10), unique=False, nullable=True)
    
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "phone": self.phone
        }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=False, nullable=False)
    body = db.Column(db.String(1000), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    user = db.relationship("User")

    def __repr__(self):
        return f"<Este es el Post!>"
    
    def serialize(self):
        return {"id": self.id,
                "title": self.title,
                "body": self.body}


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=False, nullable=False)
    body = db.Column(db.String(1000), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)
    user = db.relationship("User")
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"),nullable=False)
    post = db.relationship("Post")


    def serialize(self):
        return {"id": self.id,
                "title": self.title,
                "body": self.body}


class Follower(db.Model):
    id = db.Column(db.Integer, primary_key = True)