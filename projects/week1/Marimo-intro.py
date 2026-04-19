# Marimo-intro.py

import marimo

__generated_with = "0.19.4"
app = marimo.App(css_file="style3.css")


@app.cell
def _():
    import marimo as mo
    from marimo import ui
    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Hi! I am Balmee Hunumunt
    **2nd year BSc (Hons) Computer Science, University of the Arts London**
    📍 London, UK

    **📧** Albertbh04@outlook.com
    **📞** 07412 732178
    **🔗** [LinkedIn](https://www.linkedin.com/in/balmee-hunumunt-87080429a/) | [GitHub](https://github.com/Balmee)

    ---
    ### Welcome to my Interactive CV
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## My Education & Project Timeline
    """)
    return


@app.cell
def _(mo):
    yearS = mo.ui.slider(2021, 2025, value=2021, label="Select Year")
    yearS
    return (yearS,)


@app.cell
def _(mo, yearS):
    year = yearS.value

    if year == 2021:
        contentS = mo.md("""
        <h3>🎓 Finishing GCSE's & Starting A-levels (2021)</h3>
        <p>The Ravensbourne School.</p>
        <p>Learning Blender and Unity on the side for fun.</p>
        """)
    elif year == 2022:
        contentS = mo.md("""
        <h3>💻 Virtual Work Experience – Fujitsu (2022)</h3>
        <p>Explored smart cities and cybersecurity.</p>
        <p>Strengthened interest in real-world applications of computing.</p>
        """)
    elif year == 2023:
        contentS = mo.md("""
        <h3>🎬 Finishing A-levels & Starting BSc Computer Science at UAL (2023)</h3>
        <p>Finished A-levels at The Ravensbourne School.</p>
        <p>interset in animation and game design turns to interest in computer science.</p>
        """)
    elif year == 2024:
        contentS = mo.md("""
        <h3>🌱 Completed Year 1 (2024)</h3>
        <p>ESP8266-based automated irrigation system.</p>
        <p>Integrated MQTT, Firebase, and mobile dashboard.</p>
        <p>Full-stack movie database app.</p>
        <p> Integrating TMDB API with Flask backend and Astro/React frontend.</p>
        """)

    else:
        contentS = mo.md("""
        <h3>🌱 Year 2 Start and Applting to Internships (2025)</h3>
        <p>Starting Year 2 and also attemtping to learn more on game creation.</p>
        <p>Applying to Summer Internships.</p>
        """)



    contentS
    return (year,)


@app.cell
def _(mo, year, yearS):
    import micropip                  # Used from Pyodide which is used in browser toinstall pure Python packages dynamically using micropip,
    await micropip.install("plotly") # This case being plotly
    import plotly.graph_objects as go0

    years = yearS.value

    # Interest levels per year (percentages)
    interest_data = {
        2021: {"Computer Science": 10, "Other Academia": 90},
        2022: {"Computer Science": 30, "Other Academia": 70},
        2023: {"Computer Science": 65, "Other Academia": 35},
        2024: {"Computer Science": 85, "Other Academia": 15},
        2025: {"Computer Science": 95, "Other Academia": 5},
    }

    data0 = interest_data[year]

    labels = ["Computer Science", "Other Academia"]
    values = [data0[label] for label in labels]

    # Lock colours to categories
    colors = ["#1f77b4", "#ff7f0e"]  # Blue = CS, Orange = Other

    fig0 = go0.Figure(
        go0.Pie(
            labels=labels,
            values=values,
            hole=0.4,  # for a donut style
            hovertemplate="%{label}: %{value}%<extra></extra>",
        )
    )

    fig0.update_layout(
        title=f"Interest in Computer Science — {years}",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=True,
    )

    fig0.update_traces(sort=False)


    mo.ui.plotly(fig0)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    """)
    return


