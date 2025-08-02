"""
10 SQL Queries for Placement Eligibility Insights
These queries provide actionable insights for placement teams and academic coordinators
"""

from database import DatabaseManager
import pandas as pd
import numpy as np

class PlacementInsights:
    """
    Class containing SQL queries for placement insights and analytics
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize with database manager instance
        
        Args:
            db_manager: DatabaseManager instance
        """
        self.db = db_manager
    
    def query_1_top_placement_ready_students(self, limit: int = 10) -> pd.DataFrame:
        """
        Query 1: Top students ready for placement based on overall performance
        Combines programming skills, soft skills, and mock interview performance
        """
        query = """
        SELECT 
            s.name,
            s.course_batch,
            s.city,
            p.placement_status,
            p.mock_interview_score,
            p.internships_completed,
            ROUND(AVG(ss.communication + ss.teamwork + ss.presentation + 
                     ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6.0, 1) as avg_soft_skills,
            MAX(prog.problems_solved) as max_problems_solved,
            MAX(prog.latest_project_score) as best_project_score,
            ROUND((p.mock_interview_score * 0.4 + 
                   (ss.communication + ss.teamwork + ss.presentation + 
                    ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6.0 * 0.3 +
                   MAX(prog.latest_project_score) * 0.3), 1) as overall_score
        FROM students s
        JOIN placements p ON s.student_id = p.student_id
        JOIN soft_skills ss ON s.student_id = ss.student_id
        LEFT JOIN programming prog ON s.student_id = prog.student_id
        WHERE p.placement_status IN ('Ready', 'Placed')
        GROUP BY s.student_id, s.name, s.course_batch, s.city, p.placement_status, 
                 p.mock_interview_score, p.internships_completed, ss.communication, 
                 ss.teamwork, ss.presentation, ss.leadership, ss.critical_thinking, ss.interpersonal_skills
        ORDER BY overall_score DESC
        LIMIT ?
        """
        return self.db.execute_custom_query(query, (limit,))
    
    def query_2_programming_performance_by_batch(self) -> pd.DataFrame:
        """
        Query 2: Average programming performance metrics by course batch
        Helps identify which batches are performing better
        """
        query = """
        SELECT 
            s.course_batch,
            COUNT(DISTINCT s.student_id) as total_students,
            COUNT(DISTINCT prog.programming_id) as total_programming_records,
            ROUND(AVG(prog.problems_solved), 1) as avg_problems_solved,
            ROUND(AVG(prog.latest_project_score), 1) as avg_project_score,
            ROUND(AVG(prog.assessments_completed), 1) as avg_assessments,
            ROUND(AVG(prog.mini_projects), 1) as avg_mini_projects,
            MAX(prog.problems_solved) as max_problems_solved,
            MIN(prog.problems_solved) as min_problems_solved
        FROM students s
        LEFT JOIN programming prog ON s.student_id = prog.student_id
        GROUP BY s.course_batch
        ORDER BY avg_problems_solved DESC
        """
        return self.db.execute_custom_query(query)
    
    def query_3_soft_skills_distribution_analysis(self) -> pd.DataFrame:
        """
        Query 3: Distribution and correlation of soft skills scores
        Identifies strengths and weaknesses in soft skills development
        """
        query = """
        SELECT 
            s.course_batch,
            COUNT(*) as student_count,
            ROUND(AVG(ss.communication), 1) as avg_communication,
            ROUND(AVG(ss.teamwork), 1) as avg_teamwork,
            ROUND(AVG(ss.presentation), 1) as avg_presentation,
            ROUND(AVG(ss.leadership), 1) as avg_leadership,
            ROUND(AVG(ss.critical_thinking), 1) as avg_critical_thinking,
            ROUND(AVG(ss.interpersonal_skills), 1) as avg_interpersonal,
            ROUND(AVG((ss.communication + ss.teamwork + ss.presentation + 
                      ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6.0), 1) as overall_soft_skills
        FROM students s
        JOIN soft_skills ss ON s.student_id = ss.student_id
        GROUP BY s.course_batch
        ORDER BY overall_soft_skills DESC
        """
        return self.db.execute_custom_query(query)
    
    def query_4_placement_success_by_location(self) -> pd.DataFrame:
        """
        Query 4: Placement success rate and package analysis by city
        Helps understand geographical trends in placements
        """
        query = """
        SELECT 
            s.city,
            COUNT(*) as total_students,
            SUM(CASE WHEN p.placement_status = 'Placed' THEN 1 ELSE 0 END) as placed_students,
            ROUND(SUM(CASE WHEN p.placement_status = 'Placed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as placement_rate_percent,
            ROUND(AVG(CASE WHEN p.placement_status = 'Placed' THEN p.placement_package END), 0) as avg_package,
            MIN(CASE WHEN p.placement_status = 'Placed' THEN p.placement_package END) as min_package,
            MAX(CASE WHEN p.placement_status = 'Placed' THEN p.placement_package END) as max_package,
            ROUND(AVG(p.mock_interview_score), 1) as avg_mock_interview_score
        FROM students s
        JOIN placements p ON s.student_id = p.student_id
        GROUP BY s.city
        HAVING COUNT(*) >= 5  -- Only cities with at least 5 students
        ORDER BY placement_rate_percent DESC, avg_package DESC
        """
        return self.db.execute_custom_query(query)
    
    def query_5_company_wise_hiring_analysis(self) -> pd.DataFrame:
        """
        Query 5: Company-wise hiring patterns and package analysis
        Shows which companies are hiring most and their compensation patterns
        """
        query = """
        SELECT 
            p.company_name,
            COUNT(*) as students_hired,
            ROUND(AVG(p.placement_package), 0) as avg_package,
            MIN(p.placement_package) as min_package,
            MAX(p.placement_package) as max_package,
            ROUND(AVG(p.mock_interview_score), 1) as avg_interview_score_of_hired,
            ROUND(AVG(p.interview_rounds_cleared), 1) as avg_rounds_cleared,
            ROUND(AVG((ss.communication + ss.teamwork + ss.presentation + 
                      ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6.0), 1) as avg_soft_skills_hired
        FROM placements p
        JOIN students s ON p.student_id = s.student_id
        JOIN soft_skills ss ON s.student_id = ss.student_id
        WHERE p.placement_status = 'Placed' AND p.company_name IS NOT NULL
        GROUP BY p.company_name
        ORDER BY students_hired DESC, avg_package DESC
        """
        return self.db.execute_custom_query(query)
    
    def query_6_programming_language_impact_on_placement(self) -> pd.DataFrame:
        """
        Query 6: Impact of programming languages on placement success
        Analyzes which programming skills lead to better placement outcomes
        """
        query = """
        SELECT 
            prog.language,
            COUNT(DISTINCT s.student_id) as total_students,
            SUM(CASE WHEN p.placement_status = 'Placed' THEN 1 ELSE 0 END) as placed_students,
            ROUND(SUM(CASE WHEN p.placement_status = 'Placed' THEN 1 ELSE 0 END) * 100.0 / COUNT(DISTINCT s.student_id), 1) as placement_rate_percent,
            ROUND(AVG(prog.problems_solved), 1) as avg_problems_solved,
            ROUND(AVG(prog.latest_project_score), 1) as avg_project_score,
            ROUND(AVG(CASE WHEN p.placement_status = 'Placed' THEN p.placement_package END), 0) as avg_package_for_placed
        FROM programming prog
        JOIN students s ON prog.student_id = s.student_id
        JOIN placements p ON s.student_id = p.student_id
        GROUP BY prog.language
        ORDER BY placement_rate_percent DESC, avg_package_for_placed DESC
        """
        return self.db.execute_custom_query(query)
    
    def query_7_internship_impact_on_placement(self) -> pd.DataFrame:
        """
        Query 7: Correlation between internships completed and placement success
        Shows the importance of practical experience
        """
        query = """
        SELECT 
            p.internships_completed,
            COUNT(*) as student_count,
            SUM(CASE WHEN p.placement_status = 'Placed' THEN 1 ELSE 0 END) as placed_count,
            ROUND(SUM(CASE WHEN p.placement_status = 'Placed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as placement_rate_percent,
            ROUND(AVG(p.mock_interview_score), 1) as avg_mock_interview,
            ROUND(AVG(CASE WHEN p.placement_status = 'Placed' THEN p.placement_package END), 0) as avg_package,
            ROUND(AVG((ss.communication + ss.teamwork + ss.presentation + 
                      ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6.0), 1) as avg_soft_skills
        FROM placements p
        JOIN students s ON p.student_id = s.student_id
        JOIN soft_skills ss ON s.student_id = ss.student_id
        GROUP BY p.internships_completed
        ORDER BY p.internships_completed
        """
        return self.db.execute_custom_query(query)
    
    def query_8_students_needing_improvement(self) -> pd.DataFrame:
        """
        Query 8: Students who need improvement - actionable insights for counseling
        Identifies students at risk and specific areas for improvement
        """
        query = """
        SELECT 
            s.name,
            s.course_batch,
            s.city,
            p.placement_status,
            p.mock_interview_score,
            p.internships_completed,
            ROUND((ss.communication + ss.teamwork + ss.presentation + 
                   ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6.0, 1) as avg_soft_skills,
            MAX(prog.problems_solved) as max_problems_solved,
            MAX(prog.latest_project_score) as best_project_score,
            CASE 
                WHEN p.mock_interview_score < 50 THEN 'Interview Skills'
                WHEN MAX(prog.problems_solved) < 30 THEN 'Programming Practice'
                WHEN (ss.communication + ss.teamwork + ss.presentation + 
                      ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6.0 < 60 THEN 'Soft Skills'
                WHEN p.internships_completed = 0 THEN 'Practical Experience'
                ELSE 'General Improvement'
            END as primary_improvement_area
        FROM students s
        JOIN placements p ON s.student_id = p.student_id
        JOIN soft_skills ss ON s.student_id = ss.student_id
        LEFT JOIN programming prog ON s.student_id = prog.student_id
        WHERE p.placement_status IN ('Not Ready', 'In Progress')
        GROUP BY s.student_id, s.name, s.course_batch, s.city, p.placement_status, 
                 p.mock_interview_score, p.internships_completed, ss.communication, 
                 ss.teamwork, ss.presentation, ss.leadership, ss.critical_thinking, ss.interpersonal_skills
        ORDER BY 
            CASE p.placement_status 
                WHEN 'In Progress' THEN 1 
                WHEN 'Not Ready' THEN 2 
            END,
            p.mock_interview_score ASC
        """
        return self.db.execute_custom_query(query)
    
    def query_9_skills_gap_analysis(self) -> pd.DataFrame:
        """
        Query 9: Skills gap analysis - what skills lead to higher packages
        Helps curriculum planning and student guidance
        """
        query = """
        SELECT 
            CASE 
                WHEN p.placement_package >= 1000000 THEN 'High Package (10L+)'
                WHEN p.placement_package >= 500000 THEN 'Medium Package (5-10L)'
                WHEN p.placement_package < 500000 THEN 'Entry Package (<5L)'
                ELSE 'Not Placed'
            END as package_category,
            COUNT(*) as student_count,
            ROUND(AVG(p.mock_interview_score), 1) as avg_mock_interview,
            ROUND(AVG(ss.communication), 1) as avg_communication,
            ROUND(AVG(ss.teamwork), 1) as avg_teamwork,
            ROUND(AVG(ss.presentation), 1) as avg_presentation,
            ROUND(AVG(ss.leadership), 1) as avg_leadership,
            ROUND(AVG(ss.critical_thinking), 1) as avg_critical_thinking,
            ROUND(AVG(prog.problems_solved), 1) as avg_problems_solved,
            ROUND(AVG(prog.latest_project_score), 1) as avg_project_score,
            ROUND(AVG(p.interview_rounds_cleared), 1) as avg_rounds_cleared
        FROM placements p
        JOIN students s ON p.student_id = s.student_id
        JOIN soft_skills ss ON s.student_id = ss.student_id
        LEFT JOIN programming prog ON s.student_id = prog.student_id
        WHERE p.placement_status = 'Placed'
        GROUP BY package_category
        ORDER BY 
            CASE package_category
                WHEN 'High Package (10L+)' THEN 1
                WHEN 'Medium Package (5-10L)' THEN 2
                WHEN 'Entry Package (<5L)' THEN 3
            END
        """
        return self.db.execute_custom_query(query)
    
    def query_10_overall_program_effectiveness(self) -> pd.DataFrame:
        """
        Query 10: Overall program effectiveness metrics
        Executive summary for program evaluation and reporting
        """
        query = """
        SELECT 
            'Overall Program Performance' as metric_category,
            COUNT(DISTINCT s.student_id) as total_students,
            COUNT(DISTINCT CASE WHEN p.placement_status = 'Placed' THEN s.student_id END) as placed_students,
            ROUND(COUNT(DISTINCT CASE WHEN p.placement_status = 'Placed' THEN s.student_id END) * 100.0 / COUNT(DISTINCT s.student_id), 1) as overall_placement_rate,
            ROUND(AVG(CASE WHEN p.placement_status = 'Placed' THEN p.placement_package END), 0) as avg_placement_package,
            ROUND(AVG(p.mock_interview_score), 1) as avg_mock_interview_score,
            ROUND(AVG((ss.communication + ss.teamwork + ss.presentation + 
                      ss.leadership + ss.critical_thinking + ss.interpersonal_skills) / 6.0), 1) as avg_soft_skills_score,
            ROUND(AVG(prog.problems_solved), 1) as avg_problems_solved,
            ROUND(AVG(prog.latest_project_score), 1) as avg_project_score,
            COUNT(DISTINCT p.company_name) as total_hiring_companies
        FROM students s
        JOIN placements p ON s.student_id = p.student_id
        JOIN soft_skills ss ON s.student_id = ss.student_id
        LEFT JOIN programming prog ON s.student_id = prog.student_id
        
        UNION ALL
        
        SELECT 
            'Best Performing Batch' as metric_category,
            NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
            (SELECT s2.course_batch
             FROM students s2
             JOIN placements p2 ON s2.student_id = p2.student_id
             GROUP BY s2.course_batch
             ORDER BY SUM(CASE WHEN p2.placement_status = 'Placed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) DESC
             LIMIT 1) as total_hiring_companies
        
        UNION ALL
        
        SELECT 
            'Top Hiring Company' as metric_category,
            NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
            (SELECT p3.company_name
             FROM placements p3
             WHERE p3.placement_status = 'Placed' AND p3.company_name IS NOT NULL
             GROUP BY p3.company_name
             ORDER BY COUNT(*) DESC
             LIMIT 1) as total_hiring_companies
        """
        return self.db.execute_custom_query(query)
    
    def run_all_queries(self, save_to_files: bool = False) -> dict:
        """
        Run all 10 queries and return results
        
        Args:
            save_to_files (bool): Whether to save results to CSV files
            
        Returns:
            dict: Dictionary containing all query results
        """
        results = {}
        
        print("🚀 Running all 10 SQL queries for placement insights...")
        print("-" * 60)
        
        # Query 1
        print("📊 Query 1: Top Placement Ready Students")
        results['top_students'] = self.query_1_top_placement_ready_students()
        print(f"   Found {len(results['top_students'])} top students")
        
        # Query 2
        print("📊 Query 2: Programming Performance by Batch")
        results['batch_performance'] = self.query_2_programming_performance_by_batch()
        print(f"   Analyzed {len(results['batch_performance'])} batches")
        
        # Query 3
        print("📊 Query 3: Soft Skills Distribution Analysis")
        results['soft_skills_analysis'] = self.query_3_soft_skills_distribution_analysis()
        print(f"   Analyzed soft skills across {len(results['soft_skills_analysis'])} batches")
        
        # Query 4
        print("📊 Query 4: Placement Success by Location")
        results['location_analysis'] = self.query_4_placement_success_by_location()
        print(f"   Analyzed {len(results['location_analysis'])} cities")
        
        # Query 5
        print("📊 Query 5: Company-wise Hiring Analysis")
        results['company_analysis'] = self.query_5_company_wise_hiring_analysis()
        print(f"   Analyzed {len(results['company_analysis'])} companies")
        
        # Query 6
        print("📊 Query 6: Programming Language Impact")
        results['language_impact'] = self.query_6_programming_language_impact_on_placement()
        print(f"   Analyzed {len(results['language_impact'])} programming languages")
        
        # Query 7
        print("📊 Query 7: Internship Impact Analysis")
        results['internship_impact'] = self.query_7_internship_impact_on_placement()
        print(f"   Analyzed internship impact across {len(results['internship_impact'])} experience levels")
        
        # Query 8
        print("📊 Query 8: Students Needing Improvement")
        results['improvement_needed'] = self.query_8_students_needing_improvement()
        print(f"   Identified {len(results['improvement_needed'])} students needing support")
        
        # Query 9
        print("📊 Query 9: Skills Gap Analysis")
        results['skills_gap'] = self.query_9_skills_gap_analysis()
        print(f"   Analyzed skills across {len(results['skills_gap'])} package categories")
        
        # Query 10
        print("📊 Query 10: Overall Program Effectiveness")
        results['program_effectiveness'] = self.query_10_overall_program_effectiveness()
        print(f"   Generated {len(results['program_effectiveness'])} executive metrics")
        
        if save_to_files:
            print("\n💾 Saving results to CSV files...")
            for query_name, df in results.items():
                filename = f"insights_{query_name}.csv"
                df.to_csv(filename, index=False)
                print(f"   Saved: {filename}")
        
        print("\n✅ All queries completed successfully!")
        return results


