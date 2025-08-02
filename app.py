"""
Placement Eligibility Streamlit Application
Interactive dashboard for filtering and analyzing student placement readiness
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import our custom classes
from database import DatabaseManager
from sql_queries import PlacementInsights

# Page configuration
st.set_page_config(
    page_title="Placement Eligibility Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
    }
    .filter-section {
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .insight-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 3px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_database_manager():
    """Load and cache database manager"""
    return DatabaseManager()

@st.cache_data
def load_placement_insights():
    """Load and cache placement insights"""
    db_manager = load_database_manager()
    return PlacementInsights(db_manager)

@st.cache_data
def get_filter_options():
    """Get and cache filter options"""
    db_manager = load_database_manager()
    return db_manager.get_filter_options()

@st.cache_data
def get_database_summary():
    """Get and cache database summary"""
    db_manager = load_database_manager()
    return db_manager.get_database_summary()

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">Placement Eligibility Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("**Filter students based on eligibility criteria and explore placement insights**")
    
    # Initialize components
    try:
        db_manager = load_database_manager()
        insights = load_placement_insights()
        
        # Test database connection
        if not db_manager.test_connection():
            st.error("Database connection failed. Please check your database file.")
            return
            
    except Exception as e:
        st.error(f"Error initializing application: {e}")
        return
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Select Page",
        ["Student Eligibility Filter", "Placement Analytics", "Top Performers", "Insights Dashboard"]
    )
    
    if page == "Student Eligibility Filter":
        show_eligibility_filter(db_manager)
    elif page == "Placement Analytics":
        show_placement_analytics(insights)
    elif page == "Top Performers":
        show_top_performers(insights)
    elif page == "Insights Dashboard":
        show_insights_dashboard(insights)

def show_eligibility_filter(db_manager):
    """Show the main eligibility filtering interface"""
    
    st.header("Student Eligibility Filter")
    st.markdown("Set your criteria to find eligible students for placement opportunities.")
    
    # Get filter options
    filter_options = get_filter_options()
    
    # Filter controls in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.subheader("Academic Criteria")
        
        course_batch = st.selectbox(
            "Course Batch",
            ["All"] + filter_options.get('course_batches', []),
            help="Select specific batch or 'All' for all batches"
        )
        
        city = st.selectbox(
            "City",
            ["All"] + filter_options.get('cities', []),
            help="Filter by student location"
        )
        
        programming_language = st.selectbox(
            "Programming Language",
            ["All"] + filter_options.get('programming_languages', []),
            help="Students who have experience in this language"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.subheader("Technical Skills")
        
        min_problems_solved = st.slider(
            "Minimum Problems Solved",
            min_value=0, max_value=150, value=30,
            help="Minimum coding problems solved"
        )
        
        min_project_score = st.slider(
            "Minimum Project Score",
            min_value=0, max_value=100, value=60,
            help="Minimum score in latest project"
        )
        
        min_soft_skills = st.slider(
            "Minimum Soft Skills Average",
            min_value=0, max_value=100, value=60,
            help="Average of all soft skills scores"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        st.subheader("Placement Readiness")
        
        min_mock_interview = st.slider(
            "Minimum Mock Interview Score",
            min_value=0, max_value=100, value=50,
            help="Minimum mock interview performance"
        )
        
        min_internships = st.selectbox(
            "Minimum Internships",
            [0, 1, 2, 3, 4],
            index=1,
            help="Minimum internships completed"
        )
        
        placement_status = st.multiselect(
            "Placement Status",
            filter_options.get('placement_statuses', []),
            default=['Ready', 'Placed'],
            help="Include students with these statuses"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Build criteria dictionary
    criteria = {}
    
    if min_problems_solved > 0:
        criteria['min_problems_solved'] = min_problems_solved
    if min_project_score > 0:
        criteria['min_project_score'] = min_project_score
    if min_soft_skills > 0:
        criteria['min_soft_skills_avg'] = min_soft_skills
    if min_mock_interview > 0:
        criteria['min_mock_interview'] = min_mock_interview
    if min_internships > 0:
        criteria['min_internships'] = min_internships
    if placement_status:
        criteria['placement_status'] = placement_status
    if course_batch != "All":
        criteria['course_batch'] = course_batch
    if city != "All":
        criteria['city'] = city
    if programming_language != "All":
        criteria['programming_language'] = programming_language
    
    # Search button
    if st.button("Find Eligible Students", type="primary", use_container_width=True):
        with st.spinner("Searching for eligible students..."):
            eligible_students = db_manager.get_eligible_students(criteria)
            
            if len(eligible_students) > 0:
                st.success(f"Found {len(eligible_students)} eligible students!")
                
                # Display results
                st.subheader("Eligible Students")
                
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    placed_count = len(eligible_students[eligible_students['placement_status'] == 'Placed'])
                    st.metric("Already Placed", placed_count)
                
                with col2:
                    ready_count = len(eligible_students[eligible_students['placement_status'] == 'Ready'])
                    st.metric("Ready for Placement", ready_count)
                
                with col3:
                    avg_soft_skills = eligible_students['avg_soft_skills'].mean()
                    st.metric("Avg Soft Skills", f"{avg_soft_skills:.1f}")
                
                with col4:
                    avg_problems = eligible_students['max_problems_solved'].mean()
                    st.metric("Avg Problems Solved", f"{avg_problems:.0f}")
                
                # Detailed results table
                st.dataframe(
                    eligible_students[[
                        'name', 'course_batch', 'city', 'placement_status',
                        'mock_interview_score', 'avg_soft_skills', 'max_problems_solved',
                        'programming_languages', 'company_name', 'placement_package'
                    ]],
                    use_container_width=True,
                    height=400
                )
                
                # Download button
                csv = eligible_students.to_csv(index=False)
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name=f"eligible_students_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
            else:
                st.warning("No students found matching the specified criteria. Try adjusting your filters.")

def show_placement_analytics(insights):
    """Show placement analytics and visualizations"""
    
    st.header("Placement Analytics")
    st.markdown("Comprehensive analysis of placement trends and patterns.")
    
    # Get analytics data
    with st.spinner("Loading analytics data..."):
        try:
            # Company analysis
            company_data = insights.query_5_company_wise_hiring_analysis()
            location_data = insights.query_4_placement_success_by_location()
            language_data = insights.query_6_programming_language_impact_on_placement()
            internship_data = insights.query_7_internship_impact_on_placement()
            
        except Exception as e:
            st.error(f"Error loading analytics: {e}")
            return
    
    # Company hiring analysis
    st.subheader("Company Hiring Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        if not company_data.empty:
            fig_companies = px.bar(
                company_data.head(10),
                x='students_hired',
                y='company_name',
                orientation='h',
                title="Top 10 Hiring Companies",
                labels={'students_hired': 'Students Hired', 'company_name': 'Company'},
                color='avg_package',
                color_continuous_scale='blues'
            )
            fig_companies.update_layout(height=500)
            st.plotly_chart(fig_companies, use_container_width=True)
    
    with col2:
        if not company_data.empty:
            fig_packages = px.scatter(
                company_data,
                x='students_hired',
                y='avg_package',
                size='avg_interview_score_of_hired',
                hover_data=['company_name'],
                title="Company Package vs Hiring Volume",
                labels={'students_hired': 'Students Hired', 'avg_package': 'Average Package (₹)'}
            )
            fig_packages.update_layout(height=500)
            st.plotly_chart(fig_packages, use_container_width=True)
    
    # Location analysis
    st.subheader("Location-wise Placement Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        if not location_data.empty:
            fig_location = px.bar(
                location_data.head(10),
                x='city',
                y='placement_rate_percent',
                title="Placement Rate by City",
                labels={'placement_rate_percent': 'Placement Rate (%)', 'city': 'City'},
                color='avg_package',
                color_continuous_scale='greens'
            )
            fig_location.update_xaxes(tickangle=45)
            st.plotly_chart(fig_location, use_container_width=True)
    
    with col2:
        if not location_data.empty:
            fig_students = px.scatter(
                location_data,
                x='total_students',
                y='placement_rate_percent',
                size='avg_package',
                hover_data=['city'],
                title="Students vs Placement Rate by City",
                labels={'total_students': 'Total Students', 'placement_rate_percent': 'Placement Rate (%)'}
            )
            st.plotly_chart(fig_students, use_container_width=True)
    
    # Programming language impact
    st.subheader("Programming Language Impact")
    if not language_data.empty:
        fig_lang = px.bar(
            language_data,
            x='language',
            y='placement_rate_percent',
            title="Placement Rate by Programming Language",
            labels={'placement_rate_percent': 'Placement Rate (%)', 'language': 'Programming Language'},
            color='avg_package_for_placed',
            color_continuous_scale='viridis'
        )
        st.plotly_chart(fig_lang, use_container_width=True)
    
    # Internship impact
    st.subheader("Internship Impact on Placement")
    if not internship_data.empty:
        fig_internship = px.line(
            internship_data,
            x='internships_completed',
            y='placement_rate_percent',
            markers=True,
            title="Placement Rate vs Internships Completed",
            labels={'internships_completed': 'Internships Completed', 'placement_rate_percent': 'Placement Rate (%)'}
        )
        st.plotly_chart(fig_internship, use_container_width=True)

def show_top_performers(insights):
    """Show top performing students and batches"""
    
    st.header("Top Performers")
    st.markdown("Recognition for high-achieving students and best-performing batches.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Students")
        try:
            with st.spinner("Loading top students..."):
                top_students = insights.query_1_top_placement_ready_students(20)
            
            if not top_students.empty:
                st.success(f"Found {len(top_students)} top performing students")
                
                # Display top students
                for idx, student in top_students.head(10).iterrows():
                    with st.container():
                        st.markdown(f"""
                        <div class="insight-box">
                            <h4>#{idx+1} {student['name']}</h4>
                            <p><strong>Batch:</strong> {student['course_batch']} | <strong>City:</strong> {student['city']}</p>
                            <p><strong>Overall Score:</strong> {student['overall_score']}/100 | <strong>Status:</strong> {student['placement_status']}</p>
                            <p><strong>Skills:</strong> Mock Interview: {student['mock_interview_score']}, Soft Skills: {student['avg_soft_skills']}, Problems Solved: {student['max_problems_solved']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Download top students
                csv = top_students.to_csv(index=False)
                st.download_button(
                    label="Download Top Students List",
                    data=csv,
                    file_name=f"top_students_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No top students data found. Check database connection.")
                st.info("Debug: Attempting to show raw query result...")
                st.write("Query result shape:", top_students.shape if 'top_students' in locals() else "No data")
        
        except Exception as e:
            st.error(f"Error loading top students: {str(e)}")
            st.info("Please check the console for detailed error information.")
    
    with col2:
        st.subheader("Batch Performance")
        try:
            with st.spinner("Loading batch performance..."):
                batch_performance = insights.query_2_programming_performance_by_batch()
            
            if not batch_performance.empty:
                st.success(f"Analyzing {len(batch_performance)} batches")
                
                # Batch ranking
                batch_performance = batch_performance.sort_values('avg_problems_solved', ascending=False)
                
                for idx, batch in batch_performance.iterrows():
                    rank = batch_performance.index.get_loc(idx) + 1
                    st.markdown(f"""
                    <div class="insight-box">
                        <h4>#{rank} {batch['course_batch']}</h4>
                        <p><strong>Students:</strong> {batch['total_students']} | <strong>Programming Records:</strong> {batch['total_programming_records']}</p>
                        <p><strong>Avg Problems Solved:</strong> {batch['avg_problems_solved']} | <strong>Avg Project Score:</strong> {batch['avg_project_score']}</p>
                        <p><strong>Range:</strong> {batch['min_problems_solved']} - {batch['max_problems_solved']} problems</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No batch performance data found. Check database connection.")
                st.info("Debug: Attempting to show raw query result...")
                st.write("Query result shape:", batch_performance.shape if 'batch_performance' in locals() else "No data")
        
        except Exception as e:
            st.error(f"Error loading batch performance: {str(e)}")
            st.info("Please check the console for detailed error information.")

def show_insights_dashboard(insights):
    """Show comprehensive insights dashboard"""
    
    st.header("Insights Dashboard")
    st.markdown("Executive summary and actionable insights for program improvement.")
    
    # Database summary
    db_summary = get_database_summary()
    
    # Key metrics
    st.subheader("Key Program Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", db_summary.get('total_students', 0))
    
    with col2:
        placed = db_summary.get('placement_distribution', {}).get('Placed', 0)
        total = db_summary.get('total_students', 1)
        placement_rate = (placed / total) * 100 if total > 0 else 0
        st.metric("Placement Rate", f"{placement_rate:.1f}%")
    
    with col3:
        st.metric("Avg Problems Solved", db_summary.get('avg_problems_solved', 0))
    
    with col4:
        st.metric("Programming Records", db_summary.get('programming_records', 0))
    
    # Placement status distribution
    st.subheader("Placement Status Distribution")
    if 'placement_distribution' in db_summary:
        placement_dist = db_summary['placement_distribution']
        
        # Create pie chart
        fig_pie = px.pie(
            values=list(placement_dist.values()),
            names=list(placement_dist.keys()),
            title="Student Placement Status Distribution"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Students needing improvement
    st.subheader("Students Needing Support")
    try:
        improvement_data = insights.query_8_students_needing_improvement()
        
        if not improvement_data.empty:
            # Group by improvement area
            improvement_summary = improvement_data['primary_improvement_area'].value_counts()
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_improvement = px.bar(
                    x=improvement_summary.index,
                    y=improvement_summary.values,
                    title="Students by Improvement Area Needed",
                    labels={'x': 'Improvement Area', 'y': 'Number of Students'}
                )
                st.plotly_chart(fig_improvement, use_container_width=True)
            
            with col2:
                st.markdown("**Detailed Breakdown:**")
                for area, count in improvement_summary.items():
                    st.markdown(f"- **{area}:** {count} students")
                
                # Show some students needing help
                st.markdown("**Students Needing Interview Support:**")
                interview_help = improvement_data[improvement_data['primary_improvement_area'] == 'Interview Skills'].head(5)
                for _, student in interview_help.iterrows():
                    st.markdown(f"- {student['name']} ({student['course_batch']}) - Score: {student['mock_interview_score']}")
    
    except Exception as e:
        st.error(f"Error loading improvement data: {e}")
    
    # Skills gap analysis
    st.subheader("Skills Gap Analysis by Package Level")
    try:
        skills_gap = insights.query_9_skills_gap_analysis()
        
        if not skills_gap.empty:
            # Skills comparison chart
            skills_cols = ['avg_communication', 'avg_teamwork', 'avg_presentation', 'avg_leadership', 'avg_critical_thinking']
            
            fig_skills = go.Figure()
            
            for _, row in skills_gap.iterrows():
                fig_skills.add_trace(go.Scatterpolar(
                    r=[row[col] for col in skills_cols],
                    theta=['Communication', 'Teamwork', 'Presentation', 'Leadership', 'Critical Thinking'],
                    fill='toself',
                    name=row['package_category']
                ))
            
            fig_skills.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                title="Skills Profile by Package Category"
            )
            
            st.plotly_chart(fig_skills, use_container_width=True)
            
            # Skills gap table
            st.dataframe(skills_gap, use_container_width=True)
    
    except Exception as e:
        st.error(f"Error loading skills gap analysis: {e}")

if __name__ == "__main__":
    main()