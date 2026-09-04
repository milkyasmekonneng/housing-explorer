from pathlib import Path

from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget
import pandas as pd
import plotly.express as px
import io

# ============================================================
# HOUSING DATASET (Capital Crest Real Estate Listings)
# ============================================================

raw_data = pd.DataFrame({
    "ID": [1, 2, 3, 4, 5, 6, 7, 8],
    "Location": ["Bole", "Bole", "Kazanchis", "Kazanchis", "CMC", "CMC", "Lebu", "Lebu"],
    "Type": ["Apartment", "Villa", "Apartment", "House", "Apartment", "Villa", "House", "Apartment"],
    "Price": [8500000, 18000000, 6500000, 12000000, 5500000, 15000000, 4500000, 7000000],
    "Bedrooms": [3, 5, 2, 4, 2, 4, 3, 3],
    "Bathrooms": [2, 4, 2, 3, 2, 3, 2, 2],
    "Size": [120, 350, 95, 220, 90, 280, 160, 110],
    "Lat": [8.9806, 8.9880, 9.0200, 9.0250, 9.0100, 9.0150, 8.9400, 8.9450],
    "Lon": [38.7830, 38.7900, 38.7650, 38.7700, 38.8200, 38.8250, 38.7200, 38.7250],
    "Image": [
        "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?q=80&w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1613977257363-707ba9348227?q=80&w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?q=80&w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?q=80&w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?q=80&w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?q=80&w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?q=80&w=600&auto=format&fit=crop",
        "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?q=80&w=600&auto=format&fit=crop"
    ],
    "Amenities": [
        "Backup Generator, Elevator, 24/7 Security, Balcony",
        "Private Garden, Swimming Pool, Staff Quarters, Garage",
        "Furnished, High-Speed Internet, Underground Parking",
        "Spacious Yard, Water Tank, Gated Security",
        "Modern Kitchen, Balcony, Dedicated Parking",
        "Landscaping, Solar Water Heater, Terraced Balcony",
        "Quiet Neighborhood, Perimeter Fence, Water Reservoir",
        "City View, Gym Access, Concierge, Standby Generator"
    ]
})

raw_data["Price_Per_SQM"] = raw_data["Price"] / raw_data["Size"]

# ============================================================
# USER INTERFACE
# ============================================================