@app.cell
def _(mo):
    mo.Html(r"""
    <div class="projects-section" style="font-family:Arial, sans-serif; max-width:900px; margin:auto; padding:16px;">

      <h2 style="font-size:28px; font-family: 'Inter', sans-serif; font-weight:700; margin-bottom:24px; border-bottom:2px solid #333; padding-bottom:4px;">Year 1 Projects</h2>

      <div class="projects-grid" style="display:grid; gap:32px;">

        <!-- Project 1: Smart Watering System -->
        <div class="project-card" style="border:1px solid #ddd; border-radius:12px; padding:20px; box-shadow:0 2px 6px rgba(0,0,0,0.05);">
          <h3 style="font-size:22px; font-weight:700; margin-bottom:4px;">Smart Watering System</h3>
          <p style="font-size:14px; color:#555; font-style:italic; margin-bottom:12px;">
            London, UK &mdash; IoT + Mobile App | April - June 2025
          </p>
          <div style="margin-bottom:12px;">
            <video width="100%" controls preload="metadata" style="border-radius:8px;">
              <source src="https://b3pjjqqp3bfchjdh.public.blob.vercel-storage.com/smart_watering.mp4" type="video/mp4">
              Your browser does not support the video tag.
            </video>
          </div>
          <ul style="padding-left:20px; margin-top:0; line-height:1.5; color:#333; font-size:15px;">
            <li>•Conceived and constructed an IoT system using ESP8266 with soil moisture, DHT11 sensors and a pump.</li>
            <li>•Linked sensors to ThingSpeak for real-time data logging and analysis.</li>
            <li>•Designed both automatic irrigation logic and manual override through MQTT.</li>
            <li>•Produced a mobile dashboard using Expo Go, allowing remote supervision and pump control.</li>
          </ul>
        </div>

        <!-- Project 2: CineMind -->
        <div class="project-card" style="border:1px solid #ddd; border-radius:12px; padding:20px; box-shadow:0 2px 6px rgba(0,0,0,0.05);">
          <h3 style="font-size:22px; font-weight:700; margin-bottom:4px;">CineMind</h3>
          <p style="font-size:14px; color:#555; font-style:italic; margin-bottom:12px;">
            London, UK &mdash; Full-Stack Film Database App | March - June 2025
          </p>
          <div style="margin-bottom:12px;">
            <video width="100%" controls preload="metadata" style="border-radius:8px;">
              <source src="https://b3pjjqqp3bfchjdh.public.blob.vercel-storage.com/cinemind.mp4" type="video/mp4">
              Your browser does not support the video tag.
            </video>
          </div>
          <ul style="padding-left:20px; margin-top:0; line-height:1.5; color:#333; font-size:15px;">
            <li>•Built and deployed a full-stack platform using Flask backend with Astro/React frontend.</li>
            <li>•Connected TMDB API to enhance film metadata, actor biographies, and media assets.</li>
            <li>•Implemented search bar with filters (genre, language, etc.), dynamic UI updates, and responsive movie grid.</li>
            <li>•Employed SQLite and REST endpoints, tested via Jupyter Notebook.</li>
          </ul>
        </div>

        <!-- Project 3: Tamagotchi -->
        <div class="project-card" style="border:1px solid #ddd; border-radius:12px; padding:20px; box-shadow:0 2px 6px rgba(0,0,0,0.05);">
          <h3 style="font-size:22px; font-weight:700; margin-bottom:4px;">Tamagotchi</h3>
          <p style="font-size:14px; color:#555; font-style:italic; margin-bottom:12px;">
            Personal Project &mdash; Python Simulation | January 2025
          </p>
          <div style="margin-bottom:12px;">
            <video width="100%" controls preload="metadata" style="border-radius:8px;">
              <source src="https://b3pjjqqp3bfchjdh.public.blob.vercel-storage.com/tamagotchi.mp4" type="video/mp4">
              Your browser does not support the video tag.
            </video>
          </div>
          <ul style="padding-left:20px; margin-top:0; line-height:1.5; color:#333; font-size:15px;">
            <li>•Created a Python-based Tamagotchi simulation to practice OOP principles.</li>
            <li>•Implemented feeding, sleeping, and happiness mechanics for the virtual pet.</li>
            <li>•Designed a terminal-based interface with real-time state updates.</li>
            <li>•Enhanced problem-solving and Python GUI design skills through iterative testing.</li>
          </ul>
        </div>

      </div>
    </div>
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    """)
    return


