export interface IRecipe {
  recipe_id: number;
  recipe_name: string;
  prep_time: number;
  cooking_time: number;
  meal_type: string;
  calories: number;
  servings: number;
  instructions: string;
  creator_id: number;
}
