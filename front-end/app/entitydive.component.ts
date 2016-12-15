/**
 * Created by omri on 12/14/16.
 */
import {Component, OnInit, ElementRef} from '@angular/core';
import {Router, ActivatedRoute, Params}   from '@angular/router';
import {EntityDiveService} from './service'
import {EntityClustering} from './models'


@Component({
    selector: 'entity-dive',
    template: ` 
                Story Title: {{title}} <br>
                Please select an entity from this list: 
                <select [(ngModel)]="selectedEntity" (ngModelChange)='select(value)'>  
                    <option value="">Please select</option>
                    <option *ngFor='let entity of entities' [ngValue]="entity">{{entity}}</option>
                </select> <br>
                <br><br><br><br>
                <entitylist [clustering] = "selectedEntityList" [articles] = "articles"></entitylist>
              `
})

export class EntityDiveComponent implements OnInit {
    public entities;
    public title;
    public clusters = {};
    public articles = {};
    public elementRef;

    public selectedEntity;
    public selectedEntityList;
    
    constructor(private entitydiveService:EntityDiveService,
                myElement:ElementRef,
                private route:ActivatedRoute,
                private router:Router) {
        this.entities = ["test1", "test2"];
        this.elementRef = myElement;
        this.title = 'test title';
        this.articles = {0:{"id":"testID", "title":"test", "source":"test Source", url:"http://www.google.com", "publish_date": "2016-12-14"}};
        this.clusters = { "test1": {"positive": [], "negative": []}, "test2": {"positive": [0], "negative": [0]} };
        this.selectedEntityList = this.clusters["test1"];

    }

    ngOnInit():void {
       console.log("loaded component");
       this.entities = this.entitydiveService.getAllEntities();
       this.title = this.entitydiveService.getTitle();
       this.clusters = this.entitydiveService.getAllClusterings();
       this.articles = this.entitydiveService.getAllArticleDetails();
       console.log(this.title);

    }

    select(val) {
       console.log(this.selectedEntity);
       // this.selectedEntity = val;
       this.selectedEntityList = this.clusters[this.selectedEntity];
       console.log(this.selectedEntityList);
    }
}
