import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import urllib.request
import urllib.error
import os
import logging

# ── Logging (errores internos no expuestos al usuario) ────────────────────────
logging.basicConfig(level=logging.ERROR, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tech Jobs EDA · Stack Overflow 2025",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Design system ─────────────────────────────────────────────────────────────
COLORS = {
    "bg":        "#0a1628",
    "surface":   "#0f2040",
    "surface2":  "#162850",
    "border":    "rgba(59,130,246,0.18)",
    "primary":   "#3B82F6",
    "primary_d": "#1E40AF",
    "accent":    "#D97706",
    "accent_l":  "#F59E0B",
    "success":   "#10B981",
    "danger":    "#EF4444",
    "text":      "#E2E8F0",
    "muted":     "rgba(226,232,240,0.45)",
}

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=COLORS["text"], family="Inter, sans-serif"),
    margin=dict(l=20, r=20, t=40, b=20),
    colorway=[
        COLORS["primary"], COLORS["accent"], COLORS["success"],
        "#8B5CF6", "#EC4899", "#06B6D4", "#84CC16",
    ],
)

GRID_STYLE = dict(
    showgrid=True,
    gridcolor="rgba(59,130,246,0.12)",
    zeroline=False,
    linecolor="rgba(59,130,246,0.2)",
)

# ── Global CSS (minified — sin comentarios para evitar traduccion automatica) ──
st.markdown("""
<meta name="google" content="notranslate">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#061020 0%,#0a1628 100%);border-right:1px solid rgba(59,130,246,0.2);}
[data-testid="stSidebar"] .block-container{padding-top:1rem;}
.main{background:#0a1628;}
.main .block-container{padding-top:1.5rem;}
[data-testid="metric-container"]{background:linear-gradient(135deg,#0f2040 0%,#162850 100%);border:1px solid rgba(59,130,246,0.2);border-radius:14px;padding:1.1rem 1.2rem;transition:transform 0.2s ease,border-color 0.25s ease,box-shadow 0.25s ease;}
[data-testid="metric-container"]:hover{transform:translateY(-3px);border-color:rgba(59,130,246,0.55);box-shadow:0 8px 32px rgba(30,64,175,0.25);}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:#60A5FA;font-size:1.9rem;font-weight:700;font-family:'Fira Code',monospace;}
[data-testid="metric-container"] [data-testid="stMetricLabel"]{color:rgba(226,232,240,0.55);font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;font-weight:600;}
[data-testid="metric-container"] [data-testid="stMetricDelta"] svg{display:none;}
[data-testid="stTabs"] [data-baseweb="tab-list"]{background:#0f2040;border-radius:12px;padding:4px 6px;gap:4px;border:1px solid rgba(59,130,246,0.2);}
[data-testid="stTabs"] [data-baseweb="tab"]{border-radius:9px;color:rgba(226,232,240,0.5);font-weight:500;font-size:0.85rem;transition:all 0.2s ease;padding:6px 16px;}
[data-testid="stTabs"] [aria-selected="true"]{background:linear-gradient(135deg,#1E40AF 0%,#3B82F6 100%) !important;color:white !important;box-shadow:0 4px 12px rgba(30,64,175,0.35);}
[data-testid="stSelectbox"] > div > div{background:#0f2040 !important;border:1px solid rgba(59,130,246,0.25) !important;border-radius:10px !important;color:#e2e8f0 !important;}
[data-testid="stMultiSelect"] > div > div{background:#0f2040 !important;border:1px solid rgba(59,130,246,0.25) !important;border-radius:10px !important;}
[data-testid="stSlider"] > div > div > div{background:linear-gradient(90deg,#1E40AF,#3B82F6) !important;}
.section-title{font-size:1.15rem;font-weight:700;color:#E2E8F0;margin:1.4rem 0 0.75rem 0;padding-bottom:0.5rem;border-bottom:1px solid rgba(59,130,246,0.2);letter-spacing:-0.01em;}
.kpi-badge{display:inline-block;background:rgba(59,130,246,0.15);border:1px solid rgba(59,130,246,0.3);color:#93C5FD;padding:2px 10px;border-radius:20px;font-size:0.75rem;font-weight:600;font-family:'Fira Code',monospace;margin-left:8px;vertical-align:middle;}
hr{border:none;height:1px;background:linear-gradient(90deg,transparent,rgba(59,130,246,0.35),transparent);margin:1.5rem 0;}
::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-track{background:#0a1628;}
::-webkit-scrollbar-thumb{background:#1E40AF;border-radius:4px;}
@keyframes fadeUp{from{opacity:0;transform:translateY(18px);}to{opacity:1;transform:translateY(0);}}
.main .block-container{animation:fadeUp 0.45s ease forwards;}
.insight-box{background:linear-gradient(135deg,rgba(30,64,175,0.15) 0%,rgba(59,130,246,0.08) 100%);border:1px solid rgba(59,130,246,0.25);border-left:3px solid #3B82F6;border-radius:10px;padding:0.85rem 1.1rem;margin:0.6rem 0;font-size:0.87rem;color:rgba(226,232,240,0.85);line-height:1.6;}
.insight-box strong{color:#93C5FD;}
.accent-amber{color:#F59E0B;font-weight:700;}
.accent-blue{color:#60A5FA;font-weight:700;}
.accent-green{color:#34D399;font-weight:700;}
.accent-red{color:#F87171;font-weight:700;}
</style>
""", unsafe_allow_html=True)


# ── Data loading ──────────────────────────────────────────────────────────────
ALLOWED_CSV = "salaries.csv"   # única ruta permitida — nunca exponer rutas del sistema
MAX_FILE_MB = 200              # límite de tamaño del CSV

