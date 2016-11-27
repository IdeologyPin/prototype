/**
 * Created by Omri on 11/27/16.
 */
import { Component, OnInit, ElementRef } from '@angular/core';
import { Router, ActivatedRoute, Params }   from '@angular/router';
import { BratEmbedService } from './service'
import { Annotation } from './models'

@Component({
    selector: 'annotation',
    // template: ` <div class="container" >
    // 				<div class="title" >
    //                     Article Source: {{annotation.source}}
    //                     <br> Article Title: {{annotation.title}}
    //                     <br> <a href="{{annotation.link}}" target="_blank"> Link to Original </a>
    //                 </div>
    // 			</div>
    //           `
    templateUrl:'./template/brat.xhtml'
})

export class AnnotationComponent implements OnInit {
    
    public elementRef;
    public annotation;

    constructor(private embedService:BratEmbedService,
                myElement:ElementRef,
                private route:ActivatedRoute,
                private router:Router) {

        let a = new Annotation();
        a._id = "1"
        a.title = 'test title'
        this.annotation = a
        this.elementRef = myElement;
    }

    ngOnInit():void {
        this.route.params.forEach((params:Params) => {
            let id = params['story_id']; // (+) converts string 'id' to a number
            console.log(id);
            this.annotation = this.embedService.getArticleAnnotation(id);
            // this.embedService.getArticleAnnotation(id).then(storyList=> {
                // TBD: when service is converted to return promises, implement as callback
            // })

        });
    }
}
