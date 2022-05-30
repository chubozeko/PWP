export interface IRecipeIngredient {
  rec_ing_id: number;
  recipe_id: number;
  ingredient_id: number;
  amount: number;
  unit: number;
}

export interface Ingredient {
  ingredient_id: number;
  name: string;
}
