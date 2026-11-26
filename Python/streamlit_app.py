# app.py
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Diabetes Dashboard", page_icon="🩸", layout="wide")

CHART_H = 260  # smaller = more room, bigger = taller charts

# ---------- Colors (dark red / maroon / light red) ----------
MAROON, WINE, RED, LIGHT_RED, PINK = "#4A0D1F", "#7B1230", "#C62839", "#E8636B", "#F5A3A8"
RED_SCALE = ["#FDE8EA", PINK, LIGHT_RED, RED, WINE, MAROON]
INCOME_ORDER = ["Low", "Lower-middle", "Upper-middle", "High", "Unknown"]
AGES = ['18-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
MID_AGES = ['30-34', '35-39', '40-44', '45-49', '50-54', '55-59']
RATE = "diabetes_rate_age_standardized_pct"
LABELS = {RATE: "Diabetes rate (%)", "year": "Year", "country": "Country", "age_group": "Age group", "rate": "Rate (%)", "millions": "Patients (millions)", "group": ""}

st.markdown(f"""
<style>
header[data-testid="stHeader"] {{ display: none; }}
footer {{ display: none; }}
.block-container {{ padding: 0.6rem 1.2rem 0 1.2rem !important; max-width: 100% !important; }}
[data-testid="stVerticalBlock"] {{ gap: 0.5rem !important; }}
[data-testid="stHorizontalBlock"] {{ gap: 0.7rem !important; }}

.stApp {{ background-color: #FFF7F7; }}
section[data-testid="stSidebar"] {{ background-color: #FBE9EB; }}

.stApp, .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3, .stApp div {{ color: {MAROON}; }}
section[data-testid="stSidebar"] *, [data-testid="stWidgetLabel"] * {{ color: {MAROON} !important; }}

div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {{ background-color: white !important; }}
div[data-baseweb="select"] * {{ color: {MAROON} !important; }}
span[data-baseweb="tag"] {{ background-color: {WINE} !important; }}
span[data-baseweb="tag"] * {{ color: white !important; }}
div[data-baseweb="popover"] * {{ background-color: white; color: {MAROON} !important; }}

.stButton > button {{ font-size: 22px; background: white; border: 1px solid {WINE}; padding: 0.2rem 0; }}
.stButton > button * {{ color: {MAROON} !important; }}
.stButton > button[kind="primary"] {{ background-color: {WINE}; border-color: {WINE}; }}
.stButton > button[kind="primary"] * {{ color: white !important; }}

div[data-testid="stMetric"] {{ background: white; border-left: 6px solid {WINE}; padding: 4px 12px; border-radius: 10px; box-shadow: 0 1px 4px rgba(74,13,31,.15); }}
[data-testid="stMetricLabel"] * {{ color: {WINE} !important; font-size: 13px !important; }}
[data-testid="stMetricValue"] * {{ color: {MAROON} !important; font-size: 24px !important; font-weight: 700; }}
</style>
""", unsafe_allow_html=True)


# ---------- Helpers (work on old and new Streamlit versions) ----------
def show_chart(fig):
    try:
        st.plotly_chart(fig, width="stretch", theme=None)
    except TypeError:
        st.plotly_chart(fig, use_container_width=True, theme=None)


def nav_button(label, key, help_text, active):
    kind = "primary" if active else "secondary"
    try:
        return st.button(label, key=key, help=help_text, width="stretch", type=kind)
    except TypeError:
        return st.button(label, key=key, help=help_text, use_container_width=True, type=kind)


def need(cond, msg):
    if not cond:
        raise ValueError(msg)


# ---------- Load data (CSV or parquet, next to this file) ----------
@st.cache_data
def load_data():
    here = Path(__file__).parent
    parquet = here / "diabetes_clean.parquet"
    csv = here / "diabetes_clean.csv"

    if parquet.exists():
        df = pd.read_parquet(parquet)
    elif csv.exists():
        df = pd.read_csv(csv, encoding="utf-8-sig")
    else:
        st.error(f"Put diabetes_clean.csv (or .parquet) in this folder: {here}")
        st.stop()

    df["age_group"] = pd.Categorical(df["age_group"].astype(str), categories=AGES, ordered=True)
    df["untreated_patients"] = pd.to_numeric(df["untreated_patients"], errors="coerce").astype("float")
    df["country_diabetes_deaths"] = pd.to_numeric(df["country_diabetes_deaths"], errors="coerce").astype("float")
    df["income_level"] = df["income_level"].fillna("Unknown").astype(str)
    df["region"] = df["region"].astype(str)
    df["sex"] = df["sex"].astype(str)
    return df


df = load_data()

# ---------- Pages ----------
PAGES = {
    "world": ("🌍", "Global Picture"),
    "focus": ("📍", "Country Focus"),
    "risk": ("🔬", "Risk Factors & Spending"),
}
if st.session_state.get("page") not in PAGES:
    st.session_state.page = "world"

# ---------- Sidebar: page icons + filters ----------
with st.sidebar:
    st.markdown("### 🩸 Diabetes Dashboard")
    cols = st.columns(len(PAGES))
    for col, (key, (icon, name)) in zip(cols, PAGES.items()):
        with col:
            if nav_button(icon, f"nav_{key}", name, st.session_state.page == key):
                st.session_state.page = key
                st.rerun()
    st.markdown(f"**{PAGES[st.session_state.page][0]} {PAGES[st.session_state.page][1]}**")

    st.divider()
    st.markdown("### 🔍 Filters")
    y_min, y_max = int(df.year.min()), int(df.year.max())
    years = st.slider("Years", y_min, y_max, (y_min, y_max))
    regions = st.multiselect("Region", sorted(df.region.unique()))
    incomes = st.multiselect("Income level", INCOME_ORDER)
    sexes = st.multiselect("Sex", ["Men", "Women"])

    opts = df
    if regions:
        opts = opts[opts.region.isin(regions)]
    if incomes:
        opts = opts[opts.income_level.isin(incomes)]
    countries = st.multiselect("Country", sorted(opts.country.unique()))

    all_countries = sorted(df.country.unique())
    hl_index = all_countries.index("Egypt") if "Egypt" in all_countries else 0
    hl = st.selectbox("Highlight country", all_countries, index=hl_index)

    st.caption("Source: Our World in Data and others.")

# ---------- Apply filters ----------
f = df[df.year.between(*years)]
if regions:
    f = f[f.region.isin(regions)]
if incomes:
    f = f[f.income_level.isin(incomes)]
if sexes:
    f = f[f.sex.isin(sexes)]
if countries:
    f = f[f.country.isin(countries)]

if f.empty:
    st.warning("No data for these filters. Try changing them.")
    st.stop()

y0, ly = years[0], years[1]  # first year, snapshot year

CTY_COLS = ["country_code", "country", "region", "year", "income_level", "country_population", "country_diabetes_deaths", RATE, "obesity_rate_pct", "sugar_starch_pct_of_calories", "gdp_per_capita_ppp", "health_spending_total_usd", "health_coverage_index"]


def build_cty(frame):
    """One row per country-year (columns repeated on age/sex rows are counted once)."""
    meta = frame.drop_duplicates(["country", "year"])[CTY_COLS].copy()
    tot = frame.groupby(["country", "year"], observed=True).agg(diabetes_patients=("diabetes_patients", "sum"), adult_population=("population", "sum")).reset_index()
    kn = frame.dropna(subset=["untreated_patients"])
    gp = kn.groupby(["country", "year"], observed=True).agg(unt=("untreated_patients", "sum"), pat=("diabetes_patients", "sum")).reset_index()
    gp["treatment_gap_pct"] = gp["unt"] / gp["pat"] * 100
    out = meta.merge(tot, on=["country", "year"], how="left")
    out = out.merge(gp[["country", "year", "treatment_gap_pct"]], on=["country", "year"], how="left")
    out["spend_per_person"] = out["health_spending_total_usd"] / out["country_population"]
    return out


@st.cache_data
def cty_for(a, b):
    return build_cty(df[df.year.between(a, b)])


cty = build_cty(f)                 # follows all filters
cty_all = cty_for(y0, y1 := ly)    # all countries, only the year range (for the highlighted country)

snap_f = f[f.year == ly]
snap = cty[cty.year == ly]
hl_c = cty_all[cty_all.country == hl]
hl_snap = hl_c[hl_c.year == ly]
dly = df[df.year == ly]


def sx(d):
    return d[d.sex.isin(sexes)] if sexes else d


AXIS = dict(color=MAROON, tickfont=dict(color=MAROON, size=10), title_font=dict(color=MAROON, size=11), gridcolor="#EBD5D8", linecolor="#C9A3A8", zerolinecolor="#C9A3A8")


def style(fig, h=CHART_H):
    bottom = 44 if fig.layout.sliders else 8
    fig.update_layout(template="plotly_white", height=h, margin=dict(l=8, r=8, t=36, b=bottom), title_font=dict(size=13, color=MAROON), title_x=0.0, legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="right", x=1, title_text="", font=dict(size=9, color=MAROON)), paper_bgcolor="white", plot_bgcolor="white", font=dict(size=10, color=MAROON), hoverlabel=dict(font_color="white", bgcolor=MAROON))
    fig.update_xaxes(**AXIS)
    fig.update_yaxes(**AXIS)
    return fig


