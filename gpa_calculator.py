from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///gpa.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Grade points mapping
GRADE_POINTS = {
    'A+': 4.0, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D+': 1.3, 'D': 1.0, 'F': 0.0
}

# Database model for Course
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(2), nullable=False)
    credits = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'course_name': self.course_name,
            'grade': self.grade,
            'credits': self.credits
        }

# Create database tables
with app.app_context():
    db.create_all()

# Helper function to calculate GPA
def calculate_gpa(courses):
    total_points = 0.0
    total_credits = 0.0
    for course in courses:
        total_points += GRADE_POINTS.get(course.grade, 0.0) * course.credits
        total_credits += course.credits
    return round(total_points / total_credits, 2) if total_credits > 0 else 0.0

# API Routes
@app.route('/api/courses', methods=['POST'])
def add_course():
    data = request.get_json()
    if not all(key in data for key in ['student_id', 'course_name', 'grade', 'credits']):
        return jsonify({'error': 'Missing required fields'}), 400
    if data['grade'] not in GRADE_POINTS:
        return jsonify({'error': 'Invalid grade'}), 400
    if data['credits'] <= 0:
        return jsonify({'error': 'Credits must be positive'}), 400

    course = Course(
        student_id=data['student_id'],
        course_name=data['course_name'],
        grade=data['grade'],
        credits=data['credits']
    )
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201

@app.route('/api/courses/<student_id>', methods=['GET'])
def get_courses(student_id):
    courses = Course.query.filter_by(student_id=student_id).all()
    return jsonify([course.to_dict() for course in courses]), 200

@app.route('/api/gpa/<student_id>', methods=['GET'])
def get_gpa(student_id):
    courses = Course.query.filter_by(student_id=student_id).all()
    if not courses:
        return jsonify({'error': 'No courses found for student'}), 404
    gpa = calculate_gpa(courses)
    return jsonify({'student_id': student_id, 'gpa': gpa}), 200

@app.route('/api/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    if 'grade' in data and data['grade'] not in GRADE_POINTS:
        return jsonify({'error': 'Invalid grade'}), 400
    if 'credits' in data and data['credits'] <= 0:
        return jsonify({'error': 'Credits must be positive'}), 400

    course.course_name = data.get('course_name', course.course_name)
    course.grade = data.get('grade', course.grade)
    course.credits = data.get('credits', course.credits)
    db.session.commit()
    return jsonify(course.to_dict()), 200

@app.route('/api/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)