@app.cell
def _(mo):

    # Skill entries with unique colors
    skills_entries = [
        {"title":"Python","desc":"Scripting, data analysis, automation","emoji":"🐍","color":"#4f46e5"},
        {"title":"JavaScript","desc":"Interactive web development, DOM logic","emoji":"🟨","color":"#f59e0b"},
        {"title":"Unity","desc":"Game design, 3D simulations, real-time rendering","emoji":"🎮","color":"#22d3ee"},
        {"title":"Flask","desc":"Backend REST APIs and services","emoji":"🌶️","color":"#ef4444"},
        {"title":"React","desc":"Dynamic user interfaces","emoji":"⚛️","color":"#06b6d4"},
        {"title":"Astro","desc":"Modern frontend framework integration","emoji":"🚀","color":"#8b5cf6"},
        {"title":"MQTT","desc":"IoT device communication","emoji":"📡","color":"#10b981"},
        {"title":"ThingSpeak","desc":"IoT data visualization","emoji":"📊","color":"#22c55e"},
        {"title":"Expo","desc":"Mobile dashboards & rapid prototyping","emoji":"📱","color":"#0ea5e9"},
        {"title":"SQLite & Docker","desc":"Persistence, containers, deployment","emoji":"🗄️","color":"#64748b"},
        {"title":"Git","desc":"Version control & collaboration","emoji":"🔧","color":"#f97316"},
        {"title":"Activities","desc":"Course Rep, Hackathons, LeetCode","emoji":"🏃","color":"#ec4899"},
    ]


    # Helper to create card HTML
    def skills_card(entry: dict) -> str:
        front = f"""
        <div class='skills-face skills-front' style='background:{entry['color']}'>
            <div class='skills-title'>{entry['emoji']} {entry['title']}</div>
            <div class='skills-desc'>What I've Gained</div>
        </div>
        """
        back = f"""
        <div class='skills-face skills-back'>
            <div class='skills-title'>{entry['emoji']} {entry['title']}</div>
            <div class='skills-desc'>{entry['desc']}</div>
        </div>
        """
        return f"<div class='skills-card'><div class='skills-inner'>{front}{back}</div></div>"

    # Render all cards
    grid_html = "<div class='skills-grid'>" + "".join(skills_card(e) for e in skills_entries) + "</div>"

    # Display
    mo.vstack(
        [mo.md("## Developed Skills"), mo.md(grid_html)]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Time Spent
    """)
    return


@app.cell
def _(mo):
    # Dropdown for week type selection
    week_type = mo.ui.dropdown(
        options=["University Week", "Holiday Week", "Term Break Week"],
        value="University Week",
        label="Select Week Type"
    )
    week_type
    return (week_type,)


@app.cell
def _(mo, week_type):
    import plotly.graph_objs as go
    import numpy as np

    # Data for each week type
    time_data_sets = {
        "University Week": {"Sleep": 56, "Study": 50, "Exercise": 5, "Leisure": 37, "Social": 20},
        "Holiday Week": {"Sleep": 50, "Study": 27, "Exercise": 10, "Leisure": 41, "Social": 40},
        "Term Break Week": {"Sleep": 56, "Study": 55, "Exercise": 10, "Leisure": 22, "Social": 25},
    }

    selected_week = week_type.value
    data = time_data_sets[selected_week]

    activities = list(data.keys())
    hours = list(data.values())

    # Bar + line chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=activities,
        y=hours,
        name="Hours (Bar)",
        marker_color='royalblue',
        hovertemplate="%{x}: %{y} hours<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=activities,
        y=hours,
        name="Hours (Line)",
        mode="lines+markers",
        line=dict(color='orange', width=3),
        marker=dict(size=8),
        hovertemplate="%{x}: %{y} hours<extra></extra>"
    ))

    fig.update_layout(
        title=f"Weekly Time Allocation — {selected_week}",
        xaxis_title="Activities",
        yaxis_title="Hours per Week",
        yaxis=dict(range=[0, max(hours) + 10]),
        margin=dict(l=70, r=20, t=50, b=40),
        height=400,
        legend=dict(orientation="h", y=-0.2)
    )

    mo.hstack([mo.ui.plotly(fig)])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## For the Future!!
    """)
    return


@app.cell
def _(mo):
    mo.mermaid("""
    graph TD
        A[2025 & 2026: Final Year & Focus] --> B[Graduate with First-Class Degree]
        A --> C[Strengthen Portfolio]
        A --> D[Apply for Graduate Roles]

        C --> C1[Full-Stack Projects]
        C --> C2[Game Design and Programming]
        C --> C3[Data Visualisation & ML]

        %% Game design branch
        C2 --> G1[Solo Game Projects]
        G1 --> G2[Publish Small Games & Prototypes]
        G2 --> G3[Join Indie Game Team]

        G3 --> G4[Work in Games Industry]

        %% Career branch
        D --> E[Graduate Software Engineer Role]

        E --> F[2026–2028: Industry Growth]
        F --> F1[Build Production Systems]
        F --> F2[Work in Agile Teams]
        F --> F3[Learn Cloud & DevOps]

        F --> G[Mid-Level Software Engineer]

        G --> H[2028+: Specialisation]
        H --> H1[AI / Data Engineering]
        H --> H2[Systems & Software]
        H --> H3[Tech Leadership]

        H --> I[Long-Term Career Stability & Impact]
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## AI Use & Acknowledgement

    AI tools were used as a development assistant throughout the creation of this interactive CV notebook.
    ChatGPT (GPT-5 family) role was focused on supporting, debugging, and refinement, rather than generating final content wholesale.

    Specifically, AI assistance helped with:
    - Structuring interactive data visualisations (bar and line, but not pie) using Plotly.
    - Improving state handling and UI logic in Marimo (sliders, dropdowns, toggles).
    - Debugging syntax, scope, and rendering issues within notebook cells.
    - Enhancing layout clarity, consistency, and readability across sections.
    - Using href videos was learnt and understood through AI to allowed to be finished initially I used local videos which I couldnt achieve by myself.

    All project descriptions, career decisions, data values, and written content reflect my own experiences, skills, and intentions.
    The final design choices, code integration, and narrative structure were manually implemented and curated by me.

    AI was used as a tool to accelerate learning and problem-solving, similar to documentation or online references, while maintaining full ownership of the work.
    """)
    return


if __name__ == "__main__":
    app.run()
