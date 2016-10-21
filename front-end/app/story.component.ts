/**
 * Created by sasinda on 9/29/16.
 */
import { Component, OnInit, ElementRef } from '@angular/core';
import { ActivatedRoute, Params }   from '@angular/router';
import { StoryService, ClusteringService } from './service'
import { Story } from './models'

@Component({
    selector: 'story-list',
    template: ` analyzed stories table
    			<div class="container" >
    				<div class="stories" *ngIf="storyList.length > 0">
                        <ul *ngFor='let item of storyList; let i=index' >
                            <li *ngIf="i<10">
                                <a  (click)='select(item)'  >{{item.headline}} </a>
                                <div class="article_link"> <a href={{item.url}} target="_blank"> [Original]</a></div>
                            </li>
                        </ul>
                    </div>
    			</div>
              `
})

export class StoryComponent implements OnInit {
	stories = []

	public storyList = [];
	public urlList = [];
	public elementRef;
	public selectedStory;
	public test;

	constructor(private storyService: StoryService, 
						myElement: ElementRef, 
				private route: ActivatedRoute,
				private clusteringService: ClusteringService) {
        let s=new Story();
        s._id=1
        s.headline='Initializing'
        this.stories=[s]
        

        this.elementRef = myElement;
    }

    ngOnInit():void {
        this.route.params.forEach((params: Params) => {
		    let id = params['subject_id']; // (+) converts string 'id' to a number
		    console.log(id);
		    this.storyService.getTrending(id).then(storyList=>{
	            this.stories=storyList.stories;
	            for (var i = 0; i < storyList.stories.length; i++) { 
	                this.storyList.push(storyList.stories[i]);
	                // this.urlList.push(storyList.stories[i].url);
	                console.log(storyList.stories[i].headline);
	            }
	        })
		});
    }

    select(item) {
        this.selectedStory = item;
        console.log(item);
        this.clusteringService.getStoryClustering(item.id).then(test=>{
            console.log(test);
        })
    }
}