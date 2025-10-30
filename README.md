# The Rise of ADHD Medication in Sweden

An interactive Dash application analyzing ADHD medication consumption trends in Sweden from 2006 to 2024, using open data from Socialstyrelsen.

Unlike static reports, this dashboard lets you actively explore the data — filter by demographics, hover for details, and animate trends over time.

**The live dashboard can be found here:** [https://bengtegard.com/](https://bengtegard.com/)
## Dashboard views

<img src="https://github.com/user-attachments/assets/6474f625-b7cf-4258-a4f5-fdf18af3f3bb" width="800" alt="National Dashboard" />
<img src="https://github.com/user-attachments/assets/e8cd05d5-fa06-4b58-9680-2a8abbd4d76b" width="800" alt="County View" />


## Prerequisites

- Python 3.12 or higher

## Setup

Follow these steps to set up and run the project locally:

### 1. Clone the repository
```bash
git clone https://github.com/bengtegard/adhd_meds_sweden
cd adhd_meds_sweden
```

### 2. Create a virtual environment
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