app_ui = ui.page_fluid(

    # Custom Capital Crest Styling
    ui.tags.head(
        ui.tags.link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Montserrat:wght@400;500;600;700&display=swap")
    ),
    
    ui.tags.style("""
    :root {
        --primary-navy: #0B192C;
        --secondary-navy: #1E3E62;
        --accent-gold: #D4AF37;
        --light-gold: #F3E5AB;
        --bg-slate: #0F172A;
    }
    
    body {
        background: var(--bg-slate) url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070&auto=format&fit=crop') no-repeat center center fixed;
        background-size: cover;
        font-family: 'Montserrat', sans-serif;
        color: #0f172a;
        margin: 0;
    }
    .container-fluid { max-width: 1400px; margin: auto; padding: 20px; }
    
    /* Navigation Bar */
    .brand-navbar {
        background: rgba(11, 25, 44, 0.95);
        backdrop-filter: blur(12px);
        border-bottom: 2px solid var(--accent-gold);
        padding: 15px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-radius: 16px;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .brand-logo-container { display: flex; align-items: center; gap: 15px; }
    .brand-crest {
        width: 45px; height: 45px; border-radius: 50%;
        background: linear-gradient(135deg, var(--accent-gold), #9A7B1C);
        display: flex; align-items: center; justify-content: center;
        color: var(--primary-navy); font-weight: 800; font-family: 'Cinzel', serif;
        font-size: 22px; border: 2px solid var(--light-gold);
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
    }
    .brand-title {
        font-family: 'Cinzel', serif;
        color: #FFFFFF;
        font-size: 22px;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin: 0;
    }
    .brand-title span { color: var(--accent-gold); }
    .brand-slogan { color: #94A3B8; font-size: 11px; letter-spacing: 2px; text-transform: uppercase; margin: 0; }

    /* Hero Banner */
    .hero-wrapper {
        position: relative; height: 380px; overflow: hidden;
        border-radius: 20px; margin-bottom: 35px;
        border: 1px solid rgba(212, 175, 55, 0.3);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5);
    }
    .hero-slide {
        position: absolute; inset: 0; background-size: cover;
        background-position: center; opacity: 0; transition: opacity 1.2s ease-in-out;
    }
    .hero-slide.active { opacity: 1; }
    .hero-overlay {
        position: absolute; inset: 0;
        background: linear-gradient(135deg, rgba(11, 25, 44, 0.85), rgba(15, 23, 42, 0.65));
    }
    .hero-content {
        position: absolute; z-index: 10; top: 50%; left: 50px;
        transform: translateY(-50%); color: white; max-width: 700px;
    }
    .hero-content h1 {
        font-family: 'Cinzel', serif;
        font-size: 46px; font-weight: 800; margin-bottom: 12px; line-height: 1.1;
        color: #FFFFFF;
    }
    .hero-content h1 span { color: var(--accent-gold); }
    .hero-content p { font-size: 17px; color: #E2E8F0; margin-bottom: 20px; font-weight: 300; }
    .hero-badge {
        display: inline-block; background: rgba(212, 175, 55, 0.15);
        border: 1px solid var(--accent-gold); color: var(--accent-gold);
        padding: 6px 14px; border-radius: 20px; font-size: 11px;
        letter-spacing: 2px; text-transform: uppercase; font-weight: 600; margin-bottom: 15px;
    }
    .slide-dots {
        position: absolute; z-index: 20; bottom: 20px; left: 50%;
        transform: translateX(-50%); display: flex; gap: 8px;
    }
    .slide-dot {
        width: 10px; height: 10px; border-radius: 50%;
        background: rgba(255,255,255,0.4); transition: all 0.3s ease;
    }
    .slide-dot.active { width: 28px; border-radius: 10px; background: var(--accent-gold); }

    /* UI Cards & Glassmorphism */
    h2 { font-family: 'Cinzel', serif; font-size: 24px; font-weight: 700; margin-top: 35px; margin-bottom: 18px; color: var(--primary-navy); }
    .sidebar, .card {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 18px !important; padding: 22px;
        box-shadow: 0 10px 30px rgba(11, 25, 44, 0.1) !important;
    }
    .kpi-value { font-size: 28px; font-weight: 800; color: var(--secondary-navy); margin-top: 5px; }
    .kpi-label { color: #64748B; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }

    /* Property Cards */
    .property-grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
        gap: 22px; margin-bottom: 30px;
    }
    .property-card {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important; overflow: hidden;
        box-shadow: 0 8px 25px rgba(11, 25, 44, 0.08) !important;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        display: flex; flex-direction: column; justify-content: space-between;
    }
    .property-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 16px 35px rgba(11, 25, 44, 0.15) !important;
        border-color: var(--accent-gold) !important;
    }
    .property-img-box {
        height: 190px; background-size: cover; background-position: center;
        position: relative; padding: 12px; display: flex; align-items: flex-start; justify-content: space-between;
    }
    .property-type-badge {
        background: var(--primary-navy); color: var(--accent-gold);
        font-size: 11px; font-weight: 700; padding: 5px 12px; border-radius: 20px;
        letter-spacing: 1px; text-transform: uppercase; border: 1px solid var(--accent-gold);
    }
    .property-card-content { padding: 20px; }
    .property-title { font-family: 'Cinzel', serif; font-size: 18px; font-weight: 700; color: var(--primary-navy); margin: 0; }
    .property-price { color: var(--secondary-navy); font-size: 22px; font-weight: 800; margin: 8px 0; }
    .property-details span {
        font-size: 11px; color: #334155; background: #F8FAFC;
        border: 1px solid #E2E8F0; padding: 5px 8px; border-radius: 6px; margin-right: 4px; margin-bottom: 6px; display: inline-block; font-weight: 500;
    }
    .card-actions { display: flex; gap: 8px; margin-top: 14px; }
    .btn-fav { flex: 1; font-weight: 600; border-radius: 8px; font-size: 12px; }
    .btn-details {
        flex: 1; font-weight: 600; border-radius: 8px; font-size: 12px;
        background: var(--primary-navy) !important; color: white !important; border: none !important;
    }
    .btn-details:hover { background: var(--secondary-navy) !important; }

    /* Footer & About Section */
    .about-box { line-height: 1.7; font-size: 14px; color: #334155; }
    .site-footer {
        margin-top: 60px; padding: 30px; text-align: center;
        background: var(--primary-navy); color: white; border-radius: 18px;
        border-top: 2px solid var(--accent-gold);
    }
    .site-footer p { margin: 5px 0; color: #94A3B8; font-size: 13px; }
    .site-footer strong { color: var(--accent-gold); font-family: 'Cinzel', serif; }

    @media (max-width: 768px) {
        .hero-wrapper { height: 320px; }
        .hero-content { left: 20px; right: 20px; }
        .hero-content h1 { font-size: 30px; }
        .property-grid { grid-template-columns: 1fr; }
        .brand-navbar { flex-direction: column; text-align: center; gap: 10px; }
    }
    """),

    # Javascript Carousel Timer
    ui.tags.script("""
    document.addEventListener("DOMContentLoaded", function () {
        let currentSlide = 0;
        const slides = document.querySelectorAll(".hero-slide");
        const dots = document.querySelectorAll(".slide-dot");

        function showSlide(index) {
            slides.forEach(slide => slide.classList.remove("active"));
            dots.forEach(dot => dot.classList.remove("active"));
            if (slides[index]) slides[index].classList.add("active");
            if (dots[index]) dots[index].classList.add("active");
        }

        if (slides.length > 0) {
            showSlide(currentSlide);
            setInterval(function () {
                currentSlide = (currentSlide + 1) % slides.length;
                showSlide(currentSlide);
            }, 4500);
        }
    });
    """),

    # Brand Navbar (HTML wrapped to parse <span> correctly)
    ui.div(
        {"class": "brand-navbar"},
        ui.div(
            {"class": "brand-logo-container"},
            ui.div("C", class_="brand-crest"),
            ui.div(
                ui.HTML('<p class="brand-title">CAPITAL <span>CREST</span></p>'),
                ui.p("Real Estate", class_="brand-slogan")
            )
        ),
        ui.div(
            ui.span("ELEVATING CAPITAL LIVING", style="color: var(--accent-gold); font-size: 11px; letter-spacing: 2px; font-weight: 600;")
        )
    ),

    # 4-Image Brand Hero
    ui.div(
        {"class": "hero-wrapper"},
        ui.div({"class": "hero-slide active", "style": "background-image: url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1200&auto=format&fit=crop');"}),
        ui.div({"class": "hero-slide", "style": "background-image: url('https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?q=80&w=1200&auto=format&fit=crop');"}),
        ui.div({"class": "hero-slide", "style": "background-image: url('https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?q=80&w=1200&auto=format&fit=crop');"}),
        ui.div({"class": "hero-slide", "style": "background-image: url('https://images.unsplash.com/photo-1600566753376-12c8ab7fb75b?q=80&w=1200&auto=format&fit=crop');"}),
        ui.div({"class": "hero-overlay"}),
        ui.div(
            {"class": "hero-content"},
            ui.span("Exquisite Addis Ababa Residences", class_="hero-badge"),
            ui.HTML('<h1>YOUR APEX IN <span>PRIME REAL ESTATE</span></h1>'),
            ui.p("Capital Crest brings unparalleled luxury, market insight, and premium properties to discerning buyers and investors across prime districts.")
        ),
        ui.div(
            {"class": "slide-dots"},
            ui.div({"class": "slide-dot active"}),
            ui.div({"class": "slide-dot"}),
            ui.div({"class": "slide-dot"}),
            ui.div({"class": "slide-dot"})
        )
    ),

    # Dashboard Controls
    ui.layout_sidebar(
        ui.sidebar(
            ui.h3("🔎 Property Search", style="font-family:'Cinzel',serif; font-size:18px; color:var(--primary-navy);"),
            ui.input_select("location", "District Location", {"All": "All Locations", "Bole": "Bole", "Kazanchis": "Kazanchis", "CMC": "CMC", "Lebu": "Lebu"}),
            ui.input_slider("min_price", "Min Price (ETB)", min=500000, max=20000000, value=500000, step=500000),
            ui.input_slider("max_price", "Max Price (ETB)", min=500000, max=20000000, value=20000000, step=500000),
            ui.input_select("property_type", "Property Classification", {"All": "All Types", "Apartment": "Apartment", "Villa": "Villa", "House": "House"}),
            ui.hr(),
            ui.h4("⚙️ Sorting & Portfolio", style="font-family:'Cinzel',serif; font-size:16px; color:var(--primary-navy);"),
            ui.input_select("sort_by", "Order Listings By", {
                "price_asc": "Price: Low to High",
                "price_desc": "Price: High to Low",
                "sqm_asc": "Price/m²: Low to High",
                "size_desc": "Size: Largest First"
            }),
            ui.download_button("download_csv", "📥 Export Portfolio CSV", class_="btn-primary w-100", style="background:var(--primary-navy); border-color:var(--accent-gold);")
        ),

        # Overview Metrics
        ui.h2("Market Intelligence"),
        ui.layout_columns(
            ui.div({"class": "card"}, ui.h4("🏠 Active Listings"), ui.div(ui.output_text("property_count"), class_="kpi-value"), ui.p("Matching criteria", class_="kpi-label")),
            ui.div({"class": "card"}, ui.h4("💰 Average Price"), ui.div(ui.output_text("average_price"), class_="kpi-value"), ui.p("Portfolio valuation", class_="kpi-label")),
            ui.div({"class": "card"}, ui.h4("📐 Avg Price / m²"), ui.div(ui.output_text("average_sqm_price"), class_="kpi-value"), ui.p("Efficiency metric", class_="kpi-label"))
        ),

        # Map View
        ui.h2("📍 Prime Location Directory"),
        ui.div({"class": "card"}, output_widget("map_chart")),

        # Property List
        ui.h2("🏛️ Featured Capital Crest Properties"),
        ui.output_ui("property_cards"),

        # Analytical Charts
        ui.h2("📊 Market Analytics"),
        ui.layout_columns(
            ui.div({"class": "card"}, output_widget("price_chart")),
            ui.div({"class": "card"}, output_widget("size_price_chart"))
        ),

        # Mortgage Calculator
        ui.h2("🧮 Capital Crest Financing Estimator"),
        ui.div(
            {"class": "card"},
            ui.layout_columns(
                ui.input_numeric("home_price", "Property Price (ETB)", value=8500000, step=500000),
                ui.input_numeric("down_payment_pct", "Down Payment (%)", value=20, min=0, max=100, step=5),
                ui.input_numeric("interest_rate", "Annual Interest Rate (%)", value=14.5, min=1.0, max=30.0, step=0.5),
                ui.input_numeric("loan_years", "Loan Term (Years)", value=20, min=1, max=30, step=1)
            ),
            ui.hr(),
            ui.layout_columns(
                ui.div(ui.h5("Estimated Monthly Payment"), ui.div(ui.output_text("monthly_payment"), class_="kpi-value", style="color:#059669;")),
                ui.div(ui.h5("Total Loan Principal"), ui.div(ui.output_text("total_loan_amount"), class_="kpi-value", style="color:var(--secondary-navy);")),
                ui.div(ui.h5("Total Interest Payable"), ui.div(ui.output_text("total_interest"), class_="kpi-value", style="color:#d97706;"))
            )
        ),

        # Saved Favorites
        ui.h2("❤️ Saved Client Bookmarks"),
        ui.div({"class": "card"}, ui.output_table("favorites_table")),

        # About / Project Section
        ui.h2("ℹ️ About Capital Crest Real Estate"),
        ui.div(
            {"class": "card about-box"},
            ui.h4("Capital Crest Real Estate", style="font-family:'Cinzel',serif; color:var(--primary-navy);"),
            ui.p("Capital Crest Real Estate is a premier real estate platform specializing in high-value residential properties and investment developments across Addis Ababa's most sought-after neighborhoods."),
            ui.p("Our interactive intelligence dashboard enables buyers, sellers, and foreign investors to analyze real-time market data, map prime locations, estimate financing obligations, and curate tailored property portfolios.")
        )
    ),

    # Site Footer
    # Site Footer
    ui.div(
        {"class": "site-footer"},
        ui.p(ui.strong("CAPITAL CREST REAL ESTATE"), " — Elevating Capital Living"),
        ui.HTML('<p>Addis Ababa, Ethiopia | Contact: <a href="mailto:milkyasmekonneng@gmail.com" style="color: var(--accent-gold);">milkyasmekonneng@gmail.com</a></p>')
    )
)

