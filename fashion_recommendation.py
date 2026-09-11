def get_body_type(measurements):
    """Determine an approximate body type from body measurements."""

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


def get_clothing_size(measurements):
    """Estimate approximate clothing size."""

    chest = measurements.get("chest", 0)
    waist = measurements.get("waist", 0)
    hip = measurements.get("hip", 0)

    if chest == 0 and waist == 0 and hip == 0:
        return "M"

    largest_measurement = max(chest, waist, hip)

    if largest_measurement < 80:
        return "XS"
    elif largest_measurement < 90:
        return "S"
    elif largest_measurement < 100:
        return "M"
    elif largest_measurement < 110:
        return "L"
    else:
        return "XL"


def get_top_recommendations(body_type):

    tops = {
        "Hourglass": [
            "Wrap tops",
            "Fitted tops",
            "Peplum tops",
            "Waist-defined tops"
        ],

        "Rectangle": [
            "Layered tops",
            "Peplum tops",
            "Structured tops",
            "Ruffled tops"
        ],

        "Inverted Triangle": [
            "V-neck tops",
            "Simple fitted tops",
            "Longline tops",
            "Minimal-detail tops"
        ],

        "Triangle": [
            "Structured tops",
            "Boat-neck tops",
            "Statement tops",
            "Embellished tops"
        ],

        "Balanced": [
            "Wrap tops",
            "Fitted tops",
            "Structured tops",
            "Layered tops"
        ]
    }

    return tops.get(body_type, tops["Balanced"])


def get_neckline_recommendations(body_type):

    necklines = {
        "Hourglass": [
            "V-neck",
            "Sweetheart neckline",
            "Square neckline",
            "Wrap neckline"
        ],

        "Rectangle": [
            "Round neckline",
            "Square neckline",
            "Scoop neckline",
            "Boat neckline"
        ],

        "Inverted Triangle": [
            "V-neck",
            "Scoop neckline",
            "U-neck",
            "Simple round neckline"
        ],

        "Triangle": [
            "Boat neckline",
            "Square neckline",
            "Wide scoop neckline",
            "Off-shoulder neckline"
        ],

        "Balanced": [
            "V-neck",
            "Square neckline",
            "Round neckline",
            "Boat neckline"
        ]
    }

    return necklines.get(body_type, necklines["Balanced"])


def get_sleeve_recommendations(body_type):

    sleeves = {
        "Hourglass": [
            "Fitted sleeves",
            "Three-quarter sleeves",
            "Full sleeves",
            "Short fitted sleeves"
        ],

        "Rectangle": [
            "Puff sleeves",
            "Bell sleeves",
            "Layered sleeves",
            "Three-quarter sleeves"
        ],

        "Inverted Triangle": [
            "Simple sleeves",
            "Straight sleeves",
            "Three-quarter sleeves",
            "Fitted sleeves"
        ],

        "Triangle": [
            "Puff sleeves",
            "Statement sleeves",
            "Bell sleeves",
            "Structured sleeves"
        ],

        "Balanced": [
            "Fitted sleeves",
            "Three-quarter sleeves",
            "Bell sleeves",
            "Puff sleeves"
        ]
    }

    return sleeves.get(body_type, sleeves["Balanced"])


def get_bottom_recommendations(body_type):

    bottoms = {
        "Hourglass": [
            "High-waisted trousers",
            "Straight-fit jeans",
            "Bootcut trousers",
            "A-line skirts"
        ],

        "Rectangle": [
            "High-waisted trousers",
            "A-line skirts",
            "Wide-leg trousers",
            "Straight-fit jeans"
        ],

        "Inverted Triangle": [
            "Wide-leg trousers",
            "Flared trousers",
            "A-line skirts",
            "Straight-fit jeans"
        ],

        "Triangle": [
            "Straight-fit trousers",
            "Bootcut trousers",
            "Dark straight-fit jeans",
            "A-line skirts"
        ],

        "Balanced": [
            "Straight-fit trousers",
            "Wide-leg trousers",
            "A-line skirts",
            "Straight-fit jeans"
        ]
    }

    return bottoms.get(body_type, bottoms["Balanced"])