@st.cache_data(show_spinner=False)
def load_data():
    csv_path = ALLOWED_CSV
    url = "https://raw.githubusercontent.com/nicholasgasior/public-data/main/survey_results_public_2025.csv"

    # ── Descarga segura ───────────────────────────────────────────────────────
    if not os.path.exists(csv_path):
        try:
            with st.spinner("⬇️ Descargando dataset…"):
                urllib.request.urlretrieve(url, csv_path)
        except urllib.error.URLError as e:
            logger.error("Descarga fallida: %s", e)
            st.error("❌ Sin conexión a internet. Coloca `salaries.csv` en la carpeta del proyecto y reinicia.")
            st.stop()
        except Exception as e:
            logger.error("Error inesperado en descarga: %s", e)
            st.error("❌ No se pudo obtener el dataset. Intenta de nuevo o coloca `salaries.csv` manualmente.")
            st.stop()

    # ── Validación del archivo ────────────────────────────────────────────────
    file_size_mb = os.path.getsize(csv_path) / (1024 * 1024)
    if file_size_mb > MAX_FILE_MB:
        st.error(f"❌ El archivo supera el límite de {MAX_FILE_MB} MB. Verifica que sea el dataset correcto.")
        st.stop()

    # ── Lectura segura ────────────────────────────────────────────────────────
    try:
        all_cols = pd.read_csv(csv_path, nrows=0).columns.tolist()
    except Exception as e:
        logger.error("No se pudo leer el CSV: %s", e)
        st.error("❌ El archivo `salaries.csv` no es un CSV válido o está corrupto. Elimínalo y recarga la página.")
        st.stop()

    # Detect experience column (name varies by survey year)
    exp_col = next((c for c in ["YearsCodePro", "YearsCode", "WorkExp"] if c in all_cols), None)

    # Detect salary column
    sal_col = next((c for c in ["ConvertedCompYearly", "ConvertedComp", "CompTotal"] if c in all_cols), None)

    cols = [
        "Country", "Employment", "EdLevel",
        "JobSat", "LanguageHaveWorkedWith",
        "DatabaseHaveWorkedWith", "WebframeHaveWorkedWith",
        "DevType", "OrgSize", "RemoteWork", "Age",
    ]
    if exp_col:
        cols.append(exp_col)
    if sal_col:
        cols.append(sal_col)

    usecols = [c for c in cols if c in all_cols]
    if not usecols:
        st.error("❌ El CSV no contiene ninguna columna reconocida. Verifica que sea el Stack Overflow Survey.")
        st.stop()

    try:
        df = pd.read_csv(csv_path, usecols=usecols, low_memory=False)
    except Exception as e:
        logger.error("Error al parsear CSV: %s", e)
        st.error("❌ Error al leer los datos. El archivo puede estar incompleto o dañado.")
        st.stop()

    if len(df) < 100:
        st.error("❌ El dataset tiene muy pocas filas. Verifica que el archivo no esté vacío.")
        st.stop()

    # Normalize salary column name
    if sal_col and sal_col in df.columns and sal_col != "Salary":
        df = df.rename(columns={sal_col: "Salary"})
    if "Salary" in df.columns:
        df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")
        df = df[df["Salary"].between(10_000, 500_000)]

    # Normalize experience column name
    if exp_col and exp_col in df.columns and exp_col != "YearsCodePro":
        df = df.rename(columns={exp_col: "YearsCodePro"})
    if "YearsCodePro" in df.columns:
        df["YearsCodePro"] = (
            df["YearsCodePro"]
            .replace({"Less than 1 year": "0", "More than 50 years": "51"})
            .pipe(pd.to_numeric, errors="coerce")
        )

    return df


with st.spinner("📡 Cargando datos…"):
    df = load_data()

N = len(df)


# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt(n, prefix="", suffix=""):
    if n >= 1_000_000:
        return f"{prefix}{n/1_000_000:.1f}M{suffix}"
    if n >= 1_000:
        return f"{prefix}{n/1_000:.1f}K{suffix}"
    return f"{prefix}{n:,.0f}{suffix}"

def chart(fig):
    try:
        fig.update_layout(**CHART_LAYOUT)
        fig.update_xaxes(**GRID_STYLE)
        fig.update_yaxes(**GRID_STYLE)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    except Exception as e:
        logger.error("Error al renderizar gráfico: %s", e)
        st.warning("⚠️ No se pudo renderizar este gráfico.")

def empty_state(msg="Sin datos suficientes para este gráfico con los filtros actuales."):
    st.markdown(f"""
    <div style="text-align:center; padding:2rem 1rem; color:rgba(226,232,240,0.35);
                border:1px dashed rgba(59,130,246,0.2); border-radius:12px; margin:0.5rem 0;">
        <div style="font-size:1.8rem; margin-bottom:0.5rem;">📭</div>
        <div style="font-size:0.85rem;">{msg}</div>
    </div>
    """, unsafe_allow_html=True)

def bar_blue(fig):
    """Apply a blue gradient to a bar chart trace."""
    fig.update_traces(marker_color=COLORS["primary"], marker_line_width=0)
    return fig

