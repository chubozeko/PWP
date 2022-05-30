import { environment } from './../../environments/environment.prod';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { BehaviorSubject } from 'rxjs';
import { IRecipe } from './../components/models/recipe';
import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class RecipesService {
  private apiUrl = environment.apiUrl;
  recipe: IRecipe[] = [
    {
      recipe_id: 1,
      recipe_name: 'string',
      prep_time: 1,
      cooking_time: 1,
      meal_type: 'string',
      calories: 1,
      servings: 1,
      instructions: 'string',
      creator_id: 1,
    },
  ];
  recipe$ = new BehaviorSubject<IRecipe[]>(this.recipe);

  constructor(private http: HttpClient) {}

  getRecipes() {
    this.http
      .get<IRecipe[]>(this.apiUrl + `recipes`)
      .pipe(map((resp: any) => resp.items))
      .subscribe(
        (chef) => {
          console.log(chef);
          this.recipe$.next(chef);
        },
        (err: HttpErrorResponse) => {
          if (err.error instanceof Error) {
            console.log('Client-side error occured.');
          } else {
            console.log('Server-side error occured.');
          }
        }
      );
  }
}
