
# ==================================================
# 3. HÌNH ẢNH - BBQ HOUSE
# ==================================================

@st.cache_data(ttl=86400, show_spinner=False)
def get_food_image(keywords, index):

    # Từ khóa tìm ảnh tương ứng với 20 món trong MENU
    image_searches = {
        0: ["beef", "steak"],
        1: ["beef ribs", "beef"],
        2: ["steak", "beef"],
        3: ["beef", "mushroom"],
        4: ["pork", "pork belly"],
        5: ["pork ribs", "ribs"],
        6: ["pork", "grilled pork"],
        7: ["prawn", "shrimp"],
        8: ["squid", "seafood"],
        9: ["octopus", "seafood"],
        10: ["oyster", "seafood"],
        11: ["mushroom", "vegetarian"],
        12: ["vegetable", "salad"],
        13: ["kimchi", "vegetarian"],
        14: ["seafood", "fish"],
        15: ["kimchi", "chicken"],
        16: ["seafood", "rice"],
        17: ["tea", "drink"],
        18: ["drink", "cocktail"],
        19: ["water", "drink"],
        50: ["beef", "seafood"]
    }

    # Ảnh dự phòng theo nhóm món
    fallback_images = {
        "beef": "https://images.unsplash.com/photo-1558030006-450675393462?w=900",
        "pork": "https://images.unsplash.com/photo-1544025162-d76694265947?w=900",
        "seafood": "https://images.unsplash.com/photo-1559737558-2f5a35f4523b?w=900",
        "vegetable": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=900",
        "hotpot": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=900",
        "drink": "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=900",
        "default": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=900"
    }

    # Tìm ảnh từ TheMealDB
    search_terms = image_searches.get(index, [])

    for term in search_terms:
        try:
            response = requests.get(
                "https://www.themealdb.com/api/json/v1/1/search.php",
                params={"s": term},
                timeout=8,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            if response.status_code == 200:
                data = response.json()
                meals = data.get("meals")

                if meals:
                    image_url = meals[0].get("strMealThumb")

                    if image_url:
                        return image_url

        except Exception:
            continue

    # Nếu không tìm được ảnh, chọn ảnh dự phòng theo nhóm
    if index in [0, 1, 2, 3]:
        return fallback_images["beef"]

    elif index in [4, 5, 6]:
        return fallback_images["pork"]

    elif index in [7, 8, 9, 10]:
        return fallback_images["seafood"]

    elif index in [11, 12, 13]:
        return fallback_images["vegetable"]

    elif index in [14, 15, 16]:
        return fallback_images["hotpot"]

    elif index in [17, 18, 19]:
        return fallback_images["drink"]

    return fallback_images["default"]
