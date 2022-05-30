import { ChefsService } from './../../service/chefs.service';
import { Component, OnInit } from '@angular/core';
import { IUser } from '../models/user';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-chefs',
  templateUrl: './chefs.component.html',
  styleUrls: ['./chefs.component.scss'],
})
export class ChefsComponent implements OnInit {
  chefs: any[] = [];
  chefsSubscription!: Subscription;

  constructor(private chefsService: ChefsService) {
    console.log('chefs', this.chefs);
  }

  ngOnInit(): void {
    this.chefsService.getChefs();
    this.chefsSubscription = this.chefsService.chefs$.subscribe((chef) => {
      this.chefs = chef;
    });
  }

  getChefs() {}

  ngOnDestroy() {
    this.chefsSubscription.unsubscribe();
  }
}
