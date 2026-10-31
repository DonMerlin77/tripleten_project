# Used Car Price Explorer

A Streamlit web app for exploring US used-car listings (`vehicles_us.csv`): how prices are distributed and how they relate to
condition, drivetrain and mileage. Built for TripleTen's Sprint 4 (software development tools).

**Live app:** https://tripleten-project-sprint-4.onrender.com (free hosting; the first load can take up to a minute
while the server wakes up)

## What it shows
- **Price distribution:** how many cars are listed at each price, with a toggle to color the bars by count.
- **Condition:** the number of cars in each listed condition.
- **Four-wheel drive:** price histograms for 4wd, not 4wd, or both overlaid (two toggles).
- **Odometer:** two charts side by side, the number of cars and the total listed price per odometer reading.

The exploratory analysis behind the app is in `Notebooks/EDA.ipynb`.

## Run it locally
```
pip install -r requirements.txt
streamlit run app.py
```
Then open http://localhost:10000 (the port is set in `.streamlit/config.toml`).

## Stack
Python, pandas, Plotly, Streamlit; deployed on Render.
