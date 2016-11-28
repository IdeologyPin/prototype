/**
 * Created by Omri on 11/27/16.
 */
declare var Util: any;

import { Component, OnInit, ElementRef, ViewEncapsulation } from '@angular/core';
import { Router, ActivatedRoute, Params }   from '@angular/router';
import { BratEmbedService } from './service'
import { Annotation } from './models'

// import { head } from '../assets/brat_embed/client/head.load.min.js';
// import { head } from '../assets/brat_embed/client/head.load.min.js';
// import '../assets/brat_embed/client/lib/jquery.min.js';
import '../assets/brat_embed/client/lib/jquery.svg.min.js';
import '../assets/brat_embed/client/lib/jquery.svgdom.min.js';
import '../assets/brat_embed/client/lib/webfont.js';
import '../assets/brat_embed/client/src/configuration.js';
import '../assets/brat_embed/client/src/util.js';
import '../assets/brat_embed/client/src/annotation_log.js';
import '../assets/brat_embed/client/src/dispatcher.js';
import '../assets/brat_embed/client/src/url_monitor.js';
import '../assets/brat_embed/client/src/visualizer.js';

@Component({
    selector: 'annotation',
    templateUrl:'./template/brat.xhtml',
    styleUrls: [ '../assets/brat_embed/jquery-theme/jquery-ui.css',
                 '../assets/brat_embed/jquery-theme/jquery-ui-redmond.css', 
                 '../assets/brat_embed/style-vis.css',
                 '../assets/brat_embed/style-ui.css'],
    encapsulation: ViewEncapsulation.None
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
            this.annotation = this.embedService.getArticleAnnotation(id);
            // this.embedService.getArticleAnnotation(id).then(storyList=> {
                // TBD: when service is converted to return promises, implement as callback
            // })
            

            
        });

        var collData = {
            entity_types: [
                {
                    type: 'KeyTerm',
                    labels: ['Key Term', 'Key'],
                    bgColor: '#22A3CB',
                    borderColor: 'darken'
                }, {
                    type: 'PosSentiment',
                    labels: ['Positive Sentiment', 'Pos'],
                    bgColor: '#2DE891',
                    borderColor: 'darken'
                }, {
                    type: 'Sentiment',
                    labels: ['Sentiment', 'Sen'],
                    bgColor: '#2DE891',
                    borderColor: 'darken'
                }, {
                    type: 'NegSentiment',
                    labels: ['Negative Sentiment', 'Neg'],
                    bgColor: '#FAB3BB',
                    borderColor: 'darken'
                }, {
                    type: 'Entity',
                    labels: ['Entity', 'Ent'],
                    bgColor: '#22F3CB',
                    borderColor: 'darken'
                }]};
        var docData = {
            text: this.annotation.text,
            entities : this.annotation.entities 
        };
        var webFontURLs = [
                '../assets/brat_embed/fonts/Astloch-Bold.ttf',
                '../assets/brat_embed/fonts/PT_Sans-Caption-Web-Regular.ttf',
                '../assets/brat_embed/fonts/Liberation_Sans-Regular.ttf'
            ];

        Util.embed( 'brat',
                // object containing collection data
                collData,
                // object containing document data
                docData,
                // Array containing locations of the visualisation fonts
                webFontURLs
        );
    }
}