def insight(text):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1.2rem 0 0.5rem 0;">
        <div style="font-size:2.4rem; margin-bottom:0.3rem;">📊</div>
        <div style="font-size:1.05rem; font-weight:700; color:#93C5FD; letter-spacing:-0.01em;">
            Tech Jobs EDA
        </div>
        <div style="font-size:0.72rem; color:rgba(226,232,240,0.4); margin-top:2px;">
            Stack Overflow Survey 2025
        </div>
    </div>
    <hr style="margin:0.8rem 0;"/>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:0.78rem; color:rgba(226,232,240,0.5); font-weight:600; text-transform:uppercase; letter-spacing:0.07em; margin-bottom:0.5rem;">🔧 Filtros</div>', unsafe_allow_html=True)

    # Remote filter
    remote_opts = ["Todos", "Remoto", "Híbrido", "Presencial"]
    remote_sel = st.selectbox("Modalidad de trabajo", remote_opts)

    # Country filter
    country_opts = ["Todos"]
    if "Country" in df.columns:
        top_countries = df["Country"].value_counts().head(20).index.tolist()
        country_opts += top_countries
    country_sel = st.selectbox("País (top 20)", country_opts)

    # Salary filter
    if "Salary" in df.columns and df["Salary"].notna().any():
        sal_min = max(0, int(df["Salary"].min()))
        sal_max = min(500_000, int(df["Salary"].max()))
        if sal_min >= sal_max:
            sal_min, sal_max = 10_000, 300_000
        sal_range = st.slider("Rango de salario (USD)", sal_min, sal_max, (sal_min, sal_max), step=5000)
        # Validación: mínimo siempre menor que máximo
        if sal_range[0] >= sal_range[1]:
            st.sidebar.error("El salario mínimo debe ser menor al máximo.")
            sal_range = (sal_min, sal_max)
    else:
        sal_range = (0, 999_999)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:0.75rem; color:rgba(226,232,240,0.35); text-align:center;">{N:,} respuestas · 172 columnas</div>', unsafe_allow_html=True)


# ── Apply filters ─────────────────────────────────────────────────────────────
def simplify_remote_global(val):
    v = str(val).lower()
    if "hybrid" in v:   return "Híbrido"
    if "remote" in v:   return "Remoto"
    if "person" in v:   return "Presencial"
    return "Otro"

dff = df.copy()
if remote_sel != "Todos" and "RemoteWork" in dff.columns:
    dff["_remote_simple"] = dff["RemoteWork"].apply(simplify_remote_global)
    dff = dff[dff["_remote_simple"] == remote_sel].drop(columns=["_remote_simple"])

if country_sel != "Todos" and "Country" in dff.columns:
    dff = dff[dff["Country"] == country_sel]
if "Salary" in dff.columns:
    dff = dff[dff["Salary"].between(*sal_range)]

