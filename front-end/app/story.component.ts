/**
 * Created by sasinda on 9/29/16.
 */
import {Component, OnInit, ElementRef} from '@angular/core';
import {Router, ActivatedRoute, Params}   from '@angular/router';
import {StoryService, ClusteringService} from './service'
import {Story} from './models'

@Component({
    selector: 'story-list',
    template: ` 
                Please select analysis method: <select>
                    <option value="FV1">FV1</option>
                    <option value="LDA">LDA (TBD)</option>
                </select> <br>
                Top Trending Stories
    			<div class="container" >
    				<div class="stories" *ngIf="storyList.length > 0">
                        <ul *ngFor='let item of storyList; let i=index' >
                            <div *ngIf="i<10" class="list-group-item">
                                <a  (click)='select(item)'  >{{item.headline}} </a>
                                <div class="article_link"> <a href={{item.url}} target="_blank"> [Example]</a></div>
                                <div class="deep_dive_link"><a (click) = 'deepdive(item)'>[Entity Deep Dive]</a></div>
                                <div class="deep_dive_link"><a (click) = 'select(item)'>[Analysis Results]</a></div>
                            </div>
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
    public clusteringsList;
    public subject;


    constructor(private storyService:StoryService,
                myElement:ElementRef,
                private route:ActivatedRoute,
                private clusteringService:ClusteringService,
                private router:Router) {
        let s = new Story();
        s._id = "1"
        s.headline = 'Initializing'
        this.stories = [s]
        this.elementRef = myElement;
        this.subject = 'temp';
    }

    ngOnInit():void {
        this.route.params.forEach((params:Params) => {
            let id = params['subject_id']; // (+) converts string 'id' to a number
            console.log(id);
            this.storyService.getTrending(id).then(storyList=> {
                console.log(storyList);
                this.stories = storyList.stories;
                for (var i = 0; i < storyList.stories.length; i++) {
                    this.storyList.push(storyList.stories[i]);
                    // console.log(storyList.stories[i].id);
                    console.log(storyList.stories[i].headline);
                }
            })
        });
    }

    select(item) {
        this.selectedStory = item;
        console.log(item);
        this.router.navigate(['/clustering', item.id]);
        // this.clusteringService.getStoryClustering(item.id).then(clusteringsList=>{
        // this.router.navigate(['/clustering', clusteringsList.clusterings[0]._id]);
        // OMRI: Right now only taking the first Clustering ID; needs to find better algorithm for this
    }

    deepdive(item) {
        console.log("test button")
        this.selectedStory = item;
        console.log(item);
        this.router.navigate(['/deepdive', item.id]);
    }
}
