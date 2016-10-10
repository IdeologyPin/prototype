/**
 * Created by sasinda on 9/28/16.
 */
import {Component, Input, ElementRef} from '@angular/core';
import {ClusteringService} from './service'
import {ActivatedRoute, Params}   from '@angular/router';
import {Location}                 from '@angular/common';


@Component({
    selector: 'clustering',
    template: `
    <p>Cluster 1</p>
    <div id="foo" class="list-group">
    <div class="list-group-item"> Doc1 <a href="http://rubaxa.github.io/Sortable/">Sortable</a></div>
    <div class="list-group-item"> Doc2 </div>
    <div class="list-group-item"> Doc3 </div>
    <div class="list-group-item"> Doc4 </div>
    <div class="list-group-item"> Doc5 </div>
  </div>
  
  
   <p>Cluster 2</p>
    <div id="bar" class="list-group">
    <div class="list-group-item"> Doc6 <a href="http://rubaxa.github.io/Sortable/">Sortable</a></div>
    <div class="list-group-item"> Doc7 </div>
    <div class="list-group-item"> Doc8 </div>
    <div class="list-group-item"> Doc9 </div>
    <div class="list-group-item"> Doc10 </div>
  </div>
  
  
  `
})
export class ClusterListComponent {
    constructor(private clustering:ClusteringService) {

    }

    ngAfterViewInit() {
        var foo = document.getElementById("foo");
        Sortable.create(foo,{group: 'clusters'})

        var bar = document.getElementById("bar");
        Sortable.create(bar, {group: 'clusters'})
    }
}