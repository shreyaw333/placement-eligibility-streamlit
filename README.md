# Placement Eligibility Streamlit Application

A comprehensive data-driven application for filtering and analyzing student placement readiness using interactive dashboards and advanced analytics.

## Project Overview

This application helps placement teams and academic coordinators efficiently identify eligible students for job placements based on customizable criteria including technical skills, soft skills, and placement readiness metrics.

### Key Features

- **Interactive Student Filtering** - Dynamic filtering based on multiple criteria
- **Placement Analytics** - Comprehensive visualizations and insights
- **Performance Tracking** - Student and batch performance analysis
- **Data-Driven Insights** - 10+ analytical queries for strategic decision making
- **Professional Dashboard** - Clean, user-friendly interface

## Technical Stack

- **Frontend:** Streamlit
- **Backend:** Python with OOP design
- **Database:** SQLite
- **Data Generation:** Faker library
- **Visualizations:** Plotly
- **Data Processing:** Pandas

## Project Structure

```
placement-eligibility-streamlit/
│
├── app.py                 # Main Streamlit application
├── database.py            # Database connection and management class
├── sql_queries.py         # SQL queries and insights class
├── data_generator.py      # Synthetic data generation script
│
├── data/
│   └── students.db        # SQLite database file
│
├── docs/
│   ├── README.md          # This file
│   ├── SETUP.md           # Installation and setup guide
│   └── PROJECT_LOG.md     # Development log
│
├── requirements.txt       # Python dependencies
└── .gitignore            # Git ignore file
```

## Database Schema

### Students Table
- `student_id` (Primary Key): Unique identifier
- `name`: Full name of the student
- `age`: Age of the student
- `gender`: Gender (Male, Female, Other)
- `email`: Email address
- `phone`: Contact number
- `enrollment_year`: Year of enrollment
- `course_batch`: Batch identifier
- `city`: City of residence
- `graduation_year`: Expected graduation year

### Programming Table
- `programming_id` (Primary Key): Unique identifier
- `student_id` (Foreign Key): References students table
- `language`: Programming language (Python, SQL, R, Java, JavaScript)
- `problems_solved`: Number of coding problems solved
- `assessments_completed`: Number of assessments completed
- `mini_projects`: Number of mini projects submitted
- `certifications_earned`: Programming certifications earned
- `latest_project_score`: Most recent project score

### Soft Skills Table
- `soft_skill_id` (Primary Key): Unique identifier
- `student_id` (Foreign Key): References students table
- `communication`: Communication skills score (0-100)
- `teamwork`: Teamwork skills score (0-100)
- `presentation`: Presentation skills score (0-100)
- `leadership`: Leadership skills score (0-100)
- `critical_thinking`: Critical thinking score (0-100)
- `interpersonal_skills`: Interpersonal skills score (0-100)

### Placements Table
- `placement_id` (Primary Key): Unique identifier
- `student_id` (Foreign Key): References students table
- `mock_interview_score`: Mock interview performance (0-100)
- `internships_completed`: Number of internships completed
- `placement_status`: Status (Ready, Not Ready, Placed, In Progress)
- `company_name`: Hiring company name
- `placement_package`: Salary package offered
- `interview_rounds_cleared`: Interview rounds cleared
- `placement_date`: Date of placement offer

## Application Features

### 1. Student Eligibility Filter
- **Academic Criteria**: Course batch, city, programming language
- **Technical Skills**: Minimum problems solved, project scores, soft skills
- **Placement Readiness**: Mock interview scores, internships, placement status
- **Results Export**: Download filtered results as CSV

### 2. Placement Analytics
- **Company Analysis**: Hiring patterns and package distributions
- **Location Insights**: Placement rates by city
- **Skills Impact**: Programming language effectiveness
- **Experience Correlation**: Internship impact on placements

### 3. Top Performers
- **Student Rankings**: Top performers with weighted scoring
- **Batch Comparison**: Performance metrics across batches
- **Recognition Lists**: Downloadable performance reports