# ---------- KPIs (top, fixed) ----------
tot_pat = snap_f.diabetes_patients.sum()
tot_pop = snap_f.population.sum()
prev = tot_pat / tot_pop * 100 if tot_pop else 0
k = snap_f.dropna(subset=["untreated_patients"])
unt_share = k.untreated_patients.sum() / k.diabetes_patients.sum() * 100 if len(k) else float("nan")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric(f"Diabetes patients ({ly})", f"{tot_pat/1e6:,.1f}M")
k2.metric("Prevalence (18+)", f"{prev:.1f}%")
k3.metric("Avg age-std. rate", f"{snap[RATE].mean():.1f}%")
k4.metric("Untreated share", "—" if pd.isna(unt_share) else f"{unt_share:.1f}%")
k5.metric("Avg obesity rate", f"{snap.obesity_rate_pct.mean():.1f}%")


# =====================================================================
# Charts
# =====================================================================
def hl_colors(names):
    return [MAROON if n == hl else PINK for n in names]


# ---- Page 1: Global picture ----
def c_map():
    md = cty.sort_values("year")
    fig = px.choropleth(md, locations="country_code", color=RATE, hover_name="country", animation_frame="year", color_continuous_scale=RED_SCALE, range_color=(0, 35), labels=LABELS, projection="natural earth", title="Diabetes rate by country over time (age-standardized %)")
    fig.update_geos(showframe=False, showcoastlines=False, showland=True, landcolor="#EEEEEE")
    fig.update_coloraxes(showscale=False)
    if fig.layout.sliders:
        for s in fig.layout.sliders[0].steps:
            if int(s.label) % 5 != 0 and int(s.label) != ly:
                s.label = ""
        fig.layout.sliders[0].update(pad=dict(t=0, b=0), len=0.8, x=0.15, currentvalue=dict(visible=False), font=dict(size=9, color=MAROON))
    if fig.layout.updatemenus:
        fig.layout.updatemenus[0].update(pad=dict(t=0, r=5), x=0.1, y=0.0)
    return fig


