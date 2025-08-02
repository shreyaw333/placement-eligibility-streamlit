"""
Placement Eligibility Data Generator
Generates synthetic student data using Faker library for 4 related tables:
- Students Table
- Programming Table  
- Soft Skills Table
- Placements Table
"""

import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker
import pandas as pd

# Initialize Faker
fake = Faker()

class StudentDataGenerator:
    def __init__(self, db_path="data/students.db", num_students=500):
        """
        Initialize data generator
        
        Args:
            db_path (str): Path to SQLite database file
            num_students (int): Number of students to generate
        """
        self.db_path = db_path
        self.num_students = num_students
        self.conn = None
        
        # Data lists for realistic generation
        self.course_batches = [
            "DS_2023_A", "DS_2023_B", "DS_2024_A", "DS_2024_B", 
            "AIML_2023_A", "AIML_2024_A", "DE_2023_A", "DE_2024_A"
        ]
        
        self.cities = [
            "Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", 
            "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow",
            "Indore", "Bhopal", "Patna", "Vadodara", "Ludhiana"
        ]
        
        self.programming_languages = ["Python", "SQL", "R", "Java", "JavaScript"]
        
        self.companies = [
            "TCS", "Infosys", "Wipro", "Accenture", "IBM", "Cognizant",
            "Microsoft", "Amazon", "Google", "Flipkart", "Paytm", 
            "Zomato", "Swiggy", "BYJU'S", "Unacademy", "PhonePe",
            "Razorpay", "Freshworks", "Zoho", "HCL Technologies"
        ]
        
        self.placement_statuses = ["Ready", "Not Ready", "Placed", "In Progress"]
        
    def create_database_connection(self):
        """Create database connection and tables"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.create_tables()
            print(f"✅ Database connection established: {self.db_path}")
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            
    def create_tables(self):
        """Create all required tables with proper schema"""
        
        # Students Table
        students_table = """
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            email TEXT UNIQUE,
            phone TEXT,
            enrollment_year INTEGER,
            course_batch TEXT,
            city TEXT,
            graduation_year INTEGER
        );
        """
        
        # Programming Table
        programming_table = """
        CREATE TABLE IF NOT EXISTS programming (
            programming_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            language TEXT,
            problems_solved INTEGER,
            assessments_completed INTEGER,
            mini_projects INTEGER,
            certifications_earned INTEGER,
            latest_project_score INTEGER,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
        );
        """
        
        # Soft Skills Table
        soft_skills_table = """
        CREATE TABLE IF NOT EXISTS soft_skills (
            soft_skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            communication INTEGER,
            teamwork INTEGER,
            presentation INTEGER,
            leadership INTEGER,
            critical_thinking INTEGER,
            interpersonal_skills INTEGER,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
        );
        """
        
        # Placements Table
        placements_table = """
        CREATE TABLE IF NOT EXISTS placements (
            placement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            mock_interview_score INTEGER,
            internships_completed INTEGER,
            placement_status TEXT,
            company_name TEXT,
            placement_package INTEGER,
            interview_rounds_cleared INTEGER,
            placement_date TEXT,
            FOREIGN KEY (student_id) REFERENCES students (student_id)
        );
        """
        
        # Execute table creation
        tables = [students_table, programming_table, soft_skills_table, placements_table]
        
        for table in tables:
            self.conn.execute(table)
        
        self.conn.commit()
        print("✅ All tables created successfully")
    
    def generate_students_data(self):
        """Generate realistic student data"""
        students = []
        
        for i in range(1, self.num_students + 1):
            # Generate realistic student data
            first_name = fake.first_name()
            last_name = fake.last_name()
            full_name = f"{first_name} {last_name}"
            
            age = random.randint(20, 26)
            gender = random.choice(["Male", "Female", "Other"])
            
            # Generate email based on name
            email_prefix = f"{first_name.lower()}.{last_name.lower()}"
            email = f"{email_prefix}{random.randint(10, 99)}@email.com"
            
            phone = fake.phone_number()[:15]  # Limit phone number length
            
            # Enrollment and graduation years based on batch
            batch = random.choice(self.course_batches)
            enrollment_year = int(batch.split('_')[1])  # Extract year from batch
            graduation_year = enrollment_year + random.choice([1, 2])  # 1-2 year course
            
            city = random.choice(self.cities)
            
            student = (
                full_name, age, gender, email, phone,
                enrollment_year, batch, city, graduation_year
            )
            
            students.append(student)
        
        return students
    
    def generate_programming_data(self, student_ids):
        """Generate programming performance data"""
        programming_data = []
        
        for student_id in student_ids:
            # Each student can have multiple programming language entries
            num_languages = random.randint(1, 3)  # 1-3 programming languages
            selected_languages = random.sample(self.programming_languages, num_languages)
            
            for language in selected_languages:
                # Generate performance metrics based on realistic distributions
                if language == "Python":
                    problems_solved = random.randint(15, 150)
                    base_score = random.randint(60, 95)
                elif language == "SQL":
                    problems_solved = random.randint(10, 80)
                    base_score = random.randint(55, 90)
                else:
                    problems_solved = random.randint(5, 60)
                    base_score = random.randint(50, 85)
                
                assessments_completed = random.randint(3, 12)
                mini_projects = random.randint(1, 8)
                certifications_earned = random.randint(0, 5)
                latest_project_score = base_score + random.randint(-10, 15)
                latest_project_score = max(0, min(100, latest_project_score))  # Cap between 0-100
                
                programming_entry = (
                    student_id, language, problems_solved, assessments_completed,
                    mini_projects, certifications_earned, latest_project_score
                )
                
                programming_data.append(programming_entry)
        
        return programming_data
    
    def generate_soft_skills_data(self, student_ids):
        """Generate soft skills scores for each student"""
        soft_skills_data = []
        
        for student_id in student_ids:
            # Generate correlated soft skills (students good in one area tend to be good in others)
            base_performance = random.randint(40, 90)  # Base performance level
            variation = 15  # How much skills can vary from base
            
            communication = max(0, min(100, base_performance + random.randint(-variation, variation)))
            teamwork = max(0, min(100, base_performance + random.randint(-variation, variation)))
            presentation = max(0, min(100, base_performance + random.randint(-variation, variation)))
            leadership = max(0, min(100, base_performance + random.randint(-variation, variation)))
            critical_thinking = max(0, min(100, base_performance + random.randint(-variation, variation)))
            interpersonal_skills = max(0, min(100, base_performance + random.randint(-variation, variation)))
            
            soft_skills_entry = (
                student_id, communication, teamwork, presentation,
                leadership, critical_thinking, interpersonal_skills
            )
            
            soft_skills_data.append(soft_skills_entry)
        
        return soft_skills_data
    
    def generate_placements_data(self, student_ids):
        """Generate placement-related data"""
        placements_data = []
        
        for student_id in student_ids:
            # Mock interview score correlated with overall performance
            mock_interview_score = random.randint(35, 95)
            
            # Internships completed
            internships_completed = random.randint(0, 4)
            
            # Placement status based on performance indicators
            if mock_interview_score >= 80 and internships_completed >= 1:
                placement_status = random.choices(
                    self.placement_statuses, 
                    weights=[20, 5, 60, 15]  # Higher chance of being placed
                )[0]
            elif mock_interview_score >= 60:
                placement_status = random.choices(
                    self.placement_statuses,
                    weights=[40, 20, 25, 15]  # Moderate chance
                )[0]
            else:
                placement_status = random.choices(
                    self.placement_statuses,
                    weights=[20, 60, 10, 10]  # Lower chance of being placed
                )[0]
            
            # Company and package details for placed students
            if placement_status == "Placed":
                company_name = random.choice(self.companies)
                # Package based on company tier and performance
                if company_name in ["Microsoft", "Amazon", "Google"]:
                    placement_package = random.randint(800000, 2500000)  # High-tier companies
                elif company_name in ["TCS", "Infosys", "Wipro", "Cognizant"]:
                    placement_package = random.randint(300000, 800000)  # Service companies
                else:
                    placement_package = random.randint(400000, 1200000)  # Mid-tier companies
                
                # Placement date (recent dates)
                placement_date = fake.date_between(start_date='-6m', end_date='today')
            else:
                company_name = None
                placement_package = None
                placement_date = None
            
            # Interview rounds cleared
            interview_rounds_cleared = random.randint(0, 6)
            
            placements_entry = (
                student_id, mock_interview_score, internships_completed,
                placement_status, company_name, placement_package,
                interview_rounds_cleared, placement_date
            )
            
            placements_data.append(placements_entry)
        
        return placements_data
    
    def insert_data_to_database(self):
        """Insert all generated data into database tables"""
        
        # Generate students data
        print("📊 Generating students data...")
        students_data = self.generate_students_data()
        
        # Insert students
        insert_students_query = """
        INSERT INTO students (name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        self.conn.executemany(insert_students_query, students_data)
        self.conn.commit()
        print(f"✅ Inserted {len(students_data)} students")
        
        # Get student IDs for foreign key relationships
        cursor = self.conn.execute("SELECT student_id FROM students")
        student_ids = [row[0] for row in cursor.fetchall()]
        
        # Generate and insert programming data
        print("💻 Generating programming data...")
        programming_data = self.generate_programming_data(student_ids)
        
        insert_programming_query = """
        INSERT INTO programming (student_id, language, problems_solved, assessments_completed, 
                               mini_projects, certifications_earned, latest_project_score)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        self.conn.executemany(insert_programming_query, programming_data)
        self.conn.commit()
        print(f"✅ Inserted {len(programming_data)} programming records")
        
        # Generate and insert soft skills data
        print("🤝 Generating soft skills data...")
        soft_skills_data = self.generate_soft_skills_data(student_ids)
        
        insert_soft_skills_query = """
        INSERT INTO soft_skills (student_id, communication, teamwork, presentation, 
                               leadership, critical_thinking, interpersonal_skills)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        self.conn.executemany(insert_soft_skills_query, soft_skills_data)
        self.conn.commit()
        print(f"✅ Inserted {len(soft_skills_data)} soft skills records")
        
        # Generate and insert placements data
        print("🎯 Generating placements data...")
        placements_data = self.generate_placements_data(student_ids)
        
        insert_placements_query = """
        INSERT INTO placements (student_id, mock_interview_score, internships_completed, 
                              placement_status, company_name, placement_package, 
                              interview_rounds_cleared, placement_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        self.conn.executemany(insert_placements_query, placements_data)
        self.conn.commit()
        print(f"✅ Inserted {len(placements_data)} placement records")
    
    def generate_data_summary(self):
        """Generate summary statistics of the created data"""
        print("\n" + "="*60)
        print("📈 DATA GENERATION SUMMARY")
        print("="*60)
        
        # Students summary
        cursor = self.conn.execute("SELECT COUNT(*) FROM students")
        total_students = cursor.fetchone()[0]
        print(f"👥 Total Students: {total_students}")
        
        # Programming summary
        cursor = self.conn.execute("SELECT COUNT(*), AVG(problems_solved) FROM programming")
        prog_count, avg_problems = cursor.fetchone()
        print(f"💻 Programming Records: {prog_count}")
        print(f"📊 Average Problems Solved: {avg_problems:.1f}")
        
        # Placement status summary
        cursor = self.conn.execute("""
            SELECT placement_status, COUNT(*) 
            FROM placements 
            GROUP BY placement_status
        """)
        placement_stats = cursor.fetchall()
        print(f"🎯 Placement Status Distribution:")
        for status, count in placement_stats:
            print(f"   {status}: {count}")
        
        # Company summary for placed students
        cursor = self.conn.execute("""
            SELECT COUNT(*) FROM placements 
            WHERE placement_status = 'Placed' AND company_name IS NOT NULL
        """)
        placed_count = cursor.fetchone()[0]
        print(f"🏢 Students Successfully Placed: {placed_count}")
        
        print("="*60)
        print("✅ Data generation completed successfully!")
        print(f"📁 Database saved at: {self.db_path}")
    
    def close_connection(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("🔌 Database connection closed")

def main():
    """Main function to generate all student data"""
    print("🚀 Starting Student Data Generation...")
    print("-" * 50)
    
    # Initialize data generator
    generator = StudentDataGenerator(num_students=500)
    
    try:
        # Create database and tables
        generator.create_database_connection()
        
        # Generate and insert all data
        generator.insert_data_to_database()
        
        # Show summary
        generator.generate_data_summary()
        
    except Exception as e:
        print(f"❌ Error during data generation: {e}")
    
    finally:
        # Close connection
        generator.close_connection()

if __name__ == "__main__":
    main()