def get_dress_recommendations(body_type):

    dresses = {
        "Hourglass": [
            "Wrap dresses",
            "Fit-and-flare dresses",
            "A-line dresses",
            "Belted dresses"
        ],

        "Rectangle": [
            "A-line dresses",
            "Fit-and-flare dresses",
            "Layered dresses",
            "Belted dresses"
        ],

        "Inverted Triangle": [
            "A-line dresses",
            "Fit-and-flare dresses",
            "Flowy dresses",
            "Simple waist-defined dresses"
        ],

        "Triangle": [
            "A-line dresses",
            "Fit-and-flare dresses",
            "Structured dresses",
            "Boat-neck dresses"
        ],

        "Balanced": [
            "A-line dresses",
            "Wrap dresses",
            "Fit-and-flare dresses",
            "Midi dresses"
        ]
    }

    return dresses.get(body_type, dresses["Balanced"])


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

    return colors.get(body_type, colors["Balanced"])


def get_pattern_recommendations(body_type):

    patterns = {
        "Hourglass": [
            "Solid colours",
            "Small prints",
            "Balanced geometric patterns",
            "Subtle floral prints"
        ],

        "Rectangle": [
            "Horizontal stripes",
            "Geometric prints",
            "Layered patterns",
            "Floral prints"
        ],

        "Inverted Triangle": [
            "Vertical stripes",
            "Minimal upper-body patterns",
            "Small prints",
            "Simple geometric patterns"
        ],

        "Triangle": [
            "Statement prints",
            "Horizontal patterns",
            "Floral prints",
            "Geometric patterns"
        ],

        "Balanced": [
            "Vertical stripes",
            "Small prints",
            "Floral prints",
            "Geometric patterns"
        ]
    }

    return patterns.get(body_type, patterns["Balanced"])


def get_outfit_combinations(body_type):

    outfits = {
        "Hourglass": [
            {
                "top": "Wrap top",
                "bottom": "High-waisted trousers",
                "colour": "Navy Blue"
            },
            {
                "top": "Fitted top",
                "bottom": "A-line skirt",
                "colour": "Burgundy"
            },
            {
                "dress": "Wrap dress",
                "colour": "Emerald Green"
            }
        ],

        "Rectangle": [
            {
                "top": "Layered top",
                "bottom": "Wide-leg trousers",
                "colour": "Pastel Blue"
            },
            {
                "top": "Peplum top",
                "bottom": "A-line skirt",
                "colour": "Lavender"
            },
            {
                "dress": "Fit-and-flare dress",
                "colour": "Navy Blue"
            }
        ],

        "Inverted Triangle": [
            {
                "top": "Simple V-neck top",
                "bottom": "Wide-leg trousers",
                "colour": "Black"
            },
            {
                "top": "Minimal fitted top",
                "bottom": "A-line skirt",
                "colour": "Forest Green"
            },
            {
                "dress": "A-line dress",
                "colour": "Burgundy"
            }
        ],

        "Triangle": [
            {
                "top": "Structured top",
                "bottom": "Straight-fit trousers",
                "colour": "Sky Blue"
            },
            {
                "top": "Boat-neck top",
                "bottom": "Bootcut trousers",
                "colour": "White"
            },
            {
                "dress": "A-line dress",
                "colour": "Lavender"
            }
        ],

        "Balanced": [
            {
                "top": "Wrap top",
                "bottom": "Straight-fit trousers",
                "colour": "Navy Blue"
            },
            {
                "top": "Structured top",
                "bottom": "A-line skirt",
                "colour": "Pastel Green"
            },
            {
                "dress": "A-line dress",
                "colour": "Black"
            }
        ]
    }

    return outfits.get(body_type, outfits["Balanced"])


def generate_fashion_recommendations(measurements):

    body_type = get_body_type(measurements)

    clothing_size = get_clothing_size(measurements)

    tops = get_top_recommendations(body_type)
    necklines = get_neckline_recommendations(body_type)
    sleeves = get_sleeve_recommendations(body_type)
    bottoms = get_bottom_recommendations(body_type)
    dresses = get_dress_recommendations(body_type)
    colors = get_color_recommendations(body_type)
    patterns = get_pattern_recommendations(body_type)
    outfits = get_outfit_combinations(body_type)

    return {
        "body_type": body_type,
        "approximate_clothing_size": clothing_size,
        "recommended_tops": tops,
        "recommended_necklines": necklines,
        "recommended_sleeves": sleeves,
        "recommended_bottoms": bottoms,
        "recommended_dresses": dresses,
        "recommended_colors": colors,
        "recommended_patterns": patterns,
        "outfit_combinations": outfits
    }