def c_world():
    w = cty.groupby("year").diabetes_patients.sum().reset_index()
    w["millions"] = w["diabetes_patients"] / 1e6
    return px.line(w, x="year", y="millions", markers=True, title="Diabetes patients over time (millions)", color_discrete_sequence=[WINE], labels=LABELS)


def c_top15():
    t = snap.nlargest(15, RATE).sort_values(RATE)
    need(len(t) > 0, "No data for this year")
    fig = px.bar(t, x=RATE, y="country", orientation="h", text=t[RATE].round(1), title=f"Top 15 countries by diabetes rate ({ly})", labels=LABELS)
    fig.update_traces(marker_color=hl_colors(t["country"]), textposition="outside", cliponaxis=False, textfont=dict(color=MAROON, size=9))
    fig.update_yaxes(tickfont=dict(size=8, color=MAROON))
    return fig


def c_incr():
    need(y0 < ly, "Pick a year range with at least two years")
    two = cty[cty.year.isin([y0, ly])].pivot(index="country", columns="year", values=RATE).dropna()
    need(len(two) > 0, "No countries with data in both years")
    two["increase"] = two[ly] - two[y0]
    t = two.sort_values("increase", ascending=False).head(10).sort_values("increase").reset_index()
    t = t[["country", "increase"]]
    fig = px.bar(t, x="increase", y="country", orientation="h", text=t["increase"].round(1), title=f"Top 10 rise in diabetes rate, {y0} to {ly} (pct. points)", labels={"increase": "Increase (pct. points)", "country": "Country"})
    fig.update_traces(marker_color=hl_colors(t["country"]), textposition="outside", cliponaxis=False, textfont=dict(color=MAROON, size=9))
    return fig


