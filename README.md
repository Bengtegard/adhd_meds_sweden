# ADHD Medications Sweden - Dash App

## Prerequisites

- Python 3.8 or higher (Python 3.12 recommended)
- pip (Python package manager)

## Setup

Follow these steps to set up and run the project locally:

### 1. Clone the repository
```bash
git clone https://github.com/bengtegard/adhd_meds_sweden
cd adhd_meds_sweden
```

### 2. Create a virtual environment (recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Dash app
```bash
python dash_app.py
```

### 5. Access the application
Open your web browser and navigate to:
```
http://127.0.0.1:8050
```

## Project Structure
```
adhd_meds_sweden/
├── dash_app.py          # Main Dash application
├── config.py            # Configuration (colors, county mappings)
├── requirements.txt     # Python dependencies
└── data/               # Data files (if applicable)
```

## Deactivating the virtual environment
When you're done, deactivate the virtual environment:
```bash
deactivate
```
