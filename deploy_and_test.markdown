# Deployment and Testing Instructions for GPA Calculator Web Service

## Deployment on Render

1. **Create a Render Account**:
   - Sign up at [render.com](https://render.com).

2. **Create a New Web Service**:
   - Click "New" > "Web Service" in the Render dashboard.
   - Connect your GitHub repository (push the code below to a new repo).

3. **Configure the Service**:
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn gpa_calculator:app`
   - Set **Environment Variables**:
     - `DATABASE_URL`: `sqlite:///gpa.db` (or use a PostgreSQL URL for production)
     - `FLASK_ENV`: `production`
   - Choose the free tier for testing.

4. **Deploy**:
   - Click "Create Web Service" to deploy. Render will build and start the service.
   - Note the generated URL (e.g., `https://your-service.onrender.com`).

5. **Database Migration**:
   - After deployment, run migrations:
     - Access the Render shell or use a local terminal with the deployed app's environment.
     - Run:
       ```bash
       flask db init
       flask db migrate
       flask db upgrade
       ```

## Testing the Web Service

Use `curl` or Postman to test the API endpoints. Replace `https://your-service.onrender.com` with your actual Render URL.

1. **Add a Course**:
   ```bash
   curl -X POST https://your-service.onrender.com/api/courses \
   -H "Content-Type: application/json" \
   -d '{"student_id":"S123","course_name":"Math","grade":"A","credits":3.0}'
   ```
   Expected Response:
   ```json
   {
     "id": 1,
     "student_id": "S123",
     "course_name": "Math",
     "grade": "A",
     "credits": 3.0
   }
   ```

2. **Get Courses for a Student**:
   ```bash
   curl https://your-service.onrender.com/api/courses/S123
   ```
   Expected Response:
   ```json
   [
     {
       "id": 1,
       "student_id": "S123",
       "course_name": "Math",
       "grade": "A",
       "credits": 3.0
     }
   ]
   ```

3. **Calculate GPA**:
   ```bash
   curl https://your-service.onrender.com/api/gpa/S123
   ```
   Expected Response:
   ```json
   {
     "student_id": "S123",
     "gpa": 4.0
   }
   ```

4. **Update a Course**:
   ```bash
   curl -X PUT https://your-service.onrender.com/api/courses/1 \
   -H "Content-Type: application/json" \
   -d '{"grade":"B","credits":4.0}'
   ```
   Expected Response:
   ```json
   {
     "id": 1,
     "student_id": "S123",
     "course_name": "Math",
     "grade": "B",
     "credits": 4.0
   }
   ```

5. **Delete a Course**:
   ```bash
   curl -X DELETE https://your-service.onrender.com/api/courses/1
   ```
   Expected Response:
   ```json
   {
     "message": "Course deleted"
   }
   ```

## Local Testing (Optional)

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python gpa_calculator.py
   ```

3. **Test Endpoints**:
   - Use the same `curl` commands, replacing the URL with `http://localhost:5000`.

## Notes
- The service uses SQLite for simplicity. For production, consider PostgreSQL (Render provides it).
- Ensure the `DATABASE_URL` environment variable is set correctly for your database.
- The API validates grades and credits to ensure data integrity.
- Error handling is implemented for invalid inputs and missing resources.