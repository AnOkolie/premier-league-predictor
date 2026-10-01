# Premier League Predictor

A machine learning project that uses historical Premier League data to analyze player and team performance and predict future trends.

## Overview

This project explores historical Premier League football data using machine learning and data analysis techniques. The goal is to use past performance and player statistics to identify patterns and generate predictions about future Premier League trends.

The project is divided into two main components:

* **Backend** – Handles the data processing and machine learning functionality.
* **Frontend** – Provides an interface for interacting with the predictions and results.

## Dataset

The data used in this project comes from the [Football Data from Transfermarkt dataset](https://www.kaggle.com/datasets/davidcariboo/player-scores) on Kaggle.

The dataset contains multiple CSV files covering football matches, clubs, players, player appearances, player valuations, transfers, and other statistics. The `appearances.csv` file contains one record for each player appearance in a game and includes information such as goals, assists, minutes played, and cards.

### Dataset Files

The project uses CSV files from the Kaggle dataset, including data related to:

* Players
* Clubs
* Competitions
* Games
* Player appearances
* Player valuations
* Game events
* Club games
* Transfers

The original dataset is maintained from Transfermarkt data and contains data from a large number of competitions, clubs, players, and matches.

## Getting the Dataset

Most of the required CSV files are included in this repository.

However, **`appearances.csv` is not included** because of its file size. The file is significantly larger than the GitHub file-size limit, so it has been intentionally left out of the repository.

You can download the original `appearances.csv` file from the Kaggle dataset:

**[Download appearances.csv from Kaggle](https://www.kaggle.com/datasets/davidcariboo/player-scores?resource=download&select=appearances.csv)**

### Option 1: Download from Kaggle

1. Visit the [Football Data from Transfermarkt Kaggle dataset](https://www.kaggle.com/datasets/davidcariboo/player-scores).
2. Download the dataset.
3. Extract the downloaded archive.
4. Locate `appearances.csv`.
5. Place `appearances.csv` in the project's data directory alongside the other CSV files.

Your project structure should look approximately like:

```text
premier-league-predictor/
├── backend/
├── frontend/
├── data/
│   ├── appearances.csv
│   ├── player_valuations.csv
│   ├── players.csv
│   └── ...
└── README.md
```

### Option 2: Download Using the Kaggle API

If you have the Kaggle CLI installed and authenticated, you can download the dataset with:

```bash
kaggle datasets download -d davidcariboo/player-scores
```

Then extract the archive:

```bash
unzip player-scores.zip
```

After extraction, move `appearances.csv` into the appropriate `data/` directory.

## Technologies

* Python
* Machine Learning
* Pandas
* NumPy
* Scikit-learn
* React
* TypeScript
* Data Analysis

## Project Structure

```text
premier-league-predictor/
├── backend/        # Data processing and machine learning
├── frontend/       # Frontend application
├── data/           # Dataset files
└── README.md
```

## Data Source

The underlying dataset is **Football Data from Transfermarkt**, published by David Cariboo on Kaggle.

> Dataset: https://www.kaggle.com/datasets/davidcariboo/player-scores

The dataset provides structured football data including games, clubs, players, appearances, player valuations, transfers, and other football statistics.

Please refer to the original dataset for its licensing and attribution requirements.

## Purpose

This project was built as a machine learning and data-analysis project to explore how historical football data can be used to identify trends and make predictions.

The project is intended for educational and analytical purposes.
