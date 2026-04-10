# 🏆 The Price of Victory - Does Financial Power drive Success in European Football?

This project analyses a decade of financial and performance data, between 2014-2024, across Europe's top 5 leagues - the Premier League, La Liga, Serie A, Bundesliga, and Ligue 1, to understand how Squad Value and Transfer Spending relate to performance outcomes.

Rather than relying on simple correlations, this analysis reveals which clubs outperform their financial means, which ones fail despite heavy investment, and how the connection between money and success shifts across different footballing environments.

## 🎯 Project Objective

To analyse the relationship between Financial Investment and Sporting Success in European football

Financial Metrics:

- Squad Market Value 
- Transfer Spend

Performance Metrics:
 
- Match Points 
- League Position
- Wins
- Clean sheets
- Relegation
- Top 4 Qualification
- Goal Difference 

## ⭐ Key Insights

- 🇬🇧 Premier League spends 3× more than Bundesliga on average

- 📉 Squad value predicts points better than transfer spend

- ⚡ 30% of titles were won by the single highest spender

- 🦁 Leicester City and Monaco emerged as standout overperformers

- 💸 Chelsea 2022/23 recorded the worst ROI - €574M spent and finished 12th in the league

- 🏦 State-backed clubs initially overperform, then plateau over time

## 🚀 Recommendations

- Teams should focus on efficient squad building, not just higher spending

- Promoting youth players can improve performance at lower financial cost

- Invest in other avenues like scouting and nurturing  talent early, management, strategy, and player development

- Be mindful of diminishing returns at very high spending levels

## ⚠️ Limitations

This analysis has the following constraints:

- Transfer spending reflects confirmed fees only - a standard approach in football analytics, as clubs are not obligated to disclose fees. 
- Undisclosed records (~33% of transfers) are excluded

The above limitation was further analysed and the findings are as follows:

- Leagues: Ligue 1 (French league) is the most biased at 21.9%. Serie A and Premier League are the most reliable.

- Clubs: The top 14 most affected clubs are almost entirely Ligue 1 and La Liga - Smaller clubs like Le Havre (43.9%), Guingamp (42.9%), Athletic Bilbao (40%). These clubs' spending is most understated. Notably these are mid/lower table clubs, not big spenders, so the bias likely doesn't distort headline spending comparisons significantly.

- Years: 2020 stands out at 14.7%. The COVID caused this, but otherwise stable at 11–15%.

- Players: No player exceeds 3 undisclosed fees. The missing data is spread thin across many players, not concentrated on superstars. There's no single high-profile player skewing the numbers systematically.

## 📁 Repository Structure

```text
football-finance-analysis/
│
├── data/                     # Raw and cleaned datasets used for analysis
│
├── notebooks/                # Jupyter notebooks for cleaning + EDA 
│
│── app/                      # Multi-page Streamlit application for exploring the analysis and findings
│
│── assets                    # Contains static visual assets for the app
│
└── README.md                 # Project documentation
```

## 🛠️ Data Overview

- The dataset was gathered using Kaggle, which has data scraped from Transfermarkt and football-data.co.uk

## 🔗 Link to the detailed presentation

[Click here to view the presentation with detailed analysis, insights and business applications](https://canva.link/q9h5z97x4zk6yej)