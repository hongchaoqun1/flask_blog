from markdown import markdown
import bleach
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db
from . import login_manager


collections = db.Table('collections',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'))
)



class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('Post', backref="author", lazy="dynamic")
    collection = db.relationship('Post', secondary=collections, backref=db.backref('collector', lazy='dynamic'), lazy="dynamic")

    location  = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    

    def __repr__(self):
        return '<username %r>' % self.username

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def isCollection(self, post_id):
        if self.collection.filter_by(id=post_id).first() is not None:
            return 1
        else:
            return 0

    def addCollection(self, pid):
        self.collection.append(Post.query.filter_by(id=pid)[0])
        db.session.add(self)
        db.session.commit()

        
    def rmCollection(self, pid):
        self.collection.remove(Post.query.filter_by(id=pid)[0])
        db.session.add(self)
        db.session.commit()

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    
@login_manager.user_loader
def load_user(user_id): 
    return User.query.get(int(user_id))


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    body_html = db.Column(db.Text)
    pid = db.Column(db.Integer, default=0)
    path = db.Column(db.String(128), default='0,')
    comment = db.Column(db.Text)
    
    @staticmethod
    def onChangedBody(target, value, oldvalue, initiator):
        allowed_tas = ['a','addr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'h4','h5', 'p']
        target.body_html = bleach.linkify(bleach.clean(markdown(value, output_format='html'), tags=allowed_tas, strip=True))

    def make_path(self,sub=True):
        father = Post.query.filter_by(id=self.pid)
        f = father[0]
        f_path = f.path
        if sub:
            self.path = f_path + str(self.id) + ","
        else:
            self.path = f_path + str(self.pid) + "," + str(self.id) + ","

db.event.listen(Post.body, 'set', Post.onChangedBody)    


