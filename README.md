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

## Communication Contract
### How to Request and Receive Data
You can send a POST request to one of the endpoints with a JSON body. The service will then return JSON containing either a summary or scaled data.

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

### Example Call (using JS fetch)

```js
fetch("http://localhost:3000/summary", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    ingredients: ["1 cup rice", "2 eggs", "1 tbsp olive oil"],
    scalar: 1
  })
})
```

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

### Example Call (using JS fetch)


```js
fetch("http://localhost:3000/scale-ingredients", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    ingredients: ["1 cup rice", "2 eggs", "1 tbsp olive oil"],
    scalar: 2
  })
})
```

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

Example Call (using JS fetch)

```js
fetch("http://localhost:3000/scale-summary", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    calories: 500,
    protein: 20.5,
    carbs: 60.3,
    fat: 20.1,
    scalar: 2
  })
})
```

## UML Diagram

<img width="815" alt="Screenshot 2025-02-24 at 8 06 13 PM" src="https://github.com/user-attachments/assets/5a9afb4b-082b-47ab-b2c2-889cd7b7dd9d" />
