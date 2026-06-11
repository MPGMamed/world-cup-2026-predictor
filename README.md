# 🏆 2026 FIFA World Cup Predictor

> Machine learning pipeline that predicts match outcomes, group standings, and tournament results for the 2026 FIFA World Cup — deployed as an interactive dashboard with Docker.

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Dash](https://img.shields.io/badge/Dash-2.14-green) ![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED) ![Accuracy](https://img.shields.io/badge/Model%20Accuracy-76.1%25-brightgreen)

---

## 📊 Live Dashboard

Interactive dashboard built with Plotly Dash and deployed via Docker:

- **Group Stage Heatmap** — predicted standings for all 12 groups (A–L)
- **Championship Probability** — Monte Carlo win probabilities for all 48 nations
- **Top Scorers Prediction** — projected goals based on team progression
- **Tournament Bracket** — match-by-match win percentages with stage filter

---

## 🔮 Key Predictions

| | |
|---|---|
| 🏆 **Champion** | France |
| 🥈 **Runner-up** | Brazil |
| 🥉 **3rd Place** | Netherlands |
| ⚽ **Top Scorer** | Kylian Mbappé (7.8 projected goals) |
| 📊 **Model Accuracy** | 76.1% (5-fold cross-validation) |

---

## 🧠 Methodology

### Data Sources
- `wc_all_matches.csv` — 184 historical World Cup matches (1930–2022)
- `wc_2026_fixtures.csv` — all 104 scheduled 2026 matches with FIFA rankings
- `wc_2026_teams.csv` — 48 qualified nations with confederation and FIFA rank
- `wc_all_editions.csv` — tournament-level statistics per year
- `fifa_world_cup_2026_golden_dataset.csv` — player-level stats for 1,176 players

### Feature Engineering
For each historical match, 10 features were engineered:

| Feature | Description |
|---|---|
| `team1_win_rate` | Historical WC win rate |
| `team2_win_rate` | Historical WC win rate |
| `win_rate_diff` | Difference in win rates |
| `team1_gpg / team2_gpg` | Goals scored per game |
| `team1_gapg / team2_gapg` | Goals conceded per game |
| `goal_diff_diff` | Cumulative goal difference gap |
| `rank_diff` | FIFA ranking difference |
| `h2h_t1_win_rate` | Head-to-head historical win rate |

### ML Models Compared (5-Fold Cross-Validation)

| Model | Accuracy |
|---|---|
| **Logistic Regression** | **76.1% ± 3.2%** |
| Random Forest | 69.6% ± 4.1% |
| XGBoost | 66.3% ± 5.8% |

Logistic Regression outperforms tree-based models due to the small dataset size (184 matches). Simpler models generalize better with limited training samples.

### Tournament Simulation
Knockout stage predictions use an **ELO-style rating system**:

```
ELO = 2000 - (FIFA_rank - 1) × 8
Win Probability = 1 / (1 + 10^((ELO2 - ELO1) / 400))
```

- FIFA rank weighted at **80%** of the composite score
- Historical WC win rate adjustment of **±100 ELO points** (only for teams with 3+ matches)
- Head-to-head historical record adds a small **±25 ELO** adjustment
- **1,000 Monte Carlo simulations** run for championship probability estimation

### Top Scorer Projection
```
projected_goals = (goals / appearances) × expected_matches
```
Expected matches based on predicted stage reached (Group Stage = 3, Champion = 8).

---

## 🚀 Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running

### Run the Dashboard
```bash
# Clone the repository
git clone https://github.com/MPGMamed/world-cup-2026-predictor.git
cd world-cup-2026-predictor

# Build and run with Docker
docker compose up --build

# Open in browser
http://localhost:8050
```

### Run Locally (without Docker)
```bash
pip install -r requirements.txt
python app.py
```

---

## 📁 Project Structure

```
world-cup-2026-predictor/
├── notebooks/
│   └── 01_wc2026_predictor.ipynb   ← Full analysis notebook
├── data/
│   ├── raw/                         ← Original Kaggle datasets
│   └── processed/                   ← Cleaned team stats
├── outputs/                         ← Generated CSVs and charts
│   ├── group_standings.csv
│   ├── tournament_bracket.csv
│   ├── win_probability.csv
│   ├── top_scorers_prediction.csv
│   └── *.png                        ← Visualizations
├── app.py                           ← Dash dashboard application
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 📈 Output Files

| File | Description |
|---|---|
| `group_standings.csv` | Predicted points and rank for all 48 teams |
| `group_predictions.csv` | Win/draw/loss % for every group match |
| `tournament_bracket.csv` | Match-by-match KO predictions with win % |
| `win_probability.csv` | Championship probability per team (1000 sims) |
| `top_scorers_prediction.csv` | Projected goals for top 15 players |
| `team_stats.csv` | Historical stats + ELO rating per team |
| `feature_importance.csv` | XGBoost feature importance scores |
| `model_summary.csv` | CV accuracy for all 3 models |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Core language |
| Pandas | Data manipulation |
| Scikit-learn | ML models + cross-validation |
| XGBoost | Gradient boosting + feature importance |
| Plotly / Dash | Interactive dashboard |
| Dash Bootstrap | Dashboard styling |
| Docker | Containerization and deployment |
| Gunicorn | Production WSGI server |

---

## 📊 Key Insights

- **Defensive record beats FIFA rank** as a predictor — `goals_against_per_game` is the 2nd most important feature
- **Historical win rate** is the strongest single feature (0.163 importance score)
- **France dominates** Monte Carlo simulations with 21.4% championship probability — nearly 2× Brazil's 15.9%
- **Group L** is the most imbalanced group (7.58 vs 3.62 expected points gap)
- **Group J and F** are the most competitive ("groups of death")

---

## 📚 Dataset

Data sourced from Kaggle: [FIFA Football World Cup Dataset](https://www.kaggle.com/datasets/iamsouravbanerjee/fifa-football-world-cup-dataset)

---

## 👤 Author

**Mamed Mammadov**
Data Analytics Student — Burgundy School of Business (BSB), Dijon
GitHub: [@MPGMamed](https://github.com/MPGMamed)

---

<<<<<<< HEAD
*Built during the 2026 FIFA World Cup — predictions updated as tournament progresses*
=======
*Built during the 2026 FIFA World Cup — predictions updated as tournament progresses*
>>>>>>> 28a27efdc242c9944856b945e8360d58cfd17fb1
