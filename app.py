from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_widget
import pandas as pd
import plotly.express as px


# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv("data/housing.csv")


# ==========================================
# USER INTERFACE
# ==========================================

app_ui = ui.page_fluid(

    # ======================================
    # STYLING
    # ======================================

    ui.tags.style("""
        body {
            background-color: #f5f7fb;
            font-family: Arial, sans-serif;
        }

        h1 {
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        h2 {
            margin-top: 30px;
            margin-bottom: 15px;
            font-weight: 600;
        }

        .card {
            border: none;
            border-radius: 14px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            padding: 10px;
            background-color: white;
        }

        .kpi-value {
            font-size: 28px;
            font-weight: 700;
            margin-top: 10px;
            margin-bottom: 5px;
        }

        .kpi-label {
            color: #6b7280;
            font-size: 14px;
            margin-bottom: 5px;
        }

        .ai-result {
            white-space: pre-line;
            font-size: 16px;
            line-height: 1.7;
            padding: 15px;
        }
        
        .hero-section {
            padding: 35px 25px;
            margin-bottom: 25px;
            border-radius: 18px;
            background: white;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        }

        .hero-section h1 {
            margin-bottom: 10px;
        }

        .hero-section p {
            color: #6b7280;
            font-size: 17px;
            margin-bottom: 0;
        }

        .btn {
            border-radius: 10px;
            font-weight: 600;
            padding: 10px 18px;
        }

        @media (max-width: 768px) {

            h1 {
                font-size: 28px;
            }

            h2 {
                font-size: 22px;
            }

            .hero-section {
                padding: 25px 18px;
            }

            .kpi-value {
                font-size: 24px;
            }
            .ai-header {
                margin-bottom: 20px;
        }

           .ai-header h3 {
                margin-bottom: 8px;
                font-size: 24px;
                font-weight: 700;
        }

           .ai-header p {
                color: #6b7280;
                font-size: 15px;
                line-height: 1.6;
        }

          .ai-button-container {
               margin-top: 15px;
               margin-bottom: 10px;
        }

          .ai-button {
               font-size: 16px;
               font-weight: 600;
               border-radius: 10px;
               padding: 12px 22px;
        }

           .ai-result {
               white-space: pre-line;
               font-size: 16px;
               line-height: 1.8;
               padding: 18px;
               border-radius: 12px;
               background-color: #f8fafc;
        }
        
            
    """),

    # ======================================
    # HEADER
    # ======================================

    ui.div(
    ui.h1("🏠 Housing Explorer"),
    ui.p(
        "Explore properties, compare prices, "
        "and find the right home for your budget."
    ),
    class_="hero-section",
),

    # ======================================
    # SIDEBAR
    # ======================================

    ui.layout_sidebar(

        ui.sidebar(

            ui.h3("🔎 Filters"),

            # Location
            ui.input_select(
                "location",
                "Location",
                {
                    "All": "All Locations",
                    "Bole": "Bole",
                    "Kazanchis": "Kazanchis",
                    "CMC": "CMC",
                    "Lebu": "Lebu",
                },
            ),

            # Minimum price
            ui.input_slider(
                "min_price",
                "Minimum Price (ETB)",
                min=500_000,
                max=20_000_000,
                value=500_000,
                step=500_000,
            ),

            # Maximum price
            ui.input_slider(
                "price",
                "Maximum Price (ETB)",
                min=500_000,
                max=20_000_000,
                value=20_000_000,
                step=500_000,
            ),

            # Bedrooms
            ui.input_slider(
                "bedrooms",
                "Maximum Bedrooms",
                min=1,
                max=6,
                value=6,
                step=1,
            ),

            # Bathrooms
            ui.input_slider(
                "bathrooms",
                "Minimum Bathrooms",
                min=1,
                max=5,
                value=1,
                step=1,
            ),

            # Property type
            ui.input_select(
                "property_type",
                "Property Type",
                {
                    "All": "All Types",
                    "Apartment": "Apartment",
                    "Villa": "Villa",
                    "House": "House",
                },
            ),
        ),

        # ==================================
        # PROPERTY OVERVIEW
        # ==================================

        ui.h2("Property Overview"),

        ui.layout_columns(

            ui.card(
                ui.h4("🏠 Properties"),

                ui.h2(
                    ui.output_text("property_count"),
                    class_="kpi-value",
                ),

                ui.p(
                    "Matching your filters",
                    class_="kpi-label",
                ),
            ),

            ui.card(
                ui.h4("💰 Average Price"),

                ui.h2(
                    ui.output_text("average_price"),
                    class_="kpi-value",
                ),

                ui.p(
                    "Average property price",
                    class_="kpi-label",
                ),
            ),

            ui.card(
                ui.h4("🛏️ Average Bedrooms"),

                ui.h2(
                    ui.output_text("average_bedrooms"),
                    class_="kpi-value",
                ),

                ui.p(
                    "Average bedrooms",
                    class_="kpi-label",
                ),
            ),
        ),

        # ==================================
        # PROPERTY TABLE
        # ==================================

        ui.h2("Available Properties"),

        ui.card(
            ui.output_data_frame("property_table")
        ),

        # ==================================
        # PRICE ANALYSIS
        # ==================================

        ui.h2("Price Analysis"),

        ui.layout_columns(

            ui.card(
                output_widget("price_chart")
            ),

            ui.card(
                output_widget("property_chart")
            ),
        ),

        # ==================================
        # PROPERTY SIZE ANALYSIS
        # ==================================

        ui.h2("Property Size Analysis"),

        ui.card(
            output_widget("size_price_chart")
        ),

        # ==================================
        # AI HOUSING HELPER
        # ==================================

ui.h2("🤖 AI Housing Helper"),

ui.card(

    ui.div(
        ui.h3("🏡 Find Your Ideal Home"),

        ui.p(
            "Tell the housing assistant what you need. "
            "It will analyze the available properties "
            "and recommend the best value."
        ),

        class_="ai-header",
    ),

    ui.layout_columns(

        ui.input_numeric(
            "budget",
            "Maximum Budget (ETB)",
            value=10_000_000,
            min=500_000,
            max=50_000_000,
            step=500_000,
        ),

        ui.input_numeric(
            "wanted_bedrooms",
            "Bedrooms Needed",
            value=3,
            min=1,
            max=10,
            step=1,
        ),

        ui.input_select(
            "wanted_type",
            "Property Type",
            {
                "Any": "Any Type",
                "Apartment": "Apartment",
                "Villa": "Villa",
                "House": "House",
            },
        ),
    ),

    ui.div(
        ui.input_action_button(
            "find_property",
            "🔎 Find My Property",
            class_="ai-button",
        ),
        class_="ai-button-container",
    ),

    ui.hr(),

    ui.div(
        ui.h4("💡 Assistant Recommendation"),

        ui.output_text("ai_recommendation"),

        class_="ai-result",
    ),
),
    
)

)