# ============================================================
# SERVER LOGIC
# ============================================================

def server(input, output, session):

    saved_favorites = reactive.value(set())

    @reactive.calc
    def filtered_data():
        df = raw_data.copy()
        if input.location() != "All":
            df = df[df["Location"] == input.location()]

        df = df[(df["Price"] >= input.min_price()) & (df["Price"] <= input.max_price())]

        if input.property_type() != "All":
            df = df[df["Type"] == input.property_type()]

        sort_choice = input.sort_by()
        if sort_choice == "price_asc":
            df = df.sort_values(by="Price", ascending=True)
        elif sort_choice == "price_desc":
            df = df.sort_values(by="Price", ascending=False)
        elif sort_choice == "sqm_asc":
            df = df.sort_values(by="Price_Per_SQM", ascending=True)
        elif sort_choice == "size_desc":
            df = df.sort_values(by="Size", ascending=False)

        return df

    # KPI Outputs
    @render.text
    def property_count():
        return f"{len(filtered_data())}"

    @render.text
    def average_price():
        df = filtered_data()
        return "ETB 0" if df.empty else f"ETB {df['Price'].mean():,.0f}"

    @render.text
    def average_sqm_price():
        df = filtered_data()
        return "ETB 0" if df.empty else f"ETB {df['Price_Per_SQM'].mean():,.0f} / m²"

    # Mortgage Calculation
    @reactive.calc
    def mortgage_calc():
        p = input.home_price()
        down_pct = input.down_payment_pct() / 100.0
        principal = p * (1 - down_pct)
        annual_rate = input.interest_rate() / 100.0
        monthly_rate = annual_rate / 12.0
        num_payments = input.loan_years() * 12

        if principal <= 0 or num_payments <= 0:
            return 0, 0, 0

        monthly_pmt = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1) if monthly_rate > 0 else principal / num_payments
        return monthly_pmt, principal, (monthly_pmt * num_payments) - principal

    @render.text
    def monthly_payment():
        pmt, _, _ = mortgage_calc()
        return f"ETB {pmt:,.0f} / mo"

    @render.text
    def total_loan_amount():
        _, loan, _ = mortgage_calc()
        return f"ETB {loan:,.0f}"

    @render.text
    def total_interest():
        _, _, interest = mortgage_calc()
        return f"ETB {interest:,.0f}"

    # Map Rendering (Plotly Scatter Map Fix)
    @render_widget
    def map_chart():
        df = filtered_data()
        if df.empty:
            return px.scatter(title="No properties match criteria.")

        # Modern Plotly uses scatter_map or scatter_mapbox based on version
        map_func = getattr(px, "scatter_map", getattr(px, "scatter_mapbox", None))
        
        if map_func:
            fig = map_func(
                df, lat="Lat", lon="Lon", color="Type", size="Size",
                hover_name="Location", hover_data={"Price": ":,ETB", "Price_Per_SQM": ":,.0f", "Lat": False, "Lon": False},
                zoom=11, height=400, title="Capital Crest Locations Across Addis Ababa"
            )
            style_param = "map_style" if map_func.__name__ == "scatter_map" else "mapbox_style"
            fig.update_layout({style_param: "open-street-map"}, margin={"r":0,"t":30,"l":0,"b":0})
            return fig
        else:
            return px.scatter(df, x="Lon", y="Lat", color="Type", title="Capital Crest Locations Across Addis Ababa")

    # Analytics Charts
    @render_widget
    def price_chart():
        df = filtered_data()
        return px.bar(title="No data available") if df.empty else px.bar(df, x="Location", y="Price", color="Type", title="Property Valuation by District", color_discrete_sequence=["#0B192C", "#D4AF37", "#1E3E62"])

    @render_widget
    def size_price_chart():
        df = filtered_data()
        return px.scatter(title="No data available") if df.empty else px.scatter(df, x="Size", y="Price", color="Type", size="Bedrooms", title="Size (m²) vs. Price Distribution", color_discrete_sequence=["#0B192C", "#D4AF37", "#1E3E62"])

    # Property Cards Rendering
    @render.ui
    def property_cards():
        df = filtered_data()
        if df.empty:
            return ui.div(ui.h4("No properties match your filter selection."))

        favs = saved_favorites()
        cards = []

        for _, row in df.iterrows():
            prop_id = int(row["ID"])
            is_fav = prop_id in favs
            btn_label = "❤️ Bookmarked" if is_fav else "🤍 Bookmark"
            btn_class = "btn btn-success btn-fav" if is_fav else "btn btn-outline-dark btn-fav"

            card = ui.div(
                {"class": "property-card"},
                ui.div(
                    {"class": "property-img-box", "style": f"background-image: url('{row['Image']}');"},
                    ui.span(f"{row['Type']}", class_="property-type-badge")
                ),
                ui.div(
                    {"class": "property-card-content"},
                    ui.h4(f"{row['Type']} in {row['Location']}", class_="property-title"),
                    ui.div(f"ETB {row['Price']:,.0f}", class_="property-price"),
                    ui.div(
                        {"class": "property-details"},
                        ui.span(f"🛏 {row['Bedrooms']} Beds"),
                        ui.span(f"🚿 {row['Bathrooms']} Baths"),
                        ui.span(f"📐 {row['Size']} m²"),
                        ui.span(f"🏷 ETB {row['Price_Per_SQM']:,.0f} / m²")
                    ),
                    ui.div(
                        {"class": "card-actions"},
                        ui.input_action_button(f"fav_btn_{prop_id}", btn_label, class_=btn_class),
                        ui.input_action_button(f"detail_btn_{prop_id}", "👁️ View Crest Details", class_="btn btn-details")
                    )
                )
            )
            cards.append(card)

        return ui.div({"class": "property-grid"}, *cards)

    # Observers for Favorites & Modal Details
    @reactive.effect
    def _():
        for _, row in raw_data.iterrows():
            prop_id = int(row["ID"])
            fav_btn_id = f"fav_btn_{prop_id}"
            detail_btn_id = f"detail_btn_{prop_id}"

            if input[fav_btn_id]() > 0:
                with reactive.isolate():
                    current_favs = set(saved_favorites())
                    if prop_id in current_favs:
                        current_favs.remove(prop_id)
                    else:
                        current_favs.add(prop_id)
                    saved_favorites.set(current_favs)

            if input[detail_btn_id]() > 0:
                with reactive.isolate():
                    prop = raw_data[raw_data["ID"] == prop_id].iloc[0]
                    m = ui.modal(
                        ui.div(
                            ui.img(src=prop["Image"], style="width:100%; height:250px; object-fit:cover; border-radius:12px; margin-bottom:15px; border:1px solid #D4AF37;"),
                            ui.h3(f"{prop['Type']} in {prop['Location']}", style="font-family:'Cinzel',serif; color:#0B192C;"),
                            ui.h4(f"Price: ETB {prop['Price']:,.0f}", style="color:#1E3E62; font-weight:800;"),
                            ui.hr(),
                            ui.p(f"🛏 **Bedrooms:** {prop['Bedrooms']} | 🚿 **Bathrooms:** {prop['Bathrooms']} | 📐 **Size:** {prop['Size']} m²"),
                            ui.p(f"🏷 **Price per m²:** ETB {prop['Price_Per_SQM']:,.0f}"),
                            ui.p(f"✨ **Amenities:** {prop['Amenities']}"),
                            ui.hr(),
                            ui.p("📞 **Private Advisory:** Contact a Capital Crest advisor at `+251 911 000 000` or email `advisory@capitalcrest.et`.")
                        ),
                        title=f"Capital Crest Listing #{prop_id}",
                        easy_close=True,
                        footer=ui.modal_button("Close")
                    )
                    ui.modal_show(m)

    # Favorites Table Output
    @render.table
    def favorites_table():
        fav_ids = saved_favorites()
        if not fav_ids:
            return pd.DataFrame({"Status": ["No properties bookmarked yet. Click 'Bookmark' on any card above!"]})
        
        df = raw_data[raw_data["ID"].isin(fav_ids)].copy()
        df["Price (ETB)"] = df["Price"].apply(lambda x: f"{x:,.0f}")
        df["Price / m²"] = df["Price_Per_SQM"].apply(lambda x: f"{x:,.0f} ETB")
        return df[["ID", "Location", "Type", "Bedrooms", "Size", "Price (ETB)", "Price / m²"]]

    # CSV Download Handler
    @render.download(filename="capital_crest_listings.csv")
    def download_csv():
        buf = io.BytesIO()
        filtered_data().to_csv(buf, index=False)
        buf.seek(0)
        return buf

app_dir = Path(__file__).parent

app = App(
    app_ui,
    server,
    static_assets=app_dir / "www",
)