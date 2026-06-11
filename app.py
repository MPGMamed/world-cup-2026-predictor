import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# ── Load data ──────────────────────────────────────────────────────────────────
standings   = pd.read_csv("outputs/group_standings.csv")
win_prob    = pd.read_csv("outputs/win_probability.csv")
scorers     = pd.read_csv("outputs/top_scorers_prediction.csv")
bracket     = pd.read_csv("outputs/tournament_bracket.csv")
team_stats  = pd.read_csv("outputs/team_stats.csv")
predictions = pd.read_csv("outputs/group_predictions.csv")
# Fix encoding
scorers['name'] = scorers['name'].str.replace('?', 'é', regex=False)
standings['advances'] = standings['advances'].astype(bool)

# ── App setup ──────────────────────────────────────────────────────────────────
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "2026 FIFA World Cup Predictor"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = "#1a6b3c"
GREEN_MID   = "#2d8653"
GREEN_LIGHT = "#90d9ae"
GOLD        = "#f5c518"
BG          = "#1a1a2e"
CARD_BG     = "#16213e"
TEXT        = "#e0e0e0"

# ── Charts ─────────────────────────────────────────────────────────────────────

def make_group_heatmap():
    pivot = standings.pivot(index='rank', columns='group', values='predicted_points')
    teams_pivot = standings.pivot(index='rank', columns='group', values='team')
    adv_pivot   = standings.pivot(index='rank', columns='group', values='advances')

    text_matrix = []
    for r in pivot.index:
        row = []
        for g in pivot.columns:
            team = teams_pivot.loc[r, g]
            pts  = pivot.loc[r, g]
            adv  = adv_pivot.loc[r, g]
            mark = "✓" if adv else ""
            row.append(f"<b>{team}</b><br>{pts:.1f} pts {mark}")
        text_matrix.append(row)

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=list(pivot.columns),
        y=[f"Rank {r}" for r in pivot.index],
        text=text_matrix,
        texttemplate="%{text}",
        textfont=dict(size=11, color="white"),
        colorscale=[[0, "#0d3b1f"], [0.4, GREEN_DARK], [0.7, GREEN_MID], [1, GOLD]],
        showscale=True,
        colorbar=dict(title="Pts", tickfont=dict(color=TEXT)),
        hovertemplate="Group %{x} · Rank %{y}<br>%{text}<extra></extra>"
    ))
    fig.update_layout(
        title=dict(text="Group Stage Predicted Standings", font=dict(size=16, color=GOLD)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT),
        height=320,
        margin=dict(l=60, r=20, t=50, b=40),
        xaxis=dict(title="Group", tickfont=dict(color=TEXT, size=12)),
        yaxis=dict(title="", tickfont=dict(color=TEXT, size=11), autorange="reversed"),
    )
    return fig


def make_win_prob():
    top = win_prob.head(12).sort_values("championship_probability_%")
    colors = [GOLD if t == top.iloc[-1]["team"] else GREEN_MID for t in top["team"]]

    fig = go.Figure(go.Bar(
        x=top["championship_probability_%"],
        y=top["team"],
        orientation="h",
        marker_color=colors,
        text=[f"{v:.1f}%" for v in top["championship_probability_%"]],
        textposition="outside",
        textfont=dict(color=TEXT, size=11),
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>"
    ))
    fig.update_layout(
        title=dict(text="🏆 Championship Probability (1000 simulations)", font=dict(size=16, color=GOLD)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT),
        height=380,
        margin=dict(l=110, r=60, t=50, b=40),
        xaxis=dict(title="Win Probability (%)", tickfont=dict(color=TEXT),
                   gridcolor="#2a2a4a", range=[0, top["championship_probability_%"].max() + 5]),
        yaxis=dict(tickfont=dict(color=TEXT, size=11)),
    )
    return fig


def make_top_scorers():
    top = scorers.nlargest(12, "projected_goals").sort_values("projected_goals")
    stage_colors = {
        "Champion":       GOLD,
        "Final":          "#f0a500",
        "3rd Place":      GREEN_MID,
        "Semi-final":     GREEN_DARK,
        "Quarter-final":  "#1d6348",
        "Round of 16":    "#155233",
        "Round of 32":    "#0d3b1f",
        "Group Stage":    "#555",
    }
    colors = [stage_colors.get(s, "#555") for s in top["exit_stage"]]

    fig = go.Figure(go.Bar(
        x=top["projected_goals"],
        y=top["name"] + " (" + top["team_name"] + ")",
        orientation="h",
        marker_color=colors,
        text=[f"{v:.1f}" for v in top["projected_goals"]],
        textposition="outside",
        textfont=dict(color=TEXT, size=11),
        hovertemplate="<b>%{y}</b><br>Projected goals: %{x:.1f}<extra></extra>"
    ))
    fig.update_layout(
        title=dict(text="⚽ Predicted Top Scorers", font=dict(size=16, color=GOLD)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT),
        height=400,
        margin=dict(l=180, r=60, t=50, b=40),
        xaxis=dict(title="Projected Goals", tickfont=dict(color=TEXT),
                   gridcolor="#2a2a4a", range=[0, top["projected_goals"].max() + 1]),
        yaxis=dict(tickfont=dict(color=TEXT, size=10)),
    )
    return fig


