# Setup and Installation Guide

This guide provides step-by-step instructions for setting up the Placement Eligibility Streamlit Application on your local machine.

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB free space
- **OS**: Windows 10, macOS 10.14, or Linux Ubuntu 18.04+

### Recommended Requirements
- **Python**: 3.9 or 3.10
- **RAM**: 8GB or more
- **Storage**: 1GB free space
- **Internet**: For initial package downloads

## Pre-Installation Checklist

1. **Verify Python Installation**
```bash
python --version
# or
python3 --version
```
Should return Python 3.8+

2. **Verify pip Installation**
```bash
pip --version
# or
pip3 --version
```

3. **Check Git (Optional)**
```bash
git --version
```

## Installation Methods

### Method 1: Direct Download (Recommended for Beginners)

1. **Download Project Files**
   - Download all project files to a folder
   - Ensure you have: `app.py`, `database.py`, `sql_queries.py`, `data_generator.py`

2. **Create Project Directory**
```bash
mkdir placement-eligibility-streamlit
cd placement-eligibility-streamlit
```

3. **Copy Files**
   - Copy all downloaded files to this directory

### Method 2: Git Clone (Recommended for Developers)

1. **Clone Repository**
```bash
git clone <repository-url>
cd placement-eligibility-streamlit
```

## Environment Setup

### Option A: Using Virtual Environment (Recommended)

1. **Create Virtual Environment**
```bash
# Windows
python -m venv placement_env

# macOS/Linux
python3 -m venv placement_env
```

2. **Activate Virtual Environment**
```bash
# Windows
placement_env\Scripts\activate

# macOS/Linux
source placement_env/bin/activate
```

3. **Verify Activation**
   - Your command prompt should show `(placement_env)` prefix

### Option B: Using Conda

1. **Create Conda Environment**
```bash
conda create -n placement_env python=3.9
conda activate placement_env
```

## Dependencies Installation

### Method 1: Using requirements.txt (Recommended)

1. **Install All Dependencies**
```bash
pip install -r requirements.txt
```

### Method 2: Manual Installation

1. **Install Core Dependencies**
```bash
pip install streamlit pandas plotly sqlite3
```

2. **Install Data Generation Dependencies**
```bash
pip install faker
```

3. **Verify Installation**
```bash
pip list
```

## Database Setup

### Option 1: Generate New Data (Recommended)

1. **Run Data Generator**
```bash
python data_generator.py
```

2. **Verify Database Creation**
   - Check for `data/students.db` file
   - Should see success messages in console

### Option 2: Use Existing Database

1. **Place Database File**
   - Ensure `students.db` is in the `data/` directory
   - Create `data/` folder if it doesn't exist

## Configuration

### Database Path Configuration

1. **Default Configuration**
   - Database path: `data/students.db`
   - No changes needed for standard setup

2. **Custom Database Path**
   - Edit `database.py` if needed
   - Update `db_path` parameter in `DatabaseManager` class

### Streamlit Configuration (Optional)

1. **Create Streamlit Config**
```bash
mkdir .streamlit
```

2. **Create config.toml**
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = false
```

## Testing Installation

### 1. Test Database Connection

```bash
python -c "from database import DatabaseManager; db = DatabaseManager(); print('Database OK' if db.test_connection() else 'Database Error')"
```

### 2. Test SQL Queries

```bash
python sql_queries.py
```

### 3. Test Streamlit Application

```bash
streamlit run app.py
```

## Running the Application

### 1. Start the Application

```bash
streamlit run app.py
```

### 2. Access the Application

1. **Open Browser**
   - Navigate to: `http://localhost:8501`
   - Application should load automatically

2. **Test Functionality**
   - Try the "Student Eligibility Filter" page
   - Verify data loads correctly
   - Test filtering functionality

### 3. Expected Startup Output

```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.XXX:8501
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Python Not Found
**Error**: `python: command not found`
**Solution**: 
- Windows: Add Python to PATH
- macOS: Install Python via Homebrew
- Linux: `sudo apt-get install python3`

#### 2. Permission Denied
**Error**: `Permission denied` during installation
**Solution**:
```bash
# Use --user flag
pip install --user -r requirements.txt
```

#### 3. Port Already in Use
**Error**: `Port 8501 is already in use`
**Solution**:
```bash
# Use different port
streamlit run app.py --server.port 8502
```

#### 4. Database File Not Found
**Error**: `No such file or directory: 'data/students.db'`
**Solution**:
```bash
# Create data directory and run generator
mkdir data
python data_generator.py
```

#### 5. Module Import Errors
**Error**: `ModuleNotFoundError: No module named 'streamlit'`
**Solution**:
```bash
# Ensure virtual environment is activated
# Reinstall requirements
pip install -r requirements.txt
```

#### 6. Streamlit Not Starting
**Error**: Streamlit hangs on startup
**Solution**:
```bash
# Clear Streamlit cache
streamlit cache clear
# Update Streamlit
pip install --upgrade streamlit
```

### Platform-Specific Issues

#### Windows Issues

1. **PowerShell Execution Policy**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

2. **Long Path Names**
   - Use shorter directory names
   - Move project closer to C:\ drive

#### macOS Issues

1. **Command Line Tools**
```bash
xcode-select --install
```

2. **Homebrew Python**
```bash
brew install python
```

#### Linux Issues

1. **Missing System Dependencies**
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv
```

## Performance Optimization

### 1. Memory Usage

1. **Monitor Memory**
   - Use Task Manager/Activity Monitor
   - Close unnecessary applications

2. **Streamlit Optimization**
```python
# In app.py, adjust caching
@st.cache_data(ttl=3600)  # Cache for 1 hour
```

### 2. Database Performance

1. **Database Location**
   - Keep database on SSD if possible
   - Ensure sufficient disk space

2. **Query Optimization**
   - Queries are pre-optimized
   - No changes needed for standard use

## Development Setup

### 1. Development Dependencies

```bash
# Install additional dev tools
pip install black flake8 pytest
```

### 2. Code Formatting

```bash
# Format code
black *.py

# Check style
flake8 *.py
```

### 3. Testing

```bash
# Run tests (if available)
pytest tests/
```

## Deployment Options

### 1. Local Network Access

```bash
streamlit run app.py --server.address 0.0.0.0
```

### 2. Streamlit Cloud (Free)

1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy automatically

### 3. Docker Deployment

```dockerfile
# Example Dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## Maintenance

### 1. Regular Updates

```bash
# Update dependencies
pip install --upgrade -r requirements.txt
```

### 2. Database Backup

```bash
# Backup database
cp data/students.db data/students_backup.db
```

### 3. Clear Cache

```bash
# Clear Streamlit cache
streamlit cache clear
```

## Getting Help

### 1. Check Logs
- Look at terminal output for error messages
- Check Streamlit logs for debugging

### 2. Documentation
- Review README.md for feature explanations
- Check code comments for technical details

### 3. Common Commands Reference

```bash
# Start application
streamlit run app.py

# Generate new data
python data_generator.py

# Test database
python database.py

# Run SQL queries
python sql_queries.py

# Clear cache
streamlit cache clear

# Update packages
pip install --upgrade -r requirements.txt
```

## Next Steps

After successful installation:

1. **Explore the Application**
   - Try different filter combinations
   - Review the analytics dashboards
   - Test the download functionality

2. **Customize Data**
   - Modify `data_generator.py` for different data
   - Adjust student count or criteria

3. **Extend Functionality**
   - Add new SQL queries
   - Create additional visualizations
   - Implement new filter options

