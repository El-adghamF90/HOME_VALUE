import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


# ------------------------------------------------------------
# Page
# ------------------------------------------------------------
st.set_page_config(
    page_title="HomeValue AI",
    page_icon="⌂",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------
ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "backend" / "models" / "house_price.pkl"
LOCATIONS_PATH = ROOT / "backend" / "app" / "locations.json"


# ------------------------------------------------------------
# Load model + locations
# ------------------------------------------------------------
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_locations():
    with open(LOCATIONS_PATH, "r", encoding="utf-8") as f:
        return sorted(set(json.load(f)))


model = load_model()
locations = load_locations()


# ------------------------------------------------------------
# Global visual system
# ------------------------------------------------------------
st.html(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

        .stApp {
            background:
                radial-gradient(circle at 15% 8%, rgba(255, 107, 53, .08), transparent 28%),
                radial-gradient(circle at 85% 20%, rgba(124, 58, 237, .08), transparent 30%),
                #06060b;
            color: #f7f7f5;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stToolbar"] {
            display: none;
        }

        .block-container {
            max-width: 1280px;
            padding-top: 1.1rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3, p, label, div, span {
            font-family: "DM Sans", sans-serif;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(255,255,255,.035);
            border: 1px solid rgba(255,255,255,.10);
            border-radius: 24px;
            box-shadow: 0 25px 80px rgba(0,0,0,.28);
        }

        div[data-baseweb="select"] > div,
        div[data-testid="stNumberInput"] input {
            background: rgba(255,255,255,.055) !important;
            border: 1px solid rgba(255,255,255,.11) !important;
            color: #f7f7f5 !important;
            border-radius: 13px !important;
        }

        div[data-baseweb="select"] span {
            color: #f7f7f5 !important;
        }

        div[data-testid="stNumberInput"] input {
            color: #f7f7f5 !important;
        }

        div[data-testid="stButton"] > button {
            min-height: 54px;
            border: 0;
            border-radius: 15px;
            background: linear-gradient(135deg, #ff7a45, #d9582f);
            color: white;
            font-weight: 700;
            letter-spacing: .01em;
            box-shadow: 0 14px 35px rgba(255, 106, 54, .20);
            transition: transform .2s ease, box-shadow .2s ease;
        }

        div[data-testid="stButton"] > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 18px 45px rgba(255, 106, 54, .30);
        }

        .section-kicker {
            font-size: .72rem;
            letter-spacing: .18em;
            text-transform: uppercase;
            color: #ff8758;
            font-weight: 700;
            margin-bottom: .35rem;
        }

        .section-title {
            font-family: "Space Grotesk", sans-serif;
            font-size: clamp(2rem, 4vw, 3.4rem);
            line-height: .98;
            font-weight: 700;
            letter-spacing: -.045em;
            margin: 0 0 .65rem;
        }

        .section-copy {
            color: #a9a9b3;
            max-width: 720px;
            font-size: 1rem;
            line-height: 1.65;
        }

        footer {
            visibility: hidden;
        }
    </style>
    """
)


# ------------------------------------------------------------
# Hero
# Custom HTML + JavaScript gives us the mouse-reactive design.
# ------------------------------------------------------------
hero_html = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden}
body{background:transparent;font-family:"DM Sans",sans-serif;color:#f7f7f5}

.hero{
    --mx:0;
    --my:0;
    position:relative;
    width:100%;
    height:620px;
    overflow:hidden;
    border:1px solid rgba(255,255,255,.10);
    border-radius:28px;
    background:
        radial-gradient(circle at 74% 22%, rgba(255,101,48,.16), transparent 23%),
        radial-gradient(circle at 18% 80%, rgba(109,72,255,.13), transparent 30%),
        linear-gradient(145deg,#090910 0%,#07070d 52%,#0b080a 100%);
    box-shadow:0 30px 90px rgba(0,0,0,.38);
}

.hero:before{
    content:"";
    position:absolute;
    inset:0;
    background:
        radial-gradient(circle at 50% 45%, transparent 0 32%, rgba(0,0,0,.38) 72%),
        linear-gradient(90deg,rgba(255,255,255,.025) 1px,transparent 1px);
    background-size:auto,80px 100%;
    pointer-events:none;
    opacity:.55;
}

.glow{
    position:absolute;
    width:330px;
    height:330px;
    border-radius:50%;
    pointer-events:none;
    background:radial-gradient(circle,rgba(255,107,53,.18),rgba(255,107,53,0) 67%);
    transform:translate(-50%,-50%);
    filter:blur(6px);
    left:72%;
    top:35%;
    transition:left .08s linear,top .08s linear;
}

.grid{
    position:absolute;
    width:180%;
    height:105%;
    left:-40%;
    top:48%;
    opacity:.58;
    background-image:
        linear-gradient(rgba(183,87,255,.28) 1px,transparent 1px),
        linear-gradient(90deg,rgba(255,91,67,.22) 1px,transparent 1px);
    background-size:58px 58px;
    transform-origin:center top;
    transform:
        perspective(620px)
        rotateX(66deg)
        translate3d(calc(var(--mx) * -38px),calc(var(--my) * -14px),0)
        scale(1.28);
    animation:gridMove 12s linear infinite;
}

@keyframes gridMove{
    from{background-position:0 0,0 0}
    to{background-position:0 116px,116px 0}
}

.horizon{
    position:absolute;
    left:0;
    right:0;
    top:47%;
    height:1px;
    background:linear-gradient(90deg,transparent,rgba(255,108,68,.55),rgba(160,95,255,.42),transparent);
    box-shadow:0 0 35px rgba(255,92,54,.18);
}

.particles{
    position:absolute;
    inset:0;
    pointer-events:none;
}

.p{
    position:absolute;
    width:3px;
    height:3px;
    border-radius:50%;
    background:#fff;
    opacity:.42;
    box-shadow:0 0 14px rgba(255,255,255,.5);
    animation:float var(--d) ease-in-out infinite alternate;
}

@keyframes float{
    from{transform:translate3d(0,0,0);opacity:.18}
    to{transform:translate3d(var(--x),var(--y),0);opacity:.7}
}

.nav{
    position:absolute;
    z-index:10;
    top:22px;
    left:24px;
    right:24px;
    height:58px;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:0 12px 0 18px;
    border:1px solid rgba(255,255,255,.13);
    background:rgba(12,12,18,.64);
    backdrop-filter:blur(18px);
    border-radius:999px;
}

.logo{
    display:flex;
    align-items:center;
    gap:10px;
    font-family:"Space Grotesk",sans-serif;
    font-weight:700;
    letter-spacing:-.03em;
}

.logo-mark{
    width:29px;
    height:29px;
    border-radius:9px;
    display:grid;
    place-items:center;
    background:linear-gradient(135deg,#ff8659,#a746ff);
    box-shadow:0 0 25px rgba(255,104,55,.25);
    font-size:15px;
}

.navlinks{
    display:flex;
    gap:26px;
    align-items:center;
}

.navlinks span{
    color:#a7a7b0;
    font-size:12px;
    letter-spacing:.08em;
    text-transform:uppercase;
}

.navlinks span:first-child{color:#fff}

.badge{
    border:1px solid rgba(255,255,255,.10);
    border-radius:999px;
    padding:9px 13px;
    color:#ddd;
    font-size:11px;
    letter-spacing:.08em;
}

.content{
    position:absolute;
    z-index:5;
    left:7%;
    top:145px;
    max-width:760px;
}

.eyebrow{
    display:flex;
    align-items:center;
    gap:11px;
    color:#a9a9b2;
    font-size:11px;
    font-weight:700;
    letter-spacing:.17em;
    text-transform:uppercase;
    margin-bottom:18px;
}

.eyebrow i{
    width:34px;
    height:1px;
    background:#ff7548;
    display:inline-block;
}

h1{
    font-family:"Space Grotesk",sans-serif;
    font-size:clamp(54px,7vw,96px);
    line-height:.89;
    letter-spacing:-.065em;
    margin:0;
    font-weight:700;
}

h1 .accent{
    background:linear-gradient(100deg,#fff 0%,#ff9a70 48%,#ff5e31 100%);
    -webkit-background-clip:text;
    background-clip:text;
    color:transparent;
}

.copy{
    max-width:560px;
    color:#a8a8b2;
    line-height:1.65;
    font-size:15px;
    margin:27px 0 25px;
}

.cta{
    display:inline-flex;
    align-items:center;
    gap:13px;
    padding:14px 18px;
    border-radius:999px;
    color:#fff;
    text-decoration:none;
    font-size:12px;
    font-weight:700;
    letter-spacing:.05em;
    text-transform:uppercase;
    background:#f36d40;
    box-shadow:0 15px 40px rgba(243,109,64,.22);
}

.cta b{
    width:25px;
    height:25px;
    border-radius:50%;
    display:grid;
    place-items:center;
    background:rgba(0,0,0,.18);
}

.side-note{
    position:absolute;
    right:5.5%;
    top:48%;
    width:220px;
    padding:16px;
    border-left:1px solid rgba(255,255,255,.13);
    color:#777783;
    font-size:11px;
    line-height:1.55;
}

.side-note strong{
    color:#ddd;
    font-size:12px;
}

.bottom{
    position:absolute;
    z-index:6;
    left:7%;
    right:7%;
    bottom:22px;
    display:flex;
    justify-content:space-between;
    align-items:end;
}

.statline{
    display:flex;
    gap:28px;
}

.stat strong{
    display:block;
    font-family:"Space Grotesk",sans-serif;
    color:#f5f5f5;
    font-size:18px;
}

.stat span{
    color:#70707c;
    font-size:10px;
    letter-spacing:.08em;
    text-transform:uppercase;
}

.scroll{
    color:#666673;
    font-size:10px;
    letter-spacing:.16em;
    text-transform:uppercase;
}

@media(max-width:760px){
    .hero{height:650px}
    .navlinks{display:none}
    .content{left:7%;right:7%;top:135px}
    h1{font-size:58px}
    .side-note{display:none}
    .statline{gap:15px}
    .stat strong{font-size:15px}
    .badge{display:none}
}
</style>
</head>

<body>
<div class="hero" id="hero">
    <div class="glow" id="glow"></div>
    <div class="grid"></div>
    <div class="horizon"></div>
    <div class="particles" id="particles"></div>

    <div class="nav">
        <div class="logo">
            <div class="logo-mark">⌂</div>
            <div>HOMEVALUE<span style="color:#ff7448">.AI</span></div>
        </div>

        <div class="navlinks">
            <span>Home</span>
            <span>Predict</span>
            <span>Model</span>
            <span>About</span>
        </div>

        <div class="badge">ML / REAL ESTATE</div>
    </div>

    <div class="content">
        <div class="eyebrow">
            <i></i> AI-POWERED PROPERTY VALUATION
        </div>

        <h1>
            Know the value<br>
            of your <span class="accent">home.</span>
        </h1>

        <div class="copy">
            A machine-learning valuation experience built from real property data.
            Enter the details of a home and get an instant estimated market value.
        </div>

        <a class="cta" href="#predict" onclick="
    event.preventDefault();
    try {
        const target = window.parent.document.getElementById('predict');
        if (target) {
            target.scrollIntoView({behavior:'smooth', block:'start'});
        } else {
            window.parent.location.hash = 'predict';
        }
    } catch (e) {
        window.parent.location.hash = 'predict';
    }
    return false;
">
            START PREDICTION <b>↘</b>
        </a>
    </div>

    <div class="side-note">
        <strong>THE MODEL</strong><br>
        Random Forest regression reads area, floor, bathrooms, balcony,
        location and transaction details to estimate property value.
    </div>

    <div class="bottom">
        <div class="statline">
            <div class="stat">
                <strong>82.6%</strong>
                <span>Current R²</span>
            </div>
            <div class="stat">
                <strong>AI</strong>
                <span>Prediction engine</span>
            </div>
            <div class="stat">
                <strong>9</strong>
                <span>Property features</span>
            </div>
        </div>

        <div class="scroll"></div>
    </div>
</div>

<script>
const hero = document.getElementById("hero");
const glow = document.getElementById("glow");
const particles = document.getElementById("particles");

for (let i = 0; i < 42; i++) {
    const p = document.createElement("span");
    p.className = "p";
    p.style.left = (Math.random() * 100) + "%";
    p.style.top = (Math.random() * 100) + "%";
    p.style.setProperty("--d", (3 + Math.random() * 6) + "s");
    p.style.setProperty("--x", (-15 + Math.random() * 30) + "px");
    p.style.setProperty("--y", (-18 + Math.random() * 36) + "px");
    p.style.animationDelay = (-Math.random() * 6) + "s";
    particles.appendChild(p);
}

hero.addEventListener("mousemove", (e) => {
    const r = hero.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width;
    const y = (e.clientY - r.top) / r.height;
    const mx = (x - 0.5) * 2;
    const my = (y - 0.5) * 2;

    hero.style.setProperty("--mx", mx.toFixed(3));
    hero.style.setProperty("--my", my.toFixed(3));
    glow.style.left = (x * 100) + "%";
    glow.style.top = (y * 100) + "%";
});

hero.addEventListener("mouseleave", () => {
    hero.style.setProperty("--mx", "0");
    hero.style.setProperty("--my", "0");
    glow.style.left = "72%";
    glow.style.top = "35%";
});
</script>
</body>
</html>
"""

components.html(hero_html, height=650, scrolling=False)


# ------------------------------------------------------------
# Prediction section
# ------------------------------------------------------------
st.html('<div id="predict" style="position:relative;top:-20px;height:1px;"></div>')

st.html(
    """
    <div style="height:30px"></div>

    <div style="margin: 8px 0 20px;">
        <div class="section-kicker">01 / PROPERTY DATA</div>
        <div class="section-title">Let's estimate the property.</div>
        <div class="section-copy">
            Give the model the same kind of information used during training.
            The interface is simple; the prediction happens underneath.
        </div>
    </div>
    """
)

with st.container(border=True):
    st.markdown("### Property profile")

    c1, c2, c3 = st.columns(3)

    with c1:
        location = st.selectbox(
            "Location",
            locations,
            index=0,
            help="Choose a location from the trained location list.",
        )

    with c2:
        carpet_area_sqft = st.number_input(
            "Carpet area (sq ft)",
            min_value=100,
            max_value=20000,
            value=1200,
            step=50,
        )

    with c3:
        floor_num = st.number_input(
            "Floor number",
            min_value=0,
            max_value=100,
            value=5,
            step=1,
        )

    c4, c5, c6 = st.columns(3)

    with c4:
        bathroom = st.number_input(
            "Bathrooms",
            min_value=1,
            max_value=15,
            value=2,
            step=1,
        )

    with c5:
        balcony = st.number_input(
            "Balconies",
            min_value=0,
            max_value=10,
            value=1,
            step=1,
        )

    with c6:
        furnishing = st.selectbox(
            "Furnishing",
            ["Furnished", "Semi-Furnished", "Unfurnished"],
        )

    c7, c8, c9 = st.columns(3)

    with c7:
        transaction = st.selectbox(
            "Transaction",
            ["New Property", "Resale"],
        )

    with c8:
        ownership = st.selectbox(
            "Ownership",
            [
                "Freehold",
                "Leasehold",
                "Power of Attorney",
                "Co-operative Society",
            ],
        )

    with c9:
        facing = st.selectbox(
            "Facing",
            [
                "East",
                "West",
                "North",
                "South",
                "North-East",
                "North-West",
                "South-East",
                "South-West",
            ],
        )

    st.html("<div style='height:8px'></div>")

    predict = st.button(
        "ESTIMATE PROPERTY VALUE  →",
        use_container_width=True,
    )


# ------------------------------------------------------------
# Prediction
# ------------------------------------------------------------
if predict:
    # Keep these names exactly aligned with the existing
    # FastAPI preprocessing layer.
    model_location = location if location in set(locations) else "other"

    input_df = pd.DataFrame(
        [
            {
                "carpet_area_sqft": carpet_area_sqft,
                "floor_num": floor_num,
                "bathroom": bathroom,
                "balcony": balcony,
                "location_grouped": model_location,
                "Furnishing": furnishing,
                "Transaction": transaction,
                "Ownership": ownership,
                "facing": facing,
            }
        ]
    )

    try:
        prediction = float(model.predict(input_df)[0])
        prediction = max(prediction, 0)
        formatted = f"₹ {prediction:,.0f}"

        result_html = f"""
        <!doctype html>
        <html>
        <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

            *{{box-sizing:border-box}}
            html,body{{margin:0;background:transparent}}

            .result{{
                position:relative;
                overflow:hidden;
                min-height:245px;
                padding:30px;
                border-radius:25px;
                border:1px solid rgba(255,255,255,.12);
                background:
                    radial-gradient(circle at 82% 20%,rgba(255,104,55,.22),transparent 25%),
                    linear-gradient(135deg,#111119,#0b0b11);
                color:#f7f7f5;
                font-family:"DM Sans",sans-serif;
                box-shadow:0 25px 70px rgba(0,0,0,.32);
            }}

            .result:after{{
                content:"";
                position:absolute;
                width:260px;
                height:260px;
                right:-100px;
                bottom:-160px;
                border-radius:50%;
                border:1px solid rgba(255,115,69,.22);
                box-shadow:
                    0 0 0 35px rgba(255,115,69,.035),
                    0 0 0 70px rgba(255,115,69,.02);
            }}

            .label{{
                font-size:10px;
                letter-spacing:.18em;
                text-transform:uppercase;
                color:#ff8a5e;
                font-weight:700;
            }}

            .price{{
                margin-top:17px;
                font-family:"Space Grotesk",sans-serif;
                font-size:clamp(42px,7vw,76px);
                line-height:1;
                letter-spacing:-.055em;
                font-weight:700;
                background:linear-gradient(100deg,#fff,#ff9a72);
                -webkit-background-clip:text;
                background-clip:text;
                color:transparent;
            }}

            .desc{{
                color:#91919d;
                margin-top:13px;
                font-size:13px;
            }}

            .pill{{
                display:inline-flex;
                margin-top:20px;
                padding:8px 11px;
                border-radius:999px;
                background:rgba(255,255,255,.055);
                border:1px solid rgba(255,255,255,.08);
                color:#bdbdc7;
                font-size:10px;
                letter-spacing:.08em;
                text-transform:uppercase;
            }}
        </style>
        </head>

        <body>
            <div class="result">
                <div class="label">02 / AI VALUATION · NEW ESTIMATE</div>
                <div class="price">{formatted}</div>
                <div class="desc">
                    Estimated property value based on the details you entered.
                    This is a model estimate, not an official market appraisal.
                </div>
                <div class="pill">Random Forest · Instant prediction</div>
            </div>
        </body>
        </html>
        """

        components.html(result_html, height=270, scrolling=False)

    except Exception as exc:
        st.error(
            "The prediction could not be generated. "
            "This usually means one of the selected categorical values "
            "does not match the categories used when the model was trained."
        )
        st.exception(exc)


# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------
st.html(
    """
    <div style="height:38px"></div>

    <div style="
        padding:25px 0 5px;
        border-top:1px solid rgba(255,255,255,.08);
        color:#777782;
        font-size:12px;
        line-height:1.7;">
        <strong style="color:#d9d9de;">HOMEVALUE.AI</strong>
        &nbsp;·&nbsp; Machine Learning House Price Prediction
        <br>
        Built as an interactive Streamlit interface around the trained regression model.
    </div>
    """
)
