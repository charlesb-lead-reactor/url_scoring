# SEO Content Scoring Application

This Streamlit application provides a tool for scoring SEO content based on various metrics such as search volume, position, CPC (Cost Per Click), and content freshness.

## Features

- Calculate SEO scores using two different methods
- Adjust weights for different scoring factors
- Use test data or upload your own CSV file
- Visualize results with interactive charts
- Download results as a CSV file

## Installation

To run this application, you need Python 3.6+ installed on your system. Follow these steps to set up the environment:

1. Clone this repository:
   ```
   git clone https://github.com/charlesb-lead-reactor/url_scoring.git
   cd url_scoring
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, use the following command:

```
streamlit run app.py
```

Then, open your web browser and go to `http://localhost:8501`.

### Using the Application

1. Adjust the weights for different scoring factors in the sidebar.
2. Choose between using test data or uploading your own CSV file.
3. If uploading a file, ensure it has the following columns:
   - url
   - keyword
   - volume
   - position
   - cpc
   - last_update_date
4. View the results in the main panel, including a sortable table and bar chart.
5. Download the results as a CSV file using the provided button.

## Data Format

If you're uploading your own CSV file, it should have the following structure:

```
url,mot_cle,volume,position,cpc,date_maj
https://example.com/page1,keyword1,1000,5,2.50,2023-01-15
https://example.com/page2,keyword2,500,10,1.75,2023-02-20
...
```

## More Information
For more information, visit [Lead-Reactor](https://lead-reactor.io)
