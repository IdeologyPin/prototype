import { Component, Input, OnInit } from '@angular/core';
import { EntityClustering, entityArticles } from './models';
import {Router}   from '@angular/router';

@Component({
  selector: 'entitylist',
  template: `
    <div class="container" >
      <div class="clusters" *ngIf="clustering.positive.length > 0 || clustering.negative.length > 0">
        Positive Stories:
        <ul *ngFor='let item of clustering.positive' >
          <div class="list-group-item"><a  (click)='select(item)'  > {{articles[item].title}} </a></div>
        </ul>
        <br><br>
        Negative Stories:
        <ul *ngFor='let item of clustering.negative' >
          <div class="list-group-item"><a  (click)='select(item)'  > {{articles[item].title}} </a></div>
        </ul>
    </div>
    </div>
  `
})

export class EntityListComponent implements OnInit {
  
  @Input()
  clustering: EntityClustering;
  @Input()
  articles: entityArticles;

  constructor(private router:Router) {

    }

  ngOnInit():void {
    console.log("clustering init");
    console.log(this.clustering);
  }

  select(item) {
    console.log(this.clustering);
    console.log(this.articles);
    console.log(this.articles[item]);
    this.router.navigate(['/annotation', this.articles[item].id);
  }

}