# Example usage and testing
if __name__ == "__main__":
    # Initialize database manager and insights
    db_manager = DatabaseManager()
    insights = PlacementInsights(db_manager)
    
    if db_manager.test_connection():
        print("🎉 Database connected! Running sample queries...\n")
        
        # Run a few sample queries to test
        print("=" * 60)
        print("SAMPLE QUERY RESULTS")
        print("=" * 60)
        
        # Top 5 students
        top_students = insights.query_1_top_placement_ready_students(5)
        print("\n🏆 TOP 5 PLACEMENT READY STUDENTS:")
        print(top_students[['name', 'course_batch', 'placement_status', 'overall_score']].to_string(index=False))
        
        # Batch performance
        batch_perf = insights.query_2_programming_performance_by_batch()
        print(f"\n📊 PROGRAMMING PERFORMANCE BY BATCH:")
        print(batch_perf[['course_batch', 'total_students', 'avg_problems_solved', 'avg_project_score']].to_string(index=False))
        
        # Company analysis
        company_analysis = insights.query_5_company_wise_hiring_analysis()
        print(f"\n🏢 TOP HIRING COMPANIES:")
        print(company_analysis.head()[['company_name', 'students_hired', 'avg_package']].to_string(index=False))
        
        print("\n" + "=" * 60)
        print("🚀 Ready to run all queries! Use insights.run_all_queries() to get complete analysis")
        
    else:
        print("❌ Database connection failed!")