# ==========================================
# SERVER
# ==========================================

def server(input, output, session):

    # ======================================
    # FILTER DATA
    # ======================================

    @reactive.calc
    def filtered_data():

        data = df.copy()

        # Location filter
        if input.location() != "All":
            data = data[
                data["location"] == input.location()
            ]

        # Minimum price filter
        data = data[
            data["price"] >= input.min_price()
        ]

        # Maximum price filter
        data = data[
            data["price"] <= input.price()
        ]

        # Maximum bedrooms filter
        data = data[
            data["bedrooms"] <= input.bedrooms()
        ]

        # Minimum bathrooms filter
        data = data[
            data["bathrooms"] >= input.bathrooms()
        ]

        # Property type filter
        if input.property_type() != "All":
            data = data[
                data["type"] == input.property_type()
            ]

        return data

    # ======================================
    # PROPERTY COUNT
    # ======================================

    @output
    @render.text
    def property_count():

        data = filtered_data()

        return f"{len(data)} properties"

    # ======================================
    # AVERAGE PRICE
    # ======================================

    @output
    @render.text
    def average_price():

        data = filtered_data()

        if len(data) == 0:
            return "No properties"

        average = data["price"].mean()

        return f"ETB {average:,.0f}"

    # ======================================
    # AVERAGE BEDROOMS
    # ======================================

    @output
    @render.text
    def average_bedrooms():

        data = filtered_data()

        if len(data) == 0:
            return "No properties"

        average = data["bedrooms"].mean()

        return f"{average:.1f} bedrooms"

    # ======================================
    # PROPERTY TABLE
    # ======================================

    @output
    @render.data_frame
    def property_table():

        data = filtered_data()

        return render.DataGrid(
            data,
            width="100%",
            height="400px",
        )

    # ======================================
    # AVERAGE PRICE BY LOCATION
    # ======================================

    @output
    @render_widget
    def price_chart():

        data = filtered_data()

        if len(data) == 0:

            fig = px.bar(
                title="No properties match your filters"
            )

            return fig

        chart_data = (
            data
            .groupby("location", as_index=False)["price"]
            .mean()
        )

        fig = px.bar(
            chart_data,
            x="location",
            y="price",
            title="Average Property Price by Location",
            labels={
                "location": "Location",
                "price": "Average Price",
            },
            hover_data={
                "price": ":,.0f"
            },
        )

        fig.update_traces(
            hovertemplate=
            "<b>%{x}</b><br>"
            "Average Price: ETB %{y:,.0f}"
            "<extra></extra>"
        )

        fig.update_layout(
            height=450,

            margin=dict(
                l=20,
                r=20,
                t=60,
                b=40,
            ),

            yaxis=dict(
                tickprefix="ETB ",
                tickformat=",",
            ),

            xaxis_title="Location",
            yaxis_title="Average Price (ETB)",
        )

        return fig

    # ======================================
    # PROPERTY COUNT BY LOCATION
    # ======================================

    @output
    @render_widget
    def property_chart():

        data = filtered_data()

        if len(data) == 0:

            fig = px.bar(
                title="No properties match your filters"
            )

            return fig

        chart_data = (
            data
            .groupby("location")
            .size()
            .reset_index(name="properties")
        )

        fig = px.bar(
            chart_data,
            x="location",
            y="properties",
            title="Number of Properties by Location",
            labels={
                "location": "Location",
                "properties": "Properties",
            },
            hover_data={
                "properties": True
            },
        )

        fig.update_traces(
            hovertemplate=
            "<b>%{x}</b><br>"
            "Properties: %{y}"
            "<extra></extra>"
        )

        fig.update_layout(
            height=450,

            margin=dict(
                l=20,
                r=20,
                t=60,
                b=40,
            ),

            xaxis_title="Location",
            yaxis_title="Number of Properties",
        )

        return fig

    # ======================================
    # PROPERTY SIZE VS PRICE
    # ======================================

    @output
    @render_widget
    def size_price_chart():

        data = filtered_data()

        if len(data) == 0:

            fig = px.scatter(
                title="No properties match your filters"
            )

            return fig

        fig = px.scatter(
            data,
            x="area",
            y="price",
            color="type",
            hover_data=[
                "location",
                "bedrooms",
                "bathrooms",
                "area",
                "price",
            ],
            title="Property Size vs. Price",
            labels={
                "area": "Property Size (m²)",
                "price": "Price (ETB)",
                "type": "Property Type",
            },
        )

        fig.update_traces(
            marker=dict(
                size=12,
            ),

            hovertemplate=
            "<b>Property</b><br>"
            "Location: %{customdata[0]}<br>"
            "Bedrooms: %{customdata[1]}<br>"
            "Bathrooms: %{customdata[2]}<br>"
            "Area: %{customdata[3]} m²<br>"
            "Price: ETB %{y:,.0f}"
            "<extra></extra>"
        )

        fig.update_layout(
            height=500,

            margin=dict(
                l=20,
                r=20,
                t=60,
                b=40,
            ),

            xaxis_title="Property Size (m²)",

            yaxis_title="Price (ETB)",

            yaxis=dict(
                tickprefix="ETB ",
                tickformat=",",
            ),
        )

        return fig

    # ======================================
    # AI HOUSING HELPER
    # ======================================

    @output
    @render.text
    @reactive.event(input.find_property)
    def ai_recommendation():

        data = df.copy()

        # Get user preferences
        budget = input.budget()
        bedrooms = input.wanted_bedrooms()
        property_type = input.wanted_type()

        # ----------------------------------
        # Filter by budget
        # ----------------------------------

        data = data[
            data["price"] <= budget
        ]

        # ----------------------------------
        # Filter by bedrooms
        # ----------------------------------

        data = data[
            data["bedrooms"] >= bedrooms
        ]

        # ----------------------------------
        # Filter by property type
        # ----------------------------------

        if property_type != "Any":

            data = data[
                data["type"] == property_type
            ]

        # ----------------------------------
        # No results
        # ----------------------------------

        if len(data) == 0:

            return (
                "❌ No matching properties found.\n\n"
                "Try increasing your budget or reducing "
                "the number of bedrooms required."
            )

        # ----------------------------------
        # Calculate price per square meter
        # ----------------------------------

        data = data.copy()

        data["price_per_area"] = (
            data["price"] / data["area"]
        )

        # ----------------------------------
        # Find best value
        # ----------------------------------

        best_property = (
            data
            .sort_values("price_per_area")
            .iloc[0]
        )

        # ----------------------------------
        # Recommendation
        # ----------------------------------

        return (
            "🤖 Recommended Property\n\n"

            f"📍 Location: "
            f"{best_property['location']}\n"

            f"🏠 Type: "
            f"{best_property['type']}\n"

            f"💰 Price: "
            f"ETB {best_property['price']:,.0f}\n"

            f"🛏️ Bedrooms: "
            f"{best_property['bedrooms']}\n"

            f"🛁 Bathrooms: "
            f"{best_property['bathrooms']}\n"

            f"📐 Area: "
            f"{best_property['area']} m²\n\n"

            "💡 Why this property?\n"

            "It provides the best price-to-size "
            "value among the properties matching "
            "your requirements."
        )


# ==========================================
# CREATE APP
# ==========================================

app = App(app_ui, server)