# The Rise of ADHD Medication in Sweden

This interactive dashboard, built with Dash and Plotly Express, analyzes ADHD medication consumption trends in Sweden from 2006 to 2024. Unlike static reports, this dashboard lets you actively explore the data — filter by demographics, hover for details, and animate trends over time. Key insights are highlighted, but the real value comes from exploring the data yourself. The application is hosted on DigitalOcean.

**The live dashboard can be found here:** [https://bengtegard.com/](https://bengtegard.com/)

## Data Source

Data sourced from Socialstyrelsen's [Statistikdatabas för läkemedel](https://sdb.socialstyrelsen.se/if_lak/val.aspx).

Individual medication data (by ATC codes) were extracted via Socialstyrelsen's official API using my custom Python module: [**socialstyrelsen-api**](https://github.com/bengtegard/swedish-adhd-medication-data) (MIT License).

## Previews

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
## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.
