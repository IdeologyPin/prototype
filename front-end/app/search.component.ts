/**
 * Created by sasinda on 9/10/16.
 */
import {Component, OnInit} from '@angular/core';
import {StoryService,TaxoService} from './service'
import {Subject} from './models'
@Component({
    selector: 'search-box',
    template: ` <li>
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown">
                        <input type="text" > <i class="fa fa-search"></i>
                     </a>
                </li>
                <p>{{subjects[0].name}}</p>
               `,
    providers:[]
})
export class SearchComponent implements OnInit {
    subjects=[]
    
    constructor(private taxoService: TaxoService) {
        let s=new Subject();
        s._id=1212
        s.name='Initializing'
        this.subjects=[s]
    }

    ngOnInit():void {
        this.taxoService.getAllSubjects().then(subList=>{
            this.subjects=subList.subjects;}
        )

    }
}