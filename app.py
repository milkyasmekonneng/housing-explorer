from pathlib import Path
import pandas as pd
import plotly.express as px
from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget

# ============================================================
# APP PATH
# ============================================================
app_dir = Path(__file__).parent

# ============================================================
# PROPERTY DATA
# ============================================================
raw_data = pd.DataFrame(
    [
        {
            "ID": 1,
            "Location": "Bole",
            "Type": "Apartment",
            "Price": 8_500_000,
            "Bedrooms": 3,
            "Bathrooms": 2,
            "Size": 145,
            "Lat": 9.0108,
            "Lon": 38.7613,
            "Image": "https://images.unsplash.com/photo-1600607687920-4e2a09cf159d",
            "Amenities": "Parking, Security, Balcony, Generator",
        },
        {
            "ID": 2,
            "Location": "Kazanchis",
            "Type": "Apartment",
            "Price": 12_000_000,
            "Bedrooms": 4,
            "Bathrooms": 3,
            "Size": 210,
            "Lat": 9.0127,
            "Lon": 38.7686,
            "Image": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c",
            "Amenities": "Parking, Elevator, Security, Gym",
        },
        {
            "ID": 3,
            "Location": "CMC",
            "Type": "Villa",
            "Price": 18_000_000,
            "Bedrooms": 5,
            "Bathrooms": 4,
            "Size": 320,
            "Lat": 9.0055,
            "Lon": 38.8415,
            "Image": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c",
            "Amenities": "Garden, Parking, Security, Generator",
        },
        {
            "ID": 4,
            "Location": "Lebu",
            "Type": "House",
            "Price": 6_500_000,
            "Bedrooms": 3,
            "Bathrooms": 2,
            "Size": 180,
            "Lat": 8.9390,
            "Lon": 38.7345,
            "Image": "https://images.unsplash.com/photo-1600566753051-f0b89df2dd90",
            "Amenities": "Garden, Parking, Water Tank, Security",
        },
        {
            "ID": 5,
            "Location": "Bole",
            "Type": "Penthouse",
            "Price": 25_000_000,
            "Bedrooms": 4,
            "Bathrooms": 4,
            "Size": 350,
            "Lat": 9.0050,
            "Lon": 38.7650,
            "Image": "https://images.unsplash.com/photo-1600607688969-a5bfcd646154",
            "Amenities": "Rooftop, Parking, Gym, Security, Elevator",
        },
        {
            "ID": 6,
            "Location": "Kazanchis",
            "Type": "Apartment",
            "Price": 9_500_000,
            "Bedrooms": 3,
            "Bathrooms": 2,
            "Size": 160,
            "Lat": 9.0160,
            "Lon": 38.7700,
            "Image": "https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3",
            "Amenities": "Parking, Security, Balcony, Elevator",
        },
        {
            "ID": 7,
            "Location": "CMC",
            "Type": "Villa",
            "Price": 22_000_000,
            "Bedrooms": 5,
            "Bathrooms": 5,
            "Size": 400,
            "Lat": 9.0080,
            "Lon": 38.8450,
            "Image": "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0",
            "Amenities": "Garden, Pool, Parking, Security, Generator",
        },
        {
            "ID": 8,
            "Location": "Lebu",
            "Type": "Apartment",
            "Price": 5_200_000,
            "Bedrooms": 2,
            "Bathrooms": 2,
            "Size": 120,
            "Lat": 8.9420,
            "Lon": 38.7380,
            "Image": "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea",
            "Amenities": "Parking, Security, Balcony",
        },
    ]
)
raw_data["Price_Per_SQM"] = raw_data["Price"] / raw_data["Size"]

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def format_price(value):
    return f"{value:,.0f} ETB"