### 4. Insights Dashboard
- **Executive Metrics**: Key program statistics
- **Improvement Areas**: Students needing support
- **Skills Gap Analysis**: Package level skill comparisons
- **Placement Trends**: Status distribution and patterns

## SQL Insights (10 Analytical Queries)

1. **Top Placement Ready Students** - Weighted performance ranking
2. **Programming Performance by Batch** - Batch effectiveness analysis
3. **Soft Skills Distribution** - Skills development assessment
4. **Placement Success by Location** - Geographic trend analysis
5. **Company Hiring Patterns** - Employer preference insights
6. **Programming Language Impact** - Technology skill effectiveness
7. **Internship Correlation** - Experience impact analysis
8. **Improvement Recommendations** - At-risk student identification
9. **Skills Gap Analysis** - Package-based skill requirements
10. **Program Effectiveness** - Overall performance metrics

## Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd placement-eligibility-streamlit
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Generate sample data** (if needed)
```bash
python data_generator.py
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Open your browser** to `http://localhost:8501`

## Usage Examples

### Finding Eligible Students
1. Navigate to "Student Eligibility Filter"
2. Set criteria (e.g., min problems solved: 50, soft skills: 75)
3. Click "Find Eligible Students"
4. Review results and download CSV if needed

### Analyzing Placement Trends
1. Go to "Placement Analytics"
2. Explore company hiring patterns
3. Review location-based success rates
4. Analyze programming language impact

### Identifying Top Performers
1. Visit "Top Performers" section
2. Review ranked student list
3. Compare batch performance
4. Download recognition reports

## Data Generation

The application uses the Faker library to generate realistic synthetic data:
- **500 students** across 8 course batches
- **963 programming records** across 5 languages
- **Multiple skill assessments** per student
- **Realistic placement outcomes** with proper correlations

## Performance Optimization

- **Streamlit Caching**: Database connections and query results cached
- **Efficient Queries**: Optimized SQL with proper indexing
- **Memory Management**: Context managers for database connections
- **Error Handling**: Comprehensive exception handling throughout

## Business Impact

### For Placement Teams
- **Faster Filtering**: Reduce student screening time by 80%
- **Data-Driven Decisions**: Evidence-based placement strategies
- **Performance Tracking**: Monitor program effectiveness
- **Targeted Support**: Identify students needing intervention

### For Academic Coordinators
- **Batch Analysis**: Compare cohort performance
- **Curriculum Insights**: Skills gap identification
- **Resource Allocation**: Focus improvement efforts
- **Success Metrics**: Track program outcomes

## Technical Highlights

- **Object-Oriented Design**: Clean, maintainable code structure
- **Database Abstraction**: Modular database interaction layer
- **Dynamic Queries**: Flexible filtering with SQL generation
- **Professional UI**: Clean, responsive interface design
- **Comprehensive Logging**: Debug and monitoring capabilities

## Development Standards

- **PEP 8 Compliance**: Python coding standards followed
- **Type Hints**: Enhanced code readability and IDE support
- **Documentation**: Comprehensive docstrings and comments
- **Error Handling**: Robust exception management
- **Testing**: Manual testing procedures documented

## Future Enhancements

- **Authentication**: User role-based access control
- **Real-time Updates**: Live data synchronization
- **Advanced Analytics**: Machine learning predictions
- **API Integration**: External system connectivity
- **Mobile Responsive**: Enhanced mobile experience

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

## License

This project is developed for educational purposes as part of the Data Science curriculum.

## Support

For questions or issues:
- Check the SETUP.md for installation help
- Review the PROJECT_LOG.md for development notes
- Contact the development team for technical support

## Acknowledgments

- **Faker Library**: For realistic data generation
- **Streamlit Team**: For the excellent dashboard framework
- **Plotly**: For interactive visualization capabilities
- **Course Instructors**: For project guidance and requirements