# ---- Page 2: Country focus ----
def c_vs():
    need(len(hl_c) > 0, f"No data for {hl}")
    med = cty.groupby("year")[RATE].median().reset_index(name="Median of countries")
    mine = hl_c[["year", RATE]].rename(columns={RATE: hl})
    m = med.merge(mine, on="year")
    long = m.melt(id_vars="year", var_name="group", value_name="rate")
    return px.line(long, x="year", y="rate", color="group", title=f"{hl} vs median of countries: diabetes rate (age-std. %)", color_discrete_map={hl: MAROON, "Median of countries": LIGHT_RED}, labels=LABELS)


def age_rates(d):
    g = d.groupby("age_group", observed=True)[["diabetes_patients", "population"]].sum()
    return g["diabetes_patients"] / g["population"] * 100


def c_age():
    h = sx(dly[dly.country == hl])
    need(len(h) > 0, f"No data for {hl}")
    a = pd.DataFrame({hl: age_rates(h), "All countries (filtered)": age_rates(snap_f)}).reset_index()
    a["age_group"] = a["age_group"].astype(str)
    long = a.melt(id_vars="age_group", var_name="group", value_name="rate")
    return px.line(long, x="age_group", y="rate", color="group", markers=True, title=f"Prevalence by age group: {hl} vs world ({ly})", color_discrete_map={hl: MAROON, "All countries (filtered)": LIGHT_RED}, category_orders={"age_group": AGES}, labels=LABELS)


def c_unt_age():
    h = sx(dly[dly.country == hl]).dropna(subset=["untreated_patients"])
    need(len(h) > 0, f"No untreated data for {hl} in {ly}")
    g = h.groupby("age_group", observed=True).untreated_patients.sum().reset_index()
    g["age_group"] = g["age_group"].astype(str)
    g["millions"] = g["untreated_patients"] / 1e6
    share = g[g.age_group.isin(MID_AGES)].untreated_patients.sum() / g.untreated_patients.sum() * 100
    fig = px.bar(g, x="age_group", y="millions", text=g["millions"].round(2), title=f"{hl}: untreated patients by age, millions (ages 30-59 = {share:.0f}%)", labels={"millions": "Untreated (millions)", "age_group": "Age group"}, category_orders={"age_group": AGES})
    fig.update_traces(marker_color=[MAROON if a in MID_AGES else PINK for a in g["age_group"]], textposition="outside", cliponaxis=False, textfont=dict(color=MAROON, size=9))
    return fig


def c_gap_income():
    g = snap[snap.income_level != "Unknown"].dropna(subset=["treatment_gap_pct"])
    need(len(g) > 0, "No treatment data for this year")
    gi = g.groupby("income_level").treatment_gap_pct.median().reindex(["Low", "Lower-middle", "Upper-middle", "High"]).dropna().reset_index()
    fig = px.bar(gi, x="income_level", y="treatment_gap_pct", text=gi["treatment_gap_pct"].round(1), title=f"Untreated share of patients 30+ by country income, median % ({ly})", labels={"income_level": "Country income level", "treatment_gap_pct": "Untreated (%)"})
    fig.update_traces(marker_color=PINK, textposition="outside", cliponaxis=False, textfont=dict(color=MAROON, size=10))
    hv = hl_snap["treatment_gap_pct"].dropna()
    if len(hv) > 0:
        v = float(hv.iloc[0])
        fig.add_hline(y=v, line_color=MAROON, line_width=2, annotation_text=f"{hl}: {v:.1f}%", annotation_position="top right", annotation_font_color=MAROON)
    return fig