def format_short_price(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M ETB"
    if value >= 1_000:
        return f"{value / 1_000:.0f}K ETB"
    return f"{value:,.0f} ETB"

# ============================================================
# CSS
# ============================================================
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,400&display=swap');

:root {
    --navy: #0d1b2a;
    --navy-light: #1b263b;
    --gold: #c9a227;
    --gold-light: #e0c45c;
    --cream: #f8f5ed;
    --white: #ffffff;
    --gray: #6c757d;
    --dark: #20252b;
    --border-color: #e2e8f0;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
    margin: 0;
    background: #fafafa;
    color: var(--dark);
    font-family: "DM Sans", sans-serif;
    overflow-x: hidden;
}

.container-main {
    max-width: 1200px;
    margin: auto;
    padding: 0 24px;
}

/* NAVBAR */
.navbar-custom {
    background: var(--navy);
    color: white;
    padding: 20px 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.navbar-inner {
    max-width: 1200px;
    margin: auto;
    padding: 0 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.brand-name {
    font-family: "Playfair Display", serif;
    font-size: 26px;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: white;
}
.brand-subtitle {
    color: var(--gold-light);
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
}
.nav-links {
    display: flex;
    gap: 25px;
}
.nav-link-custom {
    color: white;
    text-decoration: none;
    font-size: 14px;
    transition: color 0.2s ease;
}
.nav-link-custom:hover {
    color: var(--gold-light);
}

/* HERO */
.hero {
    position: relative;
    background: linear-gradient(rgba(13, 27, 42, 0.75), rgba(13, 27, 42, 0.85)),
                url("https://images.unsplash.com/photo-1600607687920-4e2a09cf159d") center/cover no-repeat;
    padding: 90px 0 110px 0;
    min-height: 440px;
    display: flex;
    align-items: center;
}
.hero-content {
    max-width: 700px;
}
.hero-title {
    font-family: "Playfair Display", serif;
    color: white;
    font-size: 56px;
    font-weight: 700;
    line-height: 1.15;
    margin-bottom: 16px;
}
.hero-text {
    color: #e2e8f0;
    font-size: 18px;
    line-height: 1.6;
}

/* SECTIONS */
.section {
    padding: 70px 0;
}
.section-title {
    font-family: "Playfair Display", serif;
    color: var(--navy);
    font-size: 38px;
    margin-bottom: 8px;
}
.section-subtitle {
    color: var(--gray);
    margin-bottom: 35px;
}

/* SEARCH */
.search-box {
    background: white;
    padding: 24px 30px;
    border-radius: 12px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
    margin-top: -50px;
    position: relative;
    z-index: 20;
    border: 1px solid var(--border-color);
}

/* BUTTONS */
.btn-gold {
    background: var(--gold) !important;
    color: white !important;
    border: none !important;
    font-weight: 600;
}
.btn-gold:hover {
    background: #ad891d !important;
}
.btn-navy {
    background: var(--navy) !important;
    color: white !important;
    border: none !important;
}
.btn-navy:hover {
    background: var(--navy-light) !important;
}

/* KPI CARDS */
.kpi-card {
    background: white;
    padding: 28px;
    border-radius: 12px;
    border: 1px solid var(--border-color);
    text-align: center;
    height: 100%;
}
.kpi-number {
    color: var(--gold);
    font-size: 30px;
    font-weight: 700;
}
.kpi-label {
    color: var(--gray);
    font-size: 14px;
    margin-top: 5px;
}

/* PROPERTY CARDS & OPTIMIZED IMAGES */
.property-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border-color);
    height: 100%;
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease;
    will-change: transform;
    backface-visibility: hidden;
    transform: translateZ(0);
}
.property-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 16px 32px rgba(0, 0, 0, 0.08);
}
.property-image-wrapper {
    width: 100%;
    height: 230px;
    overflow: hidden;
    background: #e2e8f0;
}
.property-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    content-visibility: auto;
}
.property-body {
    padding: 22px;
}
.property-location {
    color: var(--gold);
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.property-title {
    color: var(--navy);
    font-family: "Playfair Display", serif;
    font-size: 22px;
    font-weight: 600;
    margin: 6px 0;
}
.property-price {
    color: var(--navy-light);
    font-size: 19px;
    font-weight: 700;
    margin-bottom: 12px;
}
.property-features {
    color: var(--gray);
    font-size: 13px;
    margin-bottom: 18px;
    border-top: 1px solid #f1f5f9;
    padding-top: 12px;
}

/* ANALYTICS */
.analytics-card {
    background: white;
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 22px;
    height: 100%;
}

/* FORMS */
.contact-form-box {
    background: var(--cream);
    padding: 35px;
    border-radius: 14px;
}
.contact-form-title {
    font-family: "Playfair Display", serif;
    color: var(--navy);
    font-size: 28px;
}
.contact-form-description {
    color: var(--gray);
}

/* MODAL */
.modal-dialog {
    max-width: 720px !important;
}
.clean-modal-image {
    width: 100%;
    height: 330px;
    object-fit: cover;
    border-radius: 12px;
    display: block;
}
.clean-modal-location {
    color: var(--gold);
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-top: 20px;
}
.clean-modal-title {
    font-family: "Playfair Display", serif;
    color: var(--navy);
    font-size: 32px;
    margin: 4px 0;
}
.clean-modal-price {
    color: var(--gold);
    font-size: 23px;
    font-weight: 700;
    margin-bottom: 20px;
}
.clean-property-stats {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}
.clean-property-stat {
    background: var(--cream);
    border-radius: 8px;
    padding: 10px 15px;
    color: var(--navy);
    font-size: 14px;
    font-weight: 600;
}
.clean-amenities {
    color: var(--gray);
    font-size: 14px;
    line-height: 1.7;
    margin-bottom: 24px;
}
.clean-modal-actions {
    display: flex;
    gap: 10px;
}

/* FOOTER */
.footer {
    background: var(--navy);
    color: white;
    padding: 50px 0;
    margin-top: 60px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
}
.footer-brand {
    font-family: "Playfair Display", serif;
    font-size: 24px;
}

/* RESPONSIVE DESIGN */
@media (max-width: 992px) {
    .nav-links { gap: 15px; }
    .hero-title { font-size: 48px; }
}
@media (max-width: 768px) {
    .container-main { padding-left: 16px; padding-right: 16px; }
    .section { padding: 45px 0; }
    .nav-links { display: none; }
    .hero { min-height: 380px; padding: 60px 0; }
    .hero-title { font-size: 36px; }
    .search-box { margin-top: -35px; padding: 20px; }
    .property-image-wrapper { height: 200px; }
}
"""

# ============================================================
# UI
# ============================================================
app_ui = ui.page_fluid(
    ui.tags.head(ui.tags.style(custom_css)),
    # NAVBAR
    ui.div(
        {"class": "navbar-custom"},
        ui.div(
            {"class": "navbar-inner"},
            ui.div(
                ui.div("CAPITAL CREST", {"class": "brand-name"}),
                ui.div("REAL ESTATE", {"class": "brand-subtitle"}),
            ),
            ui.div(
                ui.a("Home", href="#home", class_="nav-link-custom"),
                ui.a("Properties", href="#properties", class_="nav-link-custom"),
                ui.a("Locations", href="#locations", class_="nav-link-custom"),
                ui.a("Analytics", href="#analytics", class_="nav-link-custom"),
                ui.a("About", href="#about", class_="nav-link-custom"),
                class_="nav-links",
            ),
        ),
    ),
    # HERO
    ui.div(
        {"class": "hero", "id": "home"},
        ui.div(
            {"class": "container-main"},
            ui.div(
                {"class": "hero-content"},
                ui.h1("Find a Place Worth Coming Home To", class_="hero-title"),
                ui.p(
                    "Explore carefully selected properties across Addis Ababa with clear market insights.",
                    class_="hero-text",
                ),
            ),
        ),
    ),
    # SEARCH
    ui.div(
        {"class": "container-main"},
        ui.div(
            {"class": "search-box"},
            ui.layout_columns(
                ui.input_select(
                    "location_filter",
                    "Location",
                    choices=["All Locations", "Bole", "Kazanchis", "CMC", "Lebu"],
                    selected="All Locations",
                ),
                ui.input_select(
                    "type_filter",
                    "Property Type",
                    choices=["All Types", "Apartment", "Villa", "House", "Penthouse"],
                    selected="All Types",
                ),
                ui.input_numeric(
                    "max_price", "Maximum Price (ETB)", value=30_000_000, min=0, step=500_000
                ),
                ui.input_select(
                    "sort_by",
                    "Sort By",
                    choices=[
                        "Price: Low to High",
                        "Price: High to Low",
                        "Size: Large to Small",
                    ],
                    selected="Price: Low to High",
                ),
            ),
        ),
    ),
    # MARKET OVERVIEW
    ui.div(
        {"class": "section"},
        ui.div(
            {"class": "container-main"},
            ui.h2("Market Overview", class_="section-title"),
            ui.p("A quick view of the current property selection.", class_="section-subtitle"),
            ui.output_ui("kpi_section"),
        ),
    ),
    # PROPERTIES
    ui.div(
        {"class": "section", "id": "properties"},
        ui.div(
            {"class": "container-main"},
            ui.h2("Featured Properties", class_="section-title"),
            ui.p("Explore available properties and view their details.", class_="section-subtitle"),
            ui.output_ui("property_cards"),
        ),
    ),
    # MAP
    ui.div(
        {"class": "section", "id": "locations"},
        ui.div(
            {"class": "container-main"},
            ui.h2("Property Locations", class_="section-title"),
            ui.p("Explore where our featured properties are located.", class_="section-subtitle"),
            output_widget("property_map"),
        ),
    ),
    # ANALYTICS
    ui.div(
        {"class": "section", "id": "analytics"},
        ui.div(
            {"class": "container-main"},
            ui.h2("Market Analytics", class_="section-title"),
            ui.p(
                "Understand the relationship between property type, size, and price.",
                class_="section-subtitle",
            ),
            ui.layout_columns(
                ui.div({"class": "analytics-card"}, output_widget("property_chart")),
                ui.div({"class": "analytics-card"}, output_widget("price_size_chart")),
            ),
        ),
    ),
    # MORTGAGE ESTIMATOR
    ui.div(
        {"class": "section"},
        ui.div(
            {"class": "container-main"},
            ui.h2("Mortgage Estimator", class_="section-title"),
            ui.p("Estimate your monthly mortgage payment.", class_="section-subtitle"),
            ui.layout_columns(
                ui.div(
                    {"class": "contact-form-box"},
                    ui.input_numeric("loan_amount", "Loan Amount (ETB)", value=5_000_000, min=0, step=100_000),
                    ui.input_numeric("interest_rate", "Annual Interest Rate (%)", value=10, min=0, step=0.5),
                    ui.input_numeric("loan_years", "Loan Term (Years)", value=20, min=1, step=1),
                ),
                ui.div(
                    {"class": "kpi-card"},
                    ui.h3("Estimated Monthly Payment", class_="kpi-label"),
                    ui.output_ui("mortgage_result"),
                ),
            ),
        ),
    ),
    # SAVED PROPERTIES
    ui.div(
        {"class": "section"},
        ui.div(
            {"class": "container-main"},
            ui.h2("Saved Properties", class_="section-title"),
            ui.p("Your favorite properties will appear here.", class_="section-subtitle"),
            ui.output_ui("saved_properties"),
            ui.download_button("download_favorites", "Download Saved Properties", class_="btn-gold"),
        ),
    ),
    # ABOUT
    ui.div(
        {"class": "section", "id": "about"},
        ui.div(
            {"class": "container-main"},
            ui.div(
                {"class": "contact-form-box"},
                ui.h2("About Capital Crest", class_="contact-form-title"),
                ui.p(
                    "Capital Crest is a real-estate exploration platform designed to make property discovery simple, transparent, and data-driven.",
                    class_="contact-form-description",
                ),
            ),
        ),
    ),
    # FOOTER
    ui.div(
        {"class": "footer"},
        ui.div(
            {"class": "container-main"},
            ui.div("CAPITAL CREST", class_="footer-brand"),
            ui.p("Real Estate • Addis Ababa"),
        ),
    ),
)

# ============================================================
# SERVER
# ============================================================
def server(input, output, session):
    favorites = reactive.value(set())
    selected_property = reactive.value(None)

    # FILTERED DATA
    @reactive.calc
    def filtered_data():
        df = raw_data.copy()
        location = input.location_filter()
        if location != "All Locations":
            df = df[df["Location"] == location]
        property_type = input.type_filter()
        if property_type != "All Types":
            df = df[df["Type"] == property_type]
        max_price = input.max_price()
        if max_price is not None:
            df = df[df["Price"] <= max_price]
        sort_by = input.sort_by()
        if sort_by == "Price: Low to High":
            df = df.sort_values("Price", ascending=True)
        elif sort_by == "Price: High to Low":
            df = df.sort_values("Price", ascending=False)
        elif sort_by == "Size: Large to Small":
            df = df.sort_values("Size", ascending=False)
        return df

    # KPI SECTION
    @output
    @render.ui
    def kpi_section():
        df = filtered_data()
        if df.empty:
            return ui.div("No properties match your filters.")
        average_price = df["Price"].mean()
        lowest_price = df["Price"].min()
        highest_price = df["Price"].max()
        return ui.layout_columns(
            ui.div(
                {"class": "kpi-card"},
                ui.div(str(len(df)), class_="kpi-number"),
                ui.div("Properties", class_="kpi-label"),
            ),
            ui.div(
                {"class": "kpi-card"},
                ui.div(format_short_price(average_price), class_="kpi-number"),
                ui.div("Average Price", class_="kpi-label"),
            ),
            ui.div(
                {"class": "kpi-card"},
                ui.div(format_short_price(lowest_price), class_="kpi-number"),
                ui.div("Lowest Price", class_="kpi-label"),
            ),
            ui.div(
                {"class": "kpi-card"},
                ui.div(format_short_price(highest_price), class_="kpi-number"),
                ui.div("Highest Price", class_="kpi-label"),
            ),
        )

    # PROPERTY CARDS (WITH LAZY LOADING AND FIXED CONTAINERS)
    @output
    @render.ui
    def property_cards():
        df = filtered_data()
        if df.empty:
            return ui.div(
                ui.h3("No properties found."),
                ui.p("Try changing your filters."),
            )
        cards = []
        for _, row in df.iterrows():
            prop_id = int(row["ID"])
            is_saved = prop_id in favorites()
            save_text = "Saved" if is_saved else "Save"
            card = ui.div(
                {"class": "property-card"},
                ui.div(
                    {"class": "property-image-wrapper"},
                    ui.img(
                        src=row["Image"],
                        class_="property-image",
                        loading="lazy",
                        width="100%",
                        height="230",
                        alt=f"{row['Type']} in {row['Location']}",
                    ),
                ),
                ui.div(
                    {"class": "property-body"},
                    ui.div(row["Location"], class_="property-location"),
                    ui.div(f"{row['Type']} • {row['Size']} m²", class_="property-title"),
                    ui.div(format_price(row["Price"]), class_="property-price"),
                    ui.div(
                        f"{row['Bedrooms']} Beds  |  {row['Bathrooms']} Baths  |  {row['Size']} m²",
                        class_="property-features",
                    ),
                    ui.div(
                        ui.input_action_button(f"save_btn_{prop_id}", save_text, class_="btn-navy"),
                        ui.input_action_button(f"detail_btn_{prop_id}", "View Property", class_="btn-gold"),
                        style="display:flex; gap:8px; flex-wrap:wrap;",
                    ),
                ),
            )
            cards.append(card)
        return ui.layout_columns(*cards, col_widths=[4, 4, 4])

    # SAVE BUTTONS
    @reactive.effect
    def handle_save_buttons():
        for _, row in raw_data.iterrows():
            prop_id = int(row["ID"])
            button_id = f"save_btn_{prop_id}"
            if input[button_id]() > 0:
                current = set(favorites())
                if prop_id in current:
                    current.remove(prop_id)
                    ui.notification_show("Property removed from saved properties.", type="message", duration=3)
                else:
                    current.add(prop_id)
                    ui.notification_show("Property saved.", type="message", duration=3)
                favorites.set(current)

    # PROPERTY DETAILS MODAL
    @reactive.effect
    def handle_property_buttons():
        for _, row in raw_data.iterrows():
            prop_id = int(row["ID"])
            detail_id = f"detail_btn_{prop_id}"
            if input[detail_id]() > 0:
                selected_property.set(prop_id)
                amenities = [item.strip() for item in row["Amenities"].split(",")]
                amenities_text = " • ".join(amenities)
                modal = ui.modal(
                    ui.img(src=row["Image"], class_="clean-modal-image", loading="lazy"),
                    ui.div(row["Location"], class_="clean-modal-location"),
                    ui.h2(row["Type"], class_="clean-modal-title"),
                    ui.div(format_price(row["Price"]), class_="clean-modal-price"),
                    ui.div(
                        ui.div(f"{row['Bedrooms']} Bedrooms", class_="clean-property-stat"),
                        ui.div(f"{row['Bathrooms']} Bathrooms", class_="clean-property-stat"),
                        ui.div(f"{row['Size']} m²", class_="clean-property-stat"),
                        ui.div(row["Type"], class_="clean-property-stat"),
                        class_="clean-property-stats",
                    ),
                    ui.p(amenities_text, class_="clean-amenities"),
                    ui.div(
                        ui.input_action_button("request_viewing_button", "Request a Viewing", class_="btn-gold"),
                        ui.modal_button("Close"),
                        class_="clean-modal-actions",
                    ),
                    title="Property Details",
                    easy_close=True,
                    footer=None,
                )
                ui.modal_show(modal)

    # REQUEST VIEWING FORM
    @reactive.effect
    @reactive.event(input.request_viewing_button)
    def show_request_form():
        prop_id = selected_property()
        if prop_id is None:
            return
        rows = raw_data[raw_data["ID"] == prop_id]
        if rows.empty:
            return
        row = rows.iloc[0]
        request_modal = ui.modal(
            ui.h4(
                "Request a Viewing",
                style="font-family:'Playfair Display',serif; color:#0d1b2a; margin-bottom:10px;",
            ),
            ui.p(f"{row['Type']} in {row['Location']} • {format_price(row['Price'])}", style="color:#6c757d;"),
            ui.input_text("request_name", "Full Name"),
            ui.input_text("request_phone", "Phone Number"),
            ui.input_text("request_email", "Email Address"),
            ui.input_date("request_date", "Preferred Viewing Date"),
            ui.input_text_area("request_message", "Message", placeholder="Optional message..."),
            ui.div(
                ui.input_action_button("request_submit", "Submit Request", class_="btn-gold"),
                ui.modal_button("Cancel"),
                style="display:flex; gap:10px; margin-top:15px;",
            ),
            title="Viewing Request",
            easy_close=True,
        )
        ui.modal_show(request_modal)

    # HANDLE VIEWING REQUEST
    @reactive.effect
    @reactive.event(input.request_submit)
    def handle_viewing_requests():
        prop_id = selected_property()
        if prop_id is None:
            ui.notification_show("Please select a property first.", type="error", duration=5)
            return
        property_rows = raw_data[raw_data["ID"] == prop_id]
        if property_rows.empty:
            ui.notification_show("Property could not be found.", type="error", duration=5)
            return
        row = property_rows.iloc[0]
        name = input.request_name()
        phone = input.request_phone()
        email = input.request_email()
        viewing_date = input.request_date()
        message = input.request_message()
        if not name or not name.strip():
            ui.notification_show("Please enter your full name.", type="error", duration=5)
            return
        if not phone or not phone.strip():
            ui.notification_show("Please enter your phone number.", type="error", duration=5)
            return
        if not email or not email.strip():
            ui.notification_show("Please enter your email address.", type="error", duration=5)
            return

        print("\n" + "=" * 60)
        print("NEW PROPERTY VIEWING REQUEST")
        print("=" * 60)
        print(f"Property ID: {prop_id}")
        print(f"Property: {row['Type']} in {row['Location']}")
        print(f"Price: {format_price(row['Price'])}")
        print(f"Name: {name}")
        print(f"Phone: {phone}")
        print(f"Email: {email}")
        print(f"Viewing Date: {viewing_date}")
        print(f"Message: {message}")
        print("=" * 60 + "\n")
        ui.notification_show("Viewing request received successfully!", type="message", duration=5)

    # MAP
    @output
    @render_widget
    def property_map():
        df = filtered_data()
        if df.empty:
            return px.scatter_map(title="No properties available")
        try:
            fig = px.scatter_map(
                df,
                lat="Lat",
                lon="Lon",
                hover_name="Location",
                hover_data={
                    "Type": True,
                    "Price": True,
                    "Bedrooms": True,
                    "Bathrooms": True,
                    "Lat": False,
                    "Lon": False,
                },
                zoom=11,
                height=500,
            )
            fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
            return fig
        except Exception:
            fig = px.scatter_mapbox(
                df, lat="Lat", lon="Lon", hover_name="Location", zoom=11, height=500
            )
            fig.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=0, b=0))
            return fig

    # PROPERTY TYPE CHART
    @output
    @render_widget
    def property_chart():
        df = filtered_data()
        if df.empty:
            return px.bar(title="No data available")
        counts = df["Type"].value_counts().reset_index()
        counts.columns = ["Type", "Count"]
        fig = px.bar(counts, x="Type", y="Count", title="Properties by Type")
        return fig

    # PRICE VS SIZE CHART
    @output
    @render_widget
    def price_size_chart():
        df = filtered_data()
        if df.empty:
            return px.scatter(title="No data available")
        fig = px.scatter(
            df,
            x="Size",
            y="Price",
            color="Type",
            hover_name="Location",
            title="Price vs Property Size",
        )
        return fig

    # MORTGAGE CALCULATOR
    @output
    @render.ui
    def mortgage_result():
        loan = input.loan_amount()
        annual_rate = input.interest_rate()
        years = input.loan_years()
        if loan is None or annual_rate is None or years is None:
            return ui.div("Enter loan details.")
        monthly_rate = annual_rate / 100 / 12
        number_payments = years * 12
        if monthly_rate == 0:
            monthly_payment = loan / number_payments
        else:
            monthly_payment = (
                loan
                * monthly_rate
                * (1 + monthly_rate) ** number_payments
                / ((1 + monthly_rate) ** number_payments - 1)
            )
        return ui.div(
            ui.div(format_price(monthly_payment), class_="kpi-number"),
            ui.p("Estimated monthly payment"),
        )

    # SAVED PROPERTIES
    @output
    @render.ui
    def saved_properties():
        saved_ids = favorites()
        if not saved_ids:
            return ui.p("You have not saved any properties yet.", style="color:#6c757d;")
        saved_df = raw_data[raw_data["ID"].isin(saved_ids)]
        items = []
        for _, row in saved_df.iterrows():
            items.append(
                ui.div(
                    ui.div(row["Location"], class_="property-location"),
                    ui.div(f"{row['Type']} • {row['Bedrooms']} Bedrooms", class_="property-title"),
                    ui.div(format_price(row["Price"]), class_="property-price"),
                    style="padding:18px; border:1px solid #eeeeee; border-radius:10px; margin-bottom:10px;",
                )
            )
        return ui.div(*items)

    # DOWNLOAD FAVORITES
    @output
    @render.download(filename=lambda: "saved_properties.csv")
    def download_favorites():
        saved_ids = favorites()
        saved_df = raw_data[raw_data["ID"].isin(saved_ids)]
        yield saved_df.to_csv(index=False)

# ============================================================
# CREATE APP
# ============================================================
app = App(app_ui, server, static_assets=app_dir / "www")