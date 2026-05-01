from app import db
from flask_login import UserMixin
from datetime import datetime
import bcrypt


class AdminUser(UserMixin, db.Model):
    """Admin user model for authentication"""
    __tablename__ = 'admin_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Verify password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def __repr__(self):
        return f'<AdminUser {self.username}>'


class Wing(db.Model):
    """Wing/Tower model"""
    __tablename__ = 'wings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    nominees = db.relationship('Nominee', backref='wing', lazy=True, cascade='all, delete-orphan')
    voters = db.relationship('Voter', backref='wing', lazy=True)
    results = db.relationship('Result', backref='wing', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Wing {self.name}>'


class Nominee(db.Model):
    """Nominee model"""
    __tablename__ = 'nominees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # 'male' or 'female'
    flat_number = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    wing_id = db.Column(db.Integer, db.ForeignKey('wings.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    votes = db.relationship('Vote', backref='nominee', lazy=True)
    results = db.relationship('Result', backref='nominee', lazy=True)

    # Indexes for faster queries
    __table_args__ = (
        db.Index('idx_wing_gender', 'wing_id', 'gender'),
    )

    def __repr__(self):
        return f'<Nominee {self.name} ({self.gender})>'


class Voter(db.Model):
    """Voter model - tracks who has voted"""
    __tablename__ = 'voters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    flat_number = db.Column(db.String(20), nullable=False)
    wing_id = db.Column(db.Integer, db.ForeignKey('wings.id'), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)  # Optional field
    counter_number = db.Column(db.Integer, unique=True, nullable=False)
    voted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    votes = db.relationship('Vote', backref='voter', lazy=True, cascade='all, delete-orphan')

    # Unique constraint - one vote per flat per wing
    __table_args__ = (
        db.UniqueConstraint('flat_number', 'wing_id', name='unique_flat_wing'),
    )

    def __repr__(self):
        return f'<Voter {self.name} - Flat {self.flat_number}>'


class Vote(db.Model):
    """Vote model - tracks individual votes for nominees"""
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('voters.id'), nullable=False)
    nominee_id = db.Column(db.Integer, db.ForeignKey('nominees.id'), nullable=False)
    voted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Vote {self.voter_id} -> {self.nominee_id}>'


class Result(db.Model):
    """Result model - stores declared results"""
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    wing_id = db.Column(db.Integer, db.ForeignKey('wings.id'), nullable=False)
    nominee_id = db.Column(db.Integer, db.ForeignKey('nominees.id'), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    vote_count = db.Column(db.Integer, nullable=False, default=0)
    rank = db.Column(db.Integer, nullable=False)
    is_winner = db.Column(db.Boolean, default=False, nullable=False)
    declared_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Result {self.nominee_id} - Rank {self.rank}>'


class ConfigSetting(db.Model):
    """Configuration settings model"""
    __tablename__ = 'config_settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(200), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def get_value(key, default=None):
        """Get configuration value"""
        setting = ConfigSetting.query.filter_by(key=key).first()
        return setting.value if setting else default

    @staticmethod
    def set_value(key, value):
        """Set configuration value"""
        setting = ConfigSetting.query.filter_by(key=key).first()
        if setting:
            setting.value = value
            setting.updated_at = datetime.utcnow()
        else:
            setting = ConfigSetting(key=key, value=value)
            db.session.add(setting)
        db.session.commit()

    @staticmethod
    def is_voting_enabled():
        """Check if voting is enabled"""
        return ConfigSetting.get_value('voting_enabled', 'true').lower() == 'true'

    @staticmethod
    def are_results_visible():
        """Check if results are visible"""
        return ConfigSetting.get_value('results_visible', 'false').lower() == 'true'

    @staticmethod
    def get_winners_per_gender():
        """Get number of winners per gender"""
        return int(ConfigSetting.get_value('winners_per_gender', '2'))

    def __repr__(self):
        return f'<ConfigSetting {self.key}={self.value}>'


class ArchivedElection(db.Model):
    """Archived election data model"""
    __tablename__ = 'archived_elections'

    id = db.Column(db.Integer, primary_key=True)
    election_name = db.Column(db.String(200), nullable=False)
    election_data = db.Column(db.Text, nullable=False)  # JSON string
    archived_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_votes = db.Column(db.Integer, default=0)
    total_nominees = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<ArchivedElection {self.election_name}>'