# ── Aviso si los filtros no dejan datos ──────────────────────────────────────
if len(dff) == 0:
    st.warning("⚠️ La combinación de filtros no tiene resultados. Ajusta los filtros del panel izquierdo.")
    st.stop()


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="
    background: linear-gradient(135deg, #061836 0%, #0f2d5e 50%, #061836 100%);
    padding: 1.8rem 2rem;
    border-radius: 18px;
    border: 1px solid rgba(59,130,246,0.3);
    box-shadow: 0 4px 40px rgba(30,64,175,0.2);
    margin-bottom: 1.5rem;
">
    <div style="display:flex; align-items:center; gap:0.75rem; margin-bottom:0.4rem;">
        <span style="font-size:1.75rem;">📊</span>
        <h1 style="color:white; font-size:1.7rem; font-weight:800; margin:0; letter-spacing:-0.02em;">
            Tech Jobs EDA
        </h1>
        <span style="background:rgba(59,130,246,0.2); border:1px solid rgba(59,130,246,0.4); color:#93C5FD;
                     padding:3px 12px; border-radius:20px; font-size:0.75rem; font-weight:600; font-family:'Fira Code',monospace;">
            2025
        </span>
    </div>
    <p style="color:rgba(226,232,240,0.6); margin:0; font-size:0.9rem; line-height:1.5;">
        Análisis exploratorio del mercado tecnológico global · Stack Overflow Developer Survey
    </p>
</div>
""", unsafe_allow_html=True)

# ── KPI row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.metric("Respuestas", fmt(len(dff)))
with k2:
    st.metric("Países", dff["Country"].nunique() if "Country" in dff.columns else "—")
with k3:
    if "Salary" in dff.columns and dff["Salary"].notna().any():
        st.metric("Salario mediano", fmt(dff["Salary"].median(), "$"))
    else:
        st.metric("Salario mediano", "—")
with k4:
    if "Salary" in dff.columns and dff["Salary"].notna().any():
        st.metric("Salario máx", fmt(dff["Salary"].quantile(0.95), "$"))
    else:
        st.metric("Salario máx (p95)", "—")
with k5:
    if "YearsCodePro" in dff.columns:
        st.metric("Exp. mediana", f"{dff['YearsCodePro'].median():.0f} años")
    else:
        st.metric("Exp. mediana", "—")


st.markdown("<hr/>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "💼 Empleo & Mercado",
    "💰 Salarios",
    "🖥️ Tecnologías",
    "🌍 Geografía",
    "🎓 Educación & Exp.",
])


# ═══════════════════════════════════════════════════════════
# TAB 1 — Empleo & Mercado
# ═══════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-title">Distribución de modalidad de trabajo</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if "RemoteWork" in dff.columns:
            def simplify_remote(val):
                v = str(val).lower()
                if "hybrid" in v:
                    return "Híbrido"
                elif "remote" in v:
                    return "Remoto"
                elif "in-person" in v or "person" in v:
                    return "Presencial"
                return "Otro"

            remote_df = dff[dff["RemoteWork"].notna()].copy()
            remote_df["Modalidad"] = remote_df["RemoteWork"].apply(simplify_remote)
            remote_counts = remote_df["Modalidad"].value_counts().reset_index()
            remote_counts.columns = ["Modalidad", "Respuestas"]
            colors_pie = [COLORS["primary"], COLORS["accent"], COLORS["success"]]
            fig = go.Figure(go.Pie(
                labels=remote_counts["Modalidad"],
                values=remote_counts["Respuestas"],
                hole=0.55,
                marker=dict(colors=colors_pie, line=dict(color=COLORS["bg"], width=2)),
                textinfo="label+percent",
                textfont=dict(size=12),
            ))
            fig.update_layout(title="Modalidad de trabajo", **CHART_LAYOUT,
                              legend=dict(orientation="h", y=-0.1))
            chart(fig)

    with col2:
        if "OrgSize" in dff.columns:
            size_map = {
                "Just me - I am a freelancer, sole proprietor, etc.": "Freelance",
                "2 to 9 employees": "2–9",
                "10 to 19 employees": "10–19",
                "20 to 99 employees": "20–99",
                "100 to 499 employees": "100–499",
                "500 to 999 employees": "500–999",
                "1,000 to 4,999 employees": "1K–5K",
                "5,000 to 9,999 employees": "5K–10K",
                "10,000 or more employees": "10K+",
            }
            org = dff["OrgSize"].replace(size_map).value_counts().reset_index()
            org.columns = ["Tamaño", "Respuestas"]
            fig = go.Figure(go.Bar(
                x=org["Respuestas"], y=org["Tamaño"],
                orientation="h",
                marker_color=COLORS["primary"],
                marker_line_width=0,
            ))
            fig.update_layout(title="Tamaño de empresa", **CHART_LAYOUT, yaxis=dict(autorange="reversed"))
            fig.update_xaxes(**GRID_STYLE)
            fig.update_yaxes(showgrid=False)
            chart(fig)

    st.markdown('<div class="section-title">Satisfacción laboral</div>', unsafe_allow_html=True)

    if "JobSat" in dff.columns and dff["JobSat"].notna().any():
        # Detectar si los valores son numéricos o texto
        # Stack Overflow 2025: 1 = Very dissatisfied → 5 = Very satisfied (Likert estandar)
        numeric_map = {
            1: "Muy insatisfecho",
            2: "Algo insatisfecho",
            3: "Neutral",
            4: "Algo satisfecho",
            5: "Muy satisfecho",
        }
        text_map = {
            "Very satisfied":                       "Muy satisfecho",
            "Slightly satisfied":                   "Algo satisfecho",
            "Neither satisfied nor dissatisfied":   "Neutral",
            "Slightly dissatisfied":                "Algo insatisfecho",
            "Very dissatisfied":                    "Muy insatisfecho",
        }

        def map_jobsat(val):
            if pd.isna(val):
                return None
            # Primero intentar como número
            try:
                n = int(float(val))
                if n in numeric_map:
                    return numeric_map[n]
            except (ValueError, TypeError):
                pass
            # Luego como texto
            s = str(val).strip()
            if s in text_map:
                return text_map[s]
            # Valores fuera de rango no se mapean
            return None

        job_df = dff[dff["JobSat"].notna()].copy()
        job_df["Satisfacción"] = job_df["JobSat"].apply(map_jobsat)
        job_df = job_df[job_df["Satisfacción"].notna()]  # descartar valores no reconocidos

        order = ["Muy satisfecho", "Algo satisfecho", "Neutral", "Algo insatisfecho", "Muy insatisfecho"]
        job_sat = job_df["Satisfacción"].value_counts().reset_index()
        job_sat.columns = ["Satisfacción", "Respuestas"]
        job_sat["Satisfacción"] = pd.Categorical(job_sat["Satisfacción"], categories=order, ordered=True)
        job_sat = job_sat.sort_values("Satisfacción").dropna(subset=["Satisfacción"])

        sat_colors = [COLORS["success"], "#34D399", "#6B7280", COLORS["accent"], COLORS["danger"]]
        fig = go.Figure(go.Bar(
            x=job_sat["Satisfacción"].astype(str),
            y=job_sat["Respuestas"],
            marker_color=sat_colors[:len(job_sat)],
            marker_line_width=0,
            text=job_sat["Respuestas"].apply(lambda x: f"{x:,}"),
            textposition="outside",
            textfont=dict(size=10),
        ))
        fig.update_layout(title="Satisfacción en el trabajo", **CHART_LAYOUT)
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(**GRID_STYLE)
        chart(fig)

        total_valid = len(job_df)
        happy = job_df[job_df["Satisfacción"].isin(["Muy satisfecho", "Algo satisfecho"])]
        pct = len(happy) / total_valid * 100 if total_valid > 0 else 0
        insight(f'<span class="accent-green">{pct:.1f}%</span> de los encuestados están <strong>satisfechos</strong> con su trabajo actual.')
    else:
        empty_state("No hay datos de satisfacción laboral disponibles.")

    # Dev types
    st.markdown('<div class="section-title">Roles más comunes</div>', unsafe_allow_html=True)
    if "DevType" in dff.columns:
        devtype_series = dff["DevType"].dropna().str.split(";").explode().str.strip()
        devtype_counts = devtype_series.value_counts().head(12).reset_index()
        devtype_counts.columns = ["Rol", "Respuestas"]
        fig = go.Figure(go.Bar(
            x=devtype_counts["Respuestas"],
            y=devtype_counts["Rol"],
            orientation="h",
            marker_color=COLORS["primary"],
            marker_line_width=0,
        ))
        fig.update_layout(title="Top 12 roles de desarrolladores", **CHART_LAYOUT,
                          yaxis=dict(autorange="reversed"))
        fig.update_xaxes(**GRID_STYLE)
        fig.update_yaxes(showgrid=False)
        chart(fig)


# ═══════════════════════════════════════════════════════════
# TAB 2 — Salarios
# ═══════════════════════════════════════════════════════════
with tabs[1]:
    if "Salary" not in dff.columns or dff["Salary"].isna().all():
        st.info("No hay datos de salario con los filtros actuales.")
    else:
        st.markdown('<div class="section-title">Distribución de salarios</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            fig = go.Figure(go.Histogram(
                x=dff["Salary"].dropna(),
                nbinsx=50,
                marker_color=COLORS["primary"],
                marker_line_color=COLORS["bg"],
                marker_line_width=0.5,
                opacity=0.85,
            ))
            fig.update_layout(title="Histograma de salarios (USD)", **CHART_LAYOUT)
            fig.update_xaxes(tickprefix="$", **GRID_STYLE)
            fig.update_yaxes(**GRID_STYLE)
            chart(fig)

        with col2:
            if "RemoteWork" in dff.columns and "Salary" in dff.columns:
                def simplify_remote(val):
                    v = str(val).lower()
                    if "hybrid" in v:
                        return "Híbrido"
                    elif "remote" in v:
                        return "Remoto"
                    elif "in-person" in v or "person" in v:
                        return "Presencial"
                    return None

                box_df = dff[dff["RemoteWork"].notna() & dff["Salary"].notna()].copy()
                box_df["Modalidad"] = box_df["RemoteWork"].apply(simplify_remote)
                box_df = box_df[box_df["Modalidad"].notna()]

                order = ["Remoto", "Híbrido", "Presencial"]
                medians = (
                    box_df.groupby("Modalidad")["Salary"]
                    .median()
                    .reindex(order)
                    .dropna()
                )

                fig = go.Figure()
                palette = [COLORS["primary"], COLORS["accent"], COLORS["success"]]
                for i, mod in enumerate([m for m in order if m in box_df["Modalidad"].values]):
                    data = box_df[box_df["Modalidad"] == mod]["Salary"]
                    fig.add_trace(go.Box(
                        y=data,
                        name=mod,
                        marker_color=palette[i % len(palette)],
                        line_color=palette[i % len(palette)],
                        fillcolor=palette[i % len(palette)].replace(")", ", 0.15)").replace("rgb", "rgba") if "rgb" in palette[i % len(palette)] else palette[i % len(palette)] + "26",
                        boxmean=False,
                        marker_size=2,
                        line_width=1.5,
                    ))
                fig.update_layout(
                    title="Salario por modalidad de trabajo",
                    showlegend=False,
                    **CHART_LAYOUT,
                )
                fig.update_xaxes(showgrid=False)
                fig.update_yaxes(tickprefix="$", **GRID_STYLE)
                chart(fig)

        # Salary by experience
        st.markdown('<div class="section-title">Salario vs. Experiencia</div>', unsafe_allow_html=True)
        if "YearsCodePro" in dff.columns:
            exp_sal = dff[dff["YearsCodePro"].notna() & dff["Salary"].notna()].copy()
            exp_sal["Exp_bucket"] = pd.cut(
                exp_sal["YearsCodePro"],
                bins=[0, 2, 5, 10, 15, 20, 30, 51],
                labels=["0–2", "3–5", "6–10", "11–15", "16–20", "21–30", "30+"],
            )
            exp_med = exp_sal.groupby("Exp_bucket", observed=True)["Salary"].median().reset_index()
            exp_med.columns = ["Experiencia", "Salario mediano"]

            fig = go.Figure(go.Bar(
                x=exp_med["Experiencia"].astype(str),
                y=exp_med["Salario mediano"],
                marker_color=COLORS["primary"],
                marker_line_width=0,
                text=exp_med["Salario mediano"].apply(lambda x: f"${x/1000:.0f}K"),
                textposition="outside",
                textfont=dict(color=COLORS["text"], size=11),
            ))
            fig.update_layout(title="Salario mediano por años de experiencia profesional", **CHART_LAYOUT)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(tickprefix="$", **GRID_STYLE)
            chart(fig)

        # Salary by role
        st.markdown('<div class="section-title">Salario por rol</div>', unsafe_allow_html=True)
        if "DevType" in dff.columns:
            role_sal = (
                dff[dff["Salary"].notna() & dff["DevType"].notna()]
                .assign(DevType=lambda d: d["DevType"].str.split(";"))
                .explode("DevType")
                .assign(DevType=lambda d: d["DevType"].str.strip())
                .groupby("DevType")["Salary"]
                .agg(median="median", count="count")
                .query("count >= 30")
                .sort_values("median", ascending=True)
                .tail(15)
                .reset_index()
            )
            fig = go.Figure(go.Bar(
                x=role_sal["median"],
                y=role_sal["DevType"],
                orientation="h",
                marker_color=COLORS["accent"],
                marker_line_width=0,
                text=role_sal["median"].apply(lambda x: f"${x/1000:.0f}K"),
                textposition="outside",
                textfont=dict(color=COLORS["text"], size=10),
            ))
            fig.update_layout(title="Salario mediano por rol (Top 15)", **CHART_LAYOUT,
                              yaxis=dict(autorange="reversed"))
            fig.update_xaxes(tickprefix="$", **GRID_STYLE)
            fig.update_yaxes(showgrid=False)
            chart(fig)

            top_role = role_sal.iloc[-1]
            insight(f'El rol mejor pagado es <strong>{top_role["DevType"]}</strong> con un salario mediano de <span class="accent-amber">${top_role["median"]/1000:.0f}K USD</span>.')


# ═══════════════════════════════════════════════════════════
# TAB 3 — Tecnologías
# ═══════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-title">Lenguajes de programación más usados</div>', unsafe_allow_html=True)

    if "LanguageHaveWorkedWith" in dff.columns:
        lang = dff["LanguageHaveWorkedWith"].dropna().str.split(";").explode().str.strip()
        lang_counts = lang.value_counts().head(15).reset_index()
        lang_counts.columns = ["Lenguaje", "Uso"]

        fig = go.Figure(go.Bar(
            x=lang_counts["Lenguaje"],
            y=lang_counts["Uso"],
            marker_color=COLORS["primary"],
            marker_line_width=0,
            text=lang_counts["Uso"],
            textposition="outside",
            textfont=dict(size=10),
        ))
        fig.update_layout(title="Top 15 lenguajes de programación", **CHART_LAYOUT)
        fig.update_xaxes(tickangle=-35, showgrid=False)
        fig.update_yaxes(**GRID_STYLE)
        chart(fig)

        top_lang = lang_counts.iloc[0]["Lenguaje"]
        top_pct = lang_counts.iloc[0]["Uso"] / len(dff[dff["LanguageHaveWorkedWith"].notna()]) * 100
        insight(f'<span class="accent-blue">{top_lang}</span> es el lenguaje más popular con <strong>{top_pct:.1f}%</strong> de los encuestados reportando haberlo usado.')

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Bases de datos</div>', unsafe_allow_html=True)
        if "DatabaseHaveWorkedWith" in dff.columns:
            db = dff["DatabaseHaveWorkedWith"].dropna().str.split(";").explode().str.strip()
            db_counts = db.value_counts().head(10).reset_index()
            db_counts.columns = ["Base de datos", "Uso"]
            fig = go.Figure(go.Bar(
                x=db_counts["Uso"],
                y=db_counts["Base de datos"],
                orientation="h",
                marker_color=COLORS["success"],
                marker_line_width=0,
            ))
            fig.update_layout(title="Top 10 bases de datos", **CHART_LAYOUT,
                              yaxis=dict(autorange="reversed"))
            fig.update_xaxes(**GRID_STYLE)
            fig.update_yaxes(showgrid=False)
            chart(fig)

    with col2:
        st.markdown('<div class="section-title">Frameworks web</div>', unsafe_allow_html=True)
        if "WebframeHaveWorkedWith" in dff.columns:
            fw = dff["WebframeHaveWorkedWith"].dropna().str.split(";").explode().str.strip()
            fw_counts = fw.value_counts().head(10).reset_index()
            fw_counts.columns = ["Framework", "Uso"]
            fig = go.Figure(go.Bar(
                x=fw_counts["Uso"],
                y=fw_counts["Framework"],
                orientation="h",
                marker_color="#8B5CF6",
                marker_line_width=0,
            ))
            fig.update_layout(title="Top 10 frameworks web", **CHART_LAYOUT,
                              yaxis=dict(autorange="reversed"))
            fig.update_xaxes(**GRID_STYLE)
            fig.update_yaxes(showgrid=False)
            chart(fig)

    # Tech salary correlation
    st.markdown('<div class="section-title">Salario por lenguaje (mediana)</div>', unsafe_allow_html=True)
    if "LanguageHaveWorkedWith" in dff.columns and "Salary" in dff.columns:
        lang_sal = (
            dff[dff["Salary"].notna() & dff["LanguageHaveWorkedWith"].notna()]
            .assign(Lang=lambda d: d["LanguageHaveWorkedWith"].str.split(";"))
            .explode("Lang")
            .assign(Lang=lambda d: d["Lang"].str.strip())
            .groupby("Lang")["Salary"]
            .agg(median="median", count="count")
            .query("count >= 50")
            .sort_values("median", ascending=False)
            .head(12)
            .reset_index()
        )
        fig = go.Figure(go.Bar(
            x=lang_sal["Lang"],
            y=lang_sal["median"],
            marker_color=COLORS["accent"],
            marker_line_width=0,
            text=lang_sal["median"].apply(lambda x: f"${x/1000:.0f}K"),
            textposition="outside",
            textfont=dict(size=10),
        ))
        fig.update_layout(title="Salario mediano por lenguaje principal (USD)", **CHART_LAYOUT)
        fig.update_xaxes(tickangle=-30, showgrid=False)
        fig.update_yaxes(tickprefix="$", **GRID_STYLE)
        chart(fig)


# ═══════════════════════════════════════════════════════════
# TAB 4 — Geografía
# ═══════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-title">Distribución mundial de respuestas</div>', unsafe_allow_html=True)

    if "Country" in dff.columns:
        try:
            import pycountry
            def to_iso3(name):
                try:
                    return pycountry.countries.lookup(name).alpha_3
                except Exception:
                    manual = {
                        "United States of America": "USA",
                        "United Kingdom of Great Britain and Northern Ireland": "GBR",
                        "Iran, Islamic Republic of...": "IRN",
                        "Republic of Korea": "KOR",
                        "Bolivia": "BOL",
                        "Venezuela, Bolivarian Republic of...": "VEN",
                        "Taiwan": "TWN",
                        "Viet Nam": "VNM",
                        "Syrian Arab Republic": "SYR",
                        "Russian Federation": "RUS",
                    }
                    return manual.get(name)

            country_counts = dff["Country"].value_counts().reset_index()
            country_counts.columns = ["País", "Respuestas"]
            country_counts["ISO3"] = country_counts["País"].apply(to_iso3)
            country_counts = country_counts.dropna(subset=["ISO3"])

            fig = go.Figure(go.Choropleth(
                locations=country_counts["ISO3"],
                z=country_counts["Respuestas"],
                text=country_counts["País"],
                colorscale=[[0, "#0f2040"], [0.3, "#1E40AF"], [0.7, "#3B82F6"], [1, "#93C5FD"]],
                marker_line_color="#0a1628",
                marker_line_width=0.5,
                colorbar=dict(
                    title=dict(text="Respuestas", font=dict(color=COLORS["text"])),
                    bgcolor="rgba(0,0,0,0)",
                    tickfont=dict(color=COLORS["text"]),
                ),
            ))
            fig.update_layout(
                **CHART_LAYOUT,
                geo=dict(
                    showframe=False,
                    showcoastlines=True,
                    coastlinecolor="rgba(59,130,246,0.3)",
                    projection_type="natural earth",
                    bgcolor="rgba(0,0,0,0)",
                    showland=True, landcolor="#0d1d3a",
                    showocean=True, oceancolor="#06101e",
                    showcountries=True, countrycolor="rgba(59,130,246,0.15)",
                ),
                height=420,
            )
            chart(fig)

        except ImportError:
            st.warning("Instala `pycountry` para ver el mapa: `pip install pycountry`")

        # Top countries bar
        st.markdown('<div class="section-title">Top 15 países por respuestas</div>', unsafe_allow_html=True)
        top_countries = dff["Country"].value_counts().head(15).reset_index()
        top_countries.columns = ["País", "Respuestas"]
        fig = go.Figure(go.Bar(
            x=top_countries["Respuestas"],
            y=top_countries["País"],
            orientation="h",
            marker_color=COLORS["primary"],
            marker_line_width=0,
            text=top_countries["Respuestas"].apply(lambda x: f"{x:,}"),
            textposition="outside",
            textfont=dict(color=COLORS["text"], size=10),
        ))
        fig.update_layout(title="Participación por país", **CHART_LAYOUT,
                          yaxis=dict(autorange="reversed"))
        fig.update_xaxes(**GRID_STYLE)
        fig.update_yaxes(showgrid=False)
        chart(fig)

        # Salary by country
        if "Salary" in dff.columns:
            st.markdown('<div class="section-title">Salario mediano por país (Top 15)</div>', unsafe_allow_html=True)
            sal_country = (
                dff[dff["Salary"].notna() & dff["Country"].notna()]
                .groupby("Country")["Salary"]
                .agg(median="median", count="count")
                .query("count >= 20")
                .sort_values("median", ascending=False)
                .head(15)
                .reset_index()
            )
            fig = go.Figure(go.Bar(
                x=sal_country["median"],
                y=sal_country["Country"],
                orientation="h",
                marker_color=COLORS["accent"],
                marker_line_width=0,
                text=sal_country["median"].apply(lambda x: f"${x/1000:.0f}K"),
                textposition="outside",
                textfont=dict(color=COLORS["text"], size=10),
            ))
            fig.update_layout(title="Salario mediano por país (USD)", **CHART_LAYOUT,
                              yaxis=dict(autorange="reversed"))
            fig.update_xaxes(tickprefix="$", **GRID_STYLE)
            fig.update_yaxes(showgrid=False)
            chart(fig)

            top_country = sal_country.iloc[0]
            insight(f'<span class="accent-amber">{top_country["Country"]}</span> lidera con un salario mediano de <strong>${top_country["median"]/1000:.0f}K USD</strong>.')


# ═══════════════════════════════════════════════════════════
# TAB 5 — Educación & Experiencia
# ═══════════════════════════════════════════════════════════
with tabs[4]:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Nivel educativo</div>', unsafe_allow_html=True)
        if "EdLevel" in dff.columns:
            ed_map = {
                "Bachelor's degree (B.A., B.S., B.Eng., etc.)": "Licenciatura",
                "Master's degree (M.A., M.S., M.Eng., MBA, etc.)": "Maestría",
                "Some college/university study without earning a degree": "Sin título",
                "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)": "Secundaria",
                "Associate degree (A.A., A.S., etc.)": "Técnico",
                "Professional degree (JD, MD, Ph.D, Ed.D, etc.)": "Doctorado/Prof.",
                "Primary/elementary school": "Primaria",
                "Something else": "Otro",
            }
            # Map using flexible partial matching
            def map_ed(val):
                v = str(val).lower()
                if "bachelor" in v:           return "Licenciatura"
                if "master" in v:             return "Maestría"
                if "without earning" in v or "some college" in v or "no degree" in v: return "Sin título"
                if "secondary" in v or "high school" in v: return "Secundaria"
                if "associate" in v:          return "Técnico"
                if "professional" in v or "ph.d" in v or "doctoral" in v or "doctor" in v: return "Doctorado/Prof."
                if "primary" in v or "elementary" in v: return "Primaria"
                return "Otro"
            ed_series = dff["EdLevel"].map(map_ed)
            ed = ed_series.value_counts().reset_index()
            ed.columns = ["Nivel", "Respuestas"]
            total_ed = ed["Respuestas"].sum()
            ed["Pct"] = ed["Respuestas"] / total_ed * 100
            # Merge categories < 2% into "Otro"
            otros = ed[ed["Pct"] < 2]["Respuestas"].sum()
            ed = ed[ed["Pct"] >= 2].copy()
            if otros > 0:
                otro_row = pd.DataFrame([{"Nivel": "Otros", "Respuestas": otros, "Pct": otros/total_ed*100}])
                ed = pd.concat([ed, otro_row], ignore_index=True)

            palette = [COLORS["primary"], COLORS["accent"], COLORS["success"],
                       "#8B5CF6", "#EC4899", "#06B6D4", "#84CC16", "#6B7280"]
            fig = go.Figure(go.Pie(
                labels=ed["Nivel"],
                values=ed["Respuestas"],
                hole=0.52,
                marker=dict(colors=palette[:len(ed)], line=dict(color=COLORS["bg"], width=3)),
                textinfo="percent",
                textposition="inside",
                insidetextorientation="radial",
                textfont=dict(size=11, color="white"),
                hovertemplate="<b>%{label}</b><br>%{value:,} respuestas<br>%{percent}<extra></extra>",
            ))
            fig.update_layout(
                title="Distribución educativa",
                **CHART_LAYOUT,
                legend=dict(
                    orientation="v",
                    x=1.02, y=0.5,
                    xanchor="left",
                    font=dict(size=11),
                ),
                height=340,
            )
            chart(fig)

    with col2:
        st.markdown('<div class="section-title">Años de experiencia profesional</div>', unsafe_allow_html=True)
        if "YearsCodePro" in dff.columns and dff["YearsCodePro"].notna().any():
            exp = dff["YearsCodePro"].dropna()
            fig = go.Figure(go.Histogram(
                x=exp, nbinsx=30,
                marker_color=COLORS["primary"],
                marker_line_color=COLORS["bg"],
                marker_line_width=0.5,
                opacity=0.85,
            ))
            fig.update_layout(title="Distribución de experiencia profesional", **CHART_LAYOUT)
            fig.update_xaxes(title="Años", **GRID_STYLE)
            fig.update_yaxes(**GRID_STYLE)
            chart(fig)

            med_exp = exp.median()
            insight(f'La experiencia mediana es de <span class="accent-blue">{med_exp:.0f} años</span>. La mayoría de desarrolladores tienen entre 3 y 10 años de experiencia profesional.')
        else:
            st.markdown("""
            <div class="insight-box" style="border-left-color:#D97706;">
                ⚠️ El dataset no incluye la columna de experiencia profesional con ese nombre.<br>
                <small style="opacity:0.6;">Columnas disponibles con "year": revisa el CSV.</small>
            </div>
            """, unsafe_allow_html=True)
            # Show available year-related columns for debugging
            year_cols = [c for c in df.columns if "year" in c.lower() or "exp" in c.lower() or "code" in c.lower()]
            if year_cols:
                st.caption(f"Columnas relacionadas encontradas: `{'`, `'.join(year_cols[:8])}`")

    # Education vs Salary
    st.markdown('<div class="section-title">Salario por nivel educativo</div>', unsafe_allow_html=True)
    _ed_map = {
        "Bachelor's degree (B.A., B.S., B.Eng., etc.)": "Licenciatura",
        "Master's degree (M.A., M.S., M.Eng., MBA, etc.)": "Maestría",
        "Some college/university study without earning a degree": "Sin título",
        "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)": "Secundaria",
        "Associate degree (A.A., A.S., etc.)": "Técnico",
        "Professional degree (JD, MD, Ph.D, Ed.D, etc.)": "Doctorado/Prof.",
        "Primary/elementary school": "Primaria",
        "Something else": "Otro",
    }
    if "EdLevel" in dff.columns and "Salary" in dff.columns:
        ed_sal = (
            dff[dff["Salary"].notna() & dff["EdLevel"].notna()]
            .copy()
        )
        def _map_ed(val):
            v = str(val).lower()
            if "bachelor" in v:           return "Licenciatura"
            if "master" in v:             return "Maestría"
            if "without earning" in v or "some college" in v or "no degree" in v: return "Sin título"
            if "secondary" in v or "high school" in v: return "Secundaria"
            if "associate" in v:          return "Técnico"
            if "professional" in v or "ph.d" in v or "doctoral" in v or "doctor" in v: return "Doctorado/Prof."
            if "primary" in v or "elementary" in v: return "Primaria"
            return "Otro"
        ed_sal["EdLevel"] = ed_sal["EdLevel"].map(_map_ed)
        ed_sal_grouped = (
            ed_sal.groupby("EdLevel")["Salary"]
            .agg(median="median", count="count")
            .query("count >= 20")
            .sort_values("median", ascending=True)
            .reset_index()
        )
        fig = go.Figure(go.Bar(
            x=ed_sal_grouped["median"],
            y=ed_sal_grouped["EdLevel"],
            orientation="h",
            marker_color=COLORS["primary"],
            marker_line_width=0,
            text=ed_sal_grouped["median"].apply(lambda x: f"${x/1000:.0f}K"),
            textposition="outside",
            textfont=dict(color=COLORS["text"], size=11),
        ))
        fig.update_layout(title="Salario mediano por nivel educativo (USD)", **CHART_LAYOUT,
                          yaxis=dict(autorange="reversed"))
        fig.update_xaxes(tickprefix="$", **GRID_STYLE)
        fig.update_yaxes(showgrid=False)
        chart(fig)

    # Age distribution
    st.markdown('<div class="section-title">Distribución por edad</div>', unsafe_allow_html=True)
    if "Age" in dff.columns:
        age = dff["Age"].value_counts().reset_index()
        age.columns = ["Rango", "Respuestas"]
        age_order = [
            "Under 18 years old", "18-24 years old", "25-34 years old",
            "35-44 years old", "45-54 years old", "55-64 years old",
            "65 years or older", "Prefer not to say",
        ]
        age["Rango"] = pd.Categorical(age["Rango"], categories=age_order, ordered=True)
        age = age.sort_values("Rango")
        fig = go.Figure(go.Bar(
            x=age["Rango"].astype(str),
            y=age["Respuestas"],
            marker_color=COLORS["primary"],
            marker_line_width=0,
            text=age["Respuestas"],
            textposition="outside",
            textfont=dict(size=10),
        ))
        fig.update_layout(title="Distribución por grupo de edad", **CHART_LAYOUT)
        fig.update_xaxes(tickangle=-25, showgrid=False)
        fig.update_yaxes(**GRID_STYLE)
        chart(fig)

        peak_age = age.loc[age["Respuestas"].idxmax(), "Rango"]
        insight(f'El grupo de edad más representado es <span class="accent-blue">{peak_age}</span>, confirmando que el sector tech sigue siendo dominado por jóvenes profesionales.')


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<hr/>
<div style="text-align:center; color:rgba(226,232,240,0.3); font-size:0.75rem; padding:0.5rem 0 1rem 0;">
    Datos: Stack Overflow Developer Survey 2025 · Construido con Streamlit + Plotly
</div>
""", unsafe_allow_html=True)