def make_bracket(stage_filter="All"):
    stages_order = ["Round of 32", "Round of 16", "Quarter-final",
                    "Semi-final", "3rd Place", "Final"]
    df = bracket.copy()
    if stage_filter != "All":
        df = df[df["stage"] == stage_filter]

    fig = go.Figure()
    for i, row in df.iterrows():
        t1_pct = row["p_team1_win"]
        t2_pct = row["p_team2_win"]
        winner = row["predicted_winner"]
        match_label = f"{row['team1']} vs {row['team2']}"

        c1 = GOLD if row["team1"] == winner else "#444"
        c2 = GOLD if row["team2"] == winner else "#444"

        fig.add_trace(go.Bar(
            name=row["team1"],
            x=[t1_pct],
            y=[match_label],
            orientation="h",
            marker_color=c1,
            text=f"{row['team1']} {t1_pct:.0f}%",
            textposition="inside",
            textfont=dict(color="white", size=10),
            showlegend=False,
            hovertemplate=f"<b>{row['team1']}</b>: {t1_pct:.1f}%<extra></extra>"
        ))
        fig.add_trace(go.Bar(
            name=row["team2"],
            x=[t2_pct],
            y=[match_label],
            orientation="h",
            marker_color=c2,
            text=f"{row['team2']} {t2_pct:.0f}%",
            textposition="inside",
            textfont=dict(color="white", size=10),
            showlegend=False,
            hovertemplate=f"<b>{row['team2']}</b>: {t2_pct:.1f}%<extra></extra>"
        ))

    height = max(350, len(df) * 38)
    fig.update_layout(
        barmode="stack",
        title=dict(text="🏟️ Tournament Bracket — Win Probabilities", font=dict(size=16, color=GOLD)),
        paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        font=dict(color=TEXT),
        height=height,
        margin=dict(l=200, r=20, t=50, b=40),
        xaxis=dict(title="Win Probability (%)", range=[0, 100],
                   tickfont=dict(color=TEXT), gridcolor="#2a2a4a"),
        yaxis=dict(tickfont=dict(color=TEXT, size=10), autorange="reversed"),
    )
    return fig


# ── Summary cards ──────────────────────────────────────────────────────────────
def stat_card(title, value, color=GREEN_MID):
    return dbc.Card([
        dbc.CardBody([
            html.P(title, className="text-muted mb-1", style={"fontSize": "12px"}),
            html.H4(value, style={"color": color, "fontWeight": "bold", "marginBottom": 0})
        ])
    ], style={"backgroundColor": CARD_BG, "border": f"1px solid {color}", "borderRadius": "8px"})


# ── Layout ─────────────────────────────────────────────────────────────────────
app.layout = dbc.Container([

    # ── Header ──────────────────────────────────────────────────────────────────
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H1("🏆 2026 FIFA World Cup Predictor",
                        style={"color": GOLD, "fontWeight": "bold", "marginBottom": "4px"}),
                html.P("ELO model · 92 years of historical data · 1000 Monte Carlo simulations · Logistic Regression 76.1% accuracy",
                       style={"color": TEXT, "fontSize": "13px", "marginBottom": 0})
            ], style={"padding": "20px 0 10px 0"})
        ])
    ]),

    # ── Summary stats row ────────────────────────────────────────────────────────
    dbc.Row([
        dbc.Col(stat_card("🏆 Predicted Champion", "France", GOLD), width=3),
        dbc.Col(stat_card("🥈 Runner-up", "Brazil"), width=3),
        dbc.Col(stat_card("⚽ Top Scorer", "K. Mbappé  7.8 goals"), width=3),
        dbc.Col(stat_card("📊 Model Accuracy", "76.1% (5-fold CV)"), width=3),
    ], className="mb-3"),

    # ── Group heatmap full width ─────────────────────────────────────────────────
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([dcc.Graph(figure=make_group_heatmap(), config={"displayModeBar": False})])
            ], style={"backgroundColor": CARD_BG, "border": "1px solid #2a2a4a"})
        ])
    ], className="mb-3"),

    # ── Win prob + Top scorers ────────────────────────────────────────────────────
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([dcc.Graph(figure=make_win_prob(), config={"displayModeBar": False})])
            ], style={"backgroundColor": CARD_BG, "border": "1px solid #2a2a4a"})
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([dcc.Graph(figure=make_top_scorers(), config={"displayModeBar": False})])
            ], style={"backgroundColor": CARD_BG, "border": "1px solid #2a2a4a"})
        ], width=6),
    ], className="mb-3"),

    # ── Bracket with stage filter ─────────────────────────────────────────────────
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(html.H5("Filter by Stage:", style={"color": TEXT, "marginTop": "6px"}), width="auto"),
                        dbc.Col(dcc.Dropdown(
                            id="stage-filter",
                            options=[{"label": "All Stages", "value": "All"}] +
                                    [{"label": s, "value": s} for s in
                                     ["Round of 32", "Round of 16", "Quarter-final",
                                      "Semi-final", "3rd Place", "Final"]],
                            value="All",
                            clearable=False,
                            style={"backgroundColor": "#2a2a4a", "color": "#000", "width": "200px"}
                        ), width="auto")
                    ], align="center", className="mb-3"),
                    dcc.Graph(id="bracket-chart", config={"displayModeBar": False})
                ])
            ], style={"backgroundColor": CARD_BG, "border": "1px solid #2a2a4a"})
        ])
    ], className="mb-3"),

    # ── Footer ───────────────────────────────────────────────────────────────────
    dbc.Row([
        dbc.Col([
            html.P("Built by Mamed Mammadov · BSB Data Analytics · Python · XGBoost · Dash · Docker",
                   style={"color": "#666", "fontSize": "12px", "textAlign": "center", "padding": "10px 0"})
        ])
    ])

], fluid=True, style={"backgroundColor": BG, "minHeight": "100vh", "padding": "0 20px"})


# ── Callback ───────────────────────────────────────────────────────────────────
@app.callback(
    Output("bracket-chart", "figure"),
    Input("stage-filter", "value")
)
def update_bracket(stage):
    return make_bracket(stage)


server = app.server

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=False)
