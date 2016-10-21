/**
 * Created by sasinda on 9/10/16.
 */
import { Component, OnInit, ElementRef } from '@angular/core';
import { RouterModule, Router }   from '@angular/router';
import { StoryService, TaxoService } from './service'
import { Subject } from './models'


@Component({
    selector: 'search-box',
    host: {
        '(document:click)': 'handleClick($event)',
    },
    template: ` 
                <div class="container" >
                    <div class="dropdown-toggle" data-toggle="dropdown">
                        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                          <input id="subjects" type="text" [(ngModel)]=query (keyup)=filter()>
                          <i class="fa fa-search"></i>
                        </a>
                    </div>
                    <div class="suggestions" *ngIf="filteredList.length > 0">
                        <ul *ngFor='let item of filteredList; let i=index' >
                            <li *ngIf="i<10">
                                <a (click)='select(item)' >{{item}}</a>
                            </li>
                        </ul>
                    </div>
                </div> 
               `,
    providers:[]
})
export class SearchComponent implements OnInit {
    subjects=[]

    public query = '';
    public filteredList = [];
    public elementRef;
    public subjectList = [''];
    public selectedSubjectId;
    
    constructor(private taxoService: TaxoService, myElement: ElementRef, private router:Router) {
        let s=new Subject();
        s._id=1212
        s.name='Initializing'
        this.subjects=[s]
        

        this.elementRef = myElement;
    }

    ngOnInit():void {
        this.taxoService.getAllSubjects().then(subList=>{
            this.subjects=subList.subjects;
            for (var i = 0; i < subList.subjects.length; i++) { 
                // console.log(subList.subjects[i]); 
                this.subjectList.push(subList.subjects[i].name);
            }
        })

    }

    filter() {
        if (this.query !== "") {
            this.filteredList = this.subjectList.filter(function(el){
                return el.toLowerCase().indexOf(this.query.toLowerCase()) > -1; 
            }.bind(this));
        } else {
            this.filteredList = [];
        }
    }
 
    select(item) {
        this.query = item;
        this.filteredList = [];
        this.getStoriesBySubjectName(item);
    }

    handleClick(event) {
        var clickedComponent = event.target;
        var inside = false;
        do {
            if (clickedComponent === this.elementRef.nativeElement) {
               inside = true;
            }
        clickedComponent = clickedComponent.parentNode;
        } while (clickedComponent);
        if(!inside) {
            this.filteredList = [];
        }
    }

    getStoriesBySubjectName(name) {
        for (var i = 0; i < this.subjects.length; i++) { 
            if(this.subjects[i].name == name) { this.selectedSubjectId = this.subjects[i]._id }
        }
        console.log(this.selectedSubjectId);
        this.router.navigate(['/subject', this.selectedSubjectId]);
        // OMRI | TBD: use this.this.selectedSubjectId to trigger call to stories API and generate the list of stories.
    }    

}