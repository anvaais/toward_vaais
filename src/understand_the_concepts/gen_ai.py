from google import genai
from pydantic import BaseModel , Field
from typing import List, Optional


class Ingredant(BaseModel):
    name:str = Field(..., description="Name of the ingredient")
    quantity: str = Field(..., description="Quantity of the ingredient")

class Recipe(BaseModel):
    name: str = Field(..., description="Name of the recipe")
    ingredients: List[Ingredant] = Field(..., description="List of ingredients")
    instructions: str = Field(..., description="Instructions for preparing the recipe")
    prep_time: Optional[str] = Field(None, description="Preparation time for the recipe")
    cook_time: Optional[str] = Field(None, description="Cooking time for the recipe")
    servings: Optional[int] = Field(None, description="Number of servings for the recipe")

clint = genai.Client()

prompt = """
Please extract the recipe from the following text.
The user wants to make delicious chocolate chip cookies.
They need 2 and 1/4 cups of all-purpose flour, 1 teaspoon of baking soda,
1 teaspoon of salt, 1 cup of unsalted butter (softened), 3/4 cup of granulated sugar,
3/4 cup of packed brown sugar, 1 teaspoon of vanilla extract, and 2 large eggs.
For the best part, they'll need 2 cups of semisweet chocolate chips.
First, preheat the oven to 375°F (190°C). Then, in a small bowl, whisk together the flour,
baking soda, and salt. In a large bowl, cream together the butter, granulated sugar, and brown sugar
until light and fluffy. Beat in the vanilla and eggs, one at a time. Gradually beat in the dry
ingredients until just combined. Finally, stir in the chocolate chips. Drop by rounded tablespoons
onto ungreased baking sheets and bake for 9 to 11 minutes.
"""


interaction  = clint.intractions_creat (


     model="gemini-3.8-flash",
    input=prompt,
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": Recipe.model_json_schema()
    },
)

recipe = Recipe.model_validate_json(interaction.output_text)
print(recipe)