# ---- Page 3: Risk factors & spending ----
def c_scatter():
    s = snap.dropna(subset=["obesity_rate_pct", RATE])
    extra = hl_snap[~hl_snap.country.isin(s.country)].dropna(subset=["obesity_rate_pct", RATE])
    s = pd.concat([s, extra]).copy()
    need(len(s) > 0, "No data for this year")
    s["group"] = s["country"].eq(hl).map({True: hl, False: "Other countries"})
    fig = px.scatter(s, x="obesity_rate_pct", y=RATE, color="group", hover_name="country", title=f"Obesity vs diabetes rate ({ly})", color_discrete_map={hl: MAROON, "Other countries": PINK}, category_orders={"group": ["Other countries", hl]}, labels={"obesity_rate_pct": "Obesity rate (%)", RATE: "Diabetes rate (%)", "group": ""})
    fig.update_traces(marker=dict(size=7, line=dict(width=0.5, color="white")))
    fig.update_traces(selector=dict(name=hl), marker=dict(size=13, color=MAROON, line=dict(width=1, color="white")))
    return fig


def c_deaths():
    ca = cty_all[cty_all.country.isin(cty.country.unique())]
    av = ca.dropna(subset=["country_diabetes_deaths"])
    need(len(av) > 0, "No deaths data for the selected countries")
    yd = int(av.year.max())
    d = av[av.year == yd].copy()
    d["deaths_per_1000"] = d["country_diabetes_deaths"] / d["diabetes_patients"] * 1000
    d = d.dropna(subset=["deaths_per_1000", "spend_per_person"])
    need(len(d) >= 8, "Not enough countries with deaths and spending data")
    labs = ["Lowest spend", "Low-mid", "High-mid", "Highest spend"]
    d["grp"] = pd.qcut(d["spend_per_person"].rank(method="first"), 4, labels=labs)
    t = d.groupby("grp", observed=True).deaths_per_1000.median().reset_index()
    fig = px.bar(t, x="grp", y="deaths_per_1000", text=t["deaths_per_1000"].round(1), title=f"Deaths per 1,000 patients by health spending per person, median ({yd})", labels={"grp": "Health spending per person", "deaths_per_1000": "Deaths per 1,000 patients"})
    fig.update_traces(marker_color=PINK, textposition="outside", cliponaxis=False, textfont=dict(color=MAROON, size=10))
    h = d[d.country == hl]
    if len(h) > 0:
        v = float(h["deaths_per_1000"].iloc[0])
        fig.add_hline(y=v, line_color=MAROON, line_width=2, annotation_text=f"{hl}: {v:.1f}", annotation_position="top right", annotation_font_color=MAROON)
    return fig


def c_heat():
    names = {RATE: "Diabetes rate", "obesity_rate_pct": "Obesity", "gdp_per_capita_ppp": "GDP per capita", "sugar_starch_pct_of_calories": "Sugar & starch", "spend_per_person": "Health spend / person", "health_coverage_index": "Coverage index", "treatment_gap_pct": "Untreated share"}
    need(len(snap) > 5, "Not enough countries for correlations")
    h = snap[list(names)].corr(method="spearman").rename(index=names, columns=names).round(2)
    fig = px.imshow(h, text_auto=True, zmin=-1, zmax=1, aspect="auto", color_continuous_scale=["#3B6FA0", "#FFFFFF", "#7B1230"], title=f"Correlations between diabetes, risk factors and treatment, Spearman ({ly})")
    fig.update_coloraxes(showscale=False)
    fig.update_traces(textfont=dict(size=10))
    return fig


BUILD = {
    "world": [c_map, c_world, c_top15, c_incr],
    "focus": [c_vs, c_age, c_unt_age, c_gap_income],
    "risk": [c_scatter, c_deaths, c_heat],
}


def render(fn):
    try:
        fig = fn()
    except Exception as e:
        st.info("Chart not available for the current filters: " + str(e))
        return
    show_chart(style(fig))


# ---------- Grid: 2 per row, a last single chart takes the full width ----------
items = BUILD[st.session_state.page]
for i in range(0, len(items), 2):
    chunk = items[i:i + 2]
    row = st.columns(len(chunk))
    for col, fn in zip(row, chunk):
        with col:
            render(fn)