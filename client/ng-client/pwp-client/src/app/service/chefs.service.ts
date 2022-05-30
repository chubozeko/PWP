import { environment } from './../../environments/environment';
import { IUser } from './../components/models/user';
import { Injectable } from '@angular/core';
import {
  HttpClient,
  HttpErrorResponse,
  HttpHeaders,
} from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json',
  }),
};

@Injectable({
  providedIn: 'root',
})
export class ChefsService {
  private apiUrl = environment.apiUrl;
  chefs: IUser[] = [
    {
      user_id: 1,
      username: 'tag',
    },
  ];
  chefs$ = new BehaviorSubject<IUser[]>(this.chefs);

  constructor(private http: HttpClient) {}

  getChefs() {
    this.http
      .get<IUser[]>(this.apiUrl + `chefs`)
      .pipe(map((resp: any) => resp.items))
      .subscribe(
        (chef) => {
          console.log(chef);
          this.chefs$.next(chef);
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
