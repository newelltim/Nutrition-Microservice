# Nutritionix Microservice

A simple Flask microservice that uses the **Nutritionix Natural Language API** to:
1. Provide a **nutritional summary** of a list of ingredients.
2. **Scale ingredient** quantities.
3. **Scale a nutritional summary**.

---

## Running the Service

1. Ensure you have Python, Flask, Requests, and valid Nutritionix credentials (App ID and Key).
2. Open a terminal in the project directory.
3. Start the Flask server:
   ```bash
   python app.py
By default, the service will be available at http://localhost:3000.

---

## Endpoints

### POST /summary

Description: Returns the combined nutritional summary (calories, protein, carbs, fat) for a list of ingredients, optionally scaled by scalar.
Request JSON:

{
  "ingredients": ["1 cup rice", "2 eggs", "1 tbsp olive oil"],
  "scalar": 1
}
Response JSON:

{
  "summary": {
    "calories": 500,
    "protein": 20.5,
    "carbs": 60.3,
    "fat": 20.1
  }
}

---

### POST /scale-ingredients
Description: Scales the first numeric token in each ingredient string by scalar.
Request JSON:

{
  "ingredients": ["1 cup rice", "2 eggs", "1 tbsp olive oil"],
  "scalar": 2
}
Response JSON:

{
  "scaledIngredients": ["2 cup rice", "4 eggs", "2 tbsp olive oil"]
}

---

### POST /scale-summary
Description: Takes a base nutritional summary and a scalar, then returns the scaled values.
Request JSON:

{
  "calories": 500,
  "protein": 20.5,
  "carbs": 60.3,
  "fat": 20.1,
  "scalar": 2
}
Response JSON:

{
  "summary": {
    "calories": 1000,
    "protein": 41,
    "carbs": 120.6,
    "fat": 40.2
  }
}
