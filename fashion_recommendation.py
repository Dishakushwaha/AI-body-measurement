# ==========================================
# FASHION RECOMMENDATION ENGINE
# ==========================================

def get_body_type(measurements):
    """
    Determine approximate body type
    using predicted body measurements.
    """

    shoulder = measurements.get("shoulder-breadth", 0)
    chest = measurements.get("chest", 0)
    waist = measurements.get("waist", 0)
    hip = measurements.get("hip", 0)

    if shoulder == 0 or chest == 0 or waist == 0 or hip == 0:
        return "Balanced"

    if shoulder > hip * 1.10:
        return "Inverted Triangle"

    elif hip > shoulder * 1.10:
        return "Triangle"

    elif abs(shoulder - hip) <= shoulder * 0.08:

        if waist < chest * 0.75:
            return "Hourglass"

        else:
            return "Rectangle"

    else:
        return "Balanced"


# ==========================================
# CLOTHING RECOMMENDATIONS
# ==========================================

def get_clothing_recommendations(body_type):

    recommendations = {

        "Hourglass": [
            "Wrap tops",
            "A-line dresses",
            "High-waisted trousers",
            "Fitted jackets"
        ],

        "Rectangle": [
            "Layered outfits",
            "A-line skirts",
            "Straight-fit trousers",
            "Structured jackets"
        ],

        "Inverted Triangle": [
            "V-neck tops",
            "A-line skirts",
            "Wide-leg trousers",
            "Straight-fit jeans"
        ],

        "Triangle": [
            "Structured tops",
            "Boat-neck tops",
            "Straight-fit trousers",
            "A-line dresses"
        ],

        "Balanced": [
            "A-line dresses",
            "Straight-fit trousers",
            "Wrap tops",
            "Layered outfits"
        ]
    }

    return recommendations.get(
        body_type,
        recommendations["Balanced"]
    )


# ==========================================
# COLOR RECOMMENDATIONS
# ==========================================

def get_color_recommendations(body_type):

    colors = {

        "Hourglass": [
            "Navy Blue",
            "Burgundy",
            "Emerald Green",
            "Black"
        ],

        "Rectangle": [
            "Pastel Blue",
            "Lavender",
            "White",
            "Navy Blue"
        ],

        "Inverted Triangle": [
            "Dark Blue",
            "Black",
            "Forest Green",
            "Burgundy"
        ],

        "Triangle": [
            "White",
            "Sky Blue",
            "Pastel Green",
            "Lavender"
        ],

        "Balanced": [
            "Navy Blue",
            "White",
            "Pastel Green",
            "Black"
        ]
    }

    return colors.get(
        body_type,
        colors["Balanced"]
    )


# ==========================================
# MAIN RECOMMENDATION FUNCTION
# ==========================================

def generate_fashion_recommendations(measurements):

    body_type = get_body_type(measurements)

    clothing = get_clothing_recommendations(body_type)

    colors = get_color_recommendations(body_type)

    return {
        "body_type": body_type,
        "recommended_clothing": clothing,
        "recommended_colors": colors
    }