"""
Database Connection and Query Management Class
Handles all database operations for the Placement Eligibility Streamlit Application
"""

import sqlite3
import pandas as pd
from typing import List, Dict, Any, Optional, Tuple
import logging
from contextlib import contextmanager

class DatabaseManager:
    """
    Database Manager class for handling all database operations
    Implements OOP principles for clean and modular database interactions
    """
    
    def __init__(self, db_path: str = "data/students.db"):
        """
        Initialize Database Manager
        
        Args:
            db_path (str): Path to SQLite database file
        """
        self.db_path = db_path
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for database operations"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections
        Ensures proper connection handling and cleanup
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            yield conn
        except sqlite3.Error as e:
            self.logger.error(f"Database error: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    def test_connection(self) -> bool:
        """
        Test database connection and verify tables exist
        
        Returns:
            bool: True if connection successful and tables exist
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if all required tables exist
                required_tables = ['students', 'programming', 'soft_skills', 'placements']
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name IN (?, ?, ?, ?)
                """, required_tables)
                
                existing_tables = [row[0] for row in cursor.fetchall()]
                
                if len(existing_tables) == 4:
                    self.logger.info("✅ Database connection successful - All tables found")
                    return True
                else:
                    missing_tables = set(required_tables) - set(existing_tables)
                    self.logger.error(f"❌ Missing tables: {missing_tables}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"❌ Database connection failed: {e}")
            return False
    
    def get_database_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of the database
        
        Returns:
            Dict with database statistics
        """
        try:
            with self.get_connection() as conn:
                summary = {}
                
                # Students count
                cursor = conn.execute("SELECT COUNT(*) FROM students")
                summary['total_students'] = cursor.fetchone()[0]
                
                # Programming records count
                cursor = conn.execute("SELECT COUNT(*) FROM programming")
                summary['programming_records'] = cursor.fetchone()[0]
                
                # Placement status distribution
                cursor = conn.execute("""
                    SELECT placement_status, COUNT(*) as count
                    FROM placements 
                    GROUP BY placement_status
                """)
                summary['placement_distribution'] = dict(cursor.fetchall())
                
                # Average scores
                cursor = conn.execute("""
                    SELECT 
                        AVG(problems_solved) as avg_problems,
                        AVG(latest_project_score) as avg_project_score
                    FROM programming
                """)
                avg_data = cursor.fetchone()
                summary['avg_problems_solved'] = round(avg_data[0], 1)
                summary['avg_project_score'] = round(avg_data[1], 1)
                
                return summary
                
        except Exception as e:
            self.logger.error(f"Error getting database summary: {e}")
            return {}
    
    def get_eligible_students(self, criteria: Dict[str, Any]) -> pd.DataFrame:
        """
        Get students who meet the specified eligibility criteria
        
        Args:
            criteria (Dict): Dictionary with eligibility criteria
                Example: {
                    'min_problems_solved': 50,
                    'min_soft_skills_avg': 75,
                    'min_mock_interview': 60,
                    'min_internships': 1,
                    'programming_language': 'Python',
                    'placement_status': ['Ready', 'Placed']
                }
        
        Returns:
            pd.DataFrame: Eligible students with their details
        """
        try:
            # Build dynamic query based on criteria
            base_query = """
            SELECT DISTINCT
                s.student_id,
                s.name,
                s.age,
                s.gender,
                s.email,
                s.phone,
                s.course_batch,
                s.city,
                p.placement_status,
                p.mock_interview_score,
                p.internships_completed,
                p.company_name,
                p.placement_package,
                ROUND(AVG(ss.communication + ss.teamwork + ss.presentation + 
                         ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6.0, 1) as avg_soft_skills,
                GROUP_CONCAT(DISTINCT prog.language) as programming_languages,
                MAX(prog.problems_solved) as max_problems_solved,
                MAX(prog.latest_project_score) as best_project_score
            FROM students s
            JOIN placements p ON s.student_id = p.student_id
            JOIN soft_skills ss ON s.student_id = ss.student_id
            LEFT JOIN programming prog ON s.student_id = prog.student_id
            WHERE 1=1
            """
            
            conditions = []
            params = []
            
            # Add conditions based on criteria
            if criteria.get('min_problems_solved'):
                conditions.append("prog.problems_solved >= ?")
                params.append(criteria['min_problems_solved'])
            
            if criteria.get('min_soft_skills_avg'):
                conditions.append("""
                    (ss.communication + ss.teamwork + ss.presentation + 
                     ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6.0 >= ?
                """)
                params.append(criteria['min_soft_skills_avg'])
            
            if criteria.get('min_mock_interview'):
                conditions.append("p.mock_interview_score >= ?")
                params.append(criteria['min_mock_interview'])
            
            if criteria.get('min_internships'):
                conditions.append("p.internships_completed >= ?")
                params.append(criteria['min_internships'])
            
            if criteria.get('programming_language'):
                conditions.append("prog.language = ?")
                params.append(criteria['programming_language'])
            
            if criteria.get('placement_status'):
                status_list = criteria['placement_status']
                if isinstance(status_list, str):
                    status_list = [status_list]
                placeholders = ','.join(['?' for _ in status_list])
                conditions.append(f"p.placement_status IN ({placeholders})")
                params.extend(status_list)
            
            if criteria.get('course_batch'):
                conditions.append("s.course_batch = ?")
                params.append(criteria['course_batch'])
            
            if criteria.get('city'):
                conditions.append("s.city = ?")
                params.append(criteria['city'])
            
            # Add conditions to query
            if conditions:
                base_query += " AND " + " AND ".join(conditions)
            
            # Group by and order
            base_query += """
            GROUP BY s.student_id, s.name, s.age, s.gender, s.email, s.phone, 
                     s.course_batch, s.city, p.placement_status, p.mock_interview_score, 
                     p.internships_completed, p.company_name, p.placement_package
            ORDER BY avg_soft_skills DESC, max_problems_solved DESC, p.mock_interview_score DESC
            """
            
            with self.get_connection() as conn:
                df = pd.read_sql_query(base_query, conn, params=params)
                
            self.logger.info(f"Found {len(df)} eligible students")
            return df
            
        except Exception as e:
            self.logger.error(f"Error getting eligible students: {e}")
            return pd.DataFrame()
    
    def get_filter_options(self) -> Dict[str, List]:
        """
        Get available options for filters (for Streamlit dropdowns)
        
        Returns:
            Dict with available filter options
        """
        try:
            with self.get_connection() as conn:
                options = {}
                
                # Course batches
                cursor = conn.execute("SELECT DISTINCT course_batch FROM students ORDER BY course_batch")
                options['course_batches'] = [row[0] for row in cursor.fetchall()]
                
                # Cities
                cursor = conn.execute("SELECT DISTINCT city FROM students ORDER BY city")
                options['cities'] = [row[0] for row in cursor.fetchall()]
                
                # Programming languages
                cursor = conn.execute("SELECT DISTINCT language FROM programming ORDER BY language")
                options['programming_languages'] = [row[0] for row in cursor.fetchall()]
                
                # Placement statuses
                cursor = conn.execute("SELECT DISTINCT placement_status FROM placements ORDER BY placement_status")
                options['placement_statuses'] = [row[0] for row in cursor.fetchall()]
                
                # Companies (for placed students)
                cursor = conn.execute("""
                    SELECT DISTINCT company_name FROM placements 
                    WHERE company_name IS NOT NULL 
                    ORDER BY company_name
                """)
                options['companies'] = [row[0] for row in cursor.fetchall()]
                
                return options
                
        except Exception as e:
            self.logger.error(f"Error getting filter options: {e}")
            return {}
    
    def get_student_details(self, student_id: int) -> Dict[str, Any]:
        """
        Get comprehensive details for a specific student
        
        Args:
            student_id (int): Student ID
            
        Returns:
            Dict with all student information
        """
        try:
            with self.get_connection() as conn:
                # Student basic info
                cursor = conn.execute("""
                    SELECT * FROM students WHERE student_id = ?
                """, (student_id,))
                student_data = dict(cursor.fetchone())
                
                # Programming data
                cursor = conn.execute("""
                    SELECT * FROM programming WHERE student_id = ?
                """, (student_id,))
                student_data['programming'] = [dict(row) for row in cursor.fetchall()]
                
                # Soft skills data
                cursor = conn.execute("""
                    SELECT * FROM soft_skills WHERE student_id = ?
                """, (student_id,))
                student_data['soft_skills'] = dict(cursor.fetchone())
                
                # Placement data
                cursor = conn.execute("""
                    SELECT * FROM placements WHERE student_id = ?
                """, (student_id,))
                student_data['placement'] = dict(cursor.fetchone())
                
                return student_data
                
        except Exception as e:
            self.logger.error(f"Error getting student details: {e}")
            return {}
    
    def execute_custom_query(self, query: str, params: Tuple = ()) -> pd.DataFrame:
        """
        Execute a custom SQL query and return results as DataFrame
        
        Args:
            query (str): SQL query to execute
            params (Tuple): Query parameters
            
        Returns:
            pd.DataFrame: Query results
        """
        try:
            with self.get_connection() as conn:
                df = pd.read_sql_query(query, conn, params=params)
                return df
                
        except Exception as e:
            self.logger.error(f"Error executing custom query: {e}")
            return pd.DataFrame()
    
    def get_placement_analytics(self) -> Dict[str, Any]:
        """
        Get comprehensive placement analytics
        
        Returns:
            Dict with placement analytics data
        """
        try:
            with self.get_connection() as conn:
                analytics = {}
                
                # Overall placement rate
                cursor = conn.execute("""
                    SELECT 
                        placement_status,
                        COUNT(*) as count,
                        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM placements), 1) as percentage
                    FROM placements 
                    GROUP BY placement_status
                """)
                analytics['placement_distribution'] = [dict(row) for row in cursor.fetchall()]
                
                # Average package by company
                cursor = conn.execute("""
                    SELECT 
                        company_name,
                        COUNT(*) as students_placed,
                        ROUND(AVG(placement_package), 0) as avg_package,
                        MIN(placement_package) as min_package,
                        MAX(placement_package) as max_package
                    FROM placements 
                    WHERE placement_status = 'Placed' AND company_name IS NOT NULL
                    GROUP BY company_name
                    ORDER BY avg_package DESC
                """)
                analytics['company_packages'] = [dict(row) for row in cursor.fetchall()]
                
                # Skills vs placement success
                cursor = conn.execute("""
                    SELECT 
                        p.placement_status,
                        ROUND(AVG(ss.communication), 1) as avg_communication,
                        ROUND(AVG(ss.teamwork), 1) as avg_teamwork,
                        ROUND(AVG(ss.presentation), 1) as avg_presentation,
                        ROUND(AVG(ss.leadership), 1) as avg_leadership,
                        ROUND(AVG(p.mock_interview_score), 1) as avg_mock_interview,
                        ROUND(AVG(prog.problems_solved), 1) as avg_problems_solved
                    FROM placements p
                    JOIN soft_skills ss ON p.student_id = ss.student_id
                    LEFT JOIN programming prog ON p.student_id = prog.student_id
                    GROUP BY p.placement_status
                """)
                analytics['skills_by_placement_status'] = [dict(row) for row in cursor.fetchall()]
                
                return analytics
                
        except Exception as e:
            self.logger.error(f"Error getting placement analytics: {e}")
            return {}


# Example usage and testing
if __name__ == "__main__":
    # Initialize database manager
    db_manager = DatabaseManager()
    
    # Test connection
    if db_manager.test_connection():
        print("🎉 Database connection successful!")
        
        # Get database summary
        summary = db_manager.get_database_summary()
        print(f"\n📊 Database Summary:")
        for key, value in summary.items():
            print(f"   {key}: {value}")
        
        # Test eligibility filter
        criteria = {
            'min_problems_solved': 30,
            'min_soft_skills_avg': 60,
            'min_mock_interview': 50
        }
        
        eligible_students = db_manager.get_eligible_students(criteria)
        print(f"\n👥 Found {len(eligible_students)} eligible students with criteria: {criteria}")
        
        # Get filter options
        options = db_manager.get_filter_options()
        print(f"\n🎛️ Available filter options:")
        for key, values in options.items():
            print(f"   {key}: {len(values)} options")
    
    else:
        print("❌ Database connection failed!")