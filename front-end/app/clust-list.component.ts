/**
 * Created by sasinda on 9/28/16.
 */
import { Component, Input, ElementRef }      from '@angular/core';
import { ClusteringService }                 from './service'
import { ActivatedRoute, Params }            from '@angular/router';
import { Location }                          from '@angular/common';
import { Clustering, Node, Cluster }         from "./models";


@Component({
    selector: 'clustering',
    template: `
                <div *ngFor="let clustering of clusterings">
                    <p>Clustering  : {{clustering.name}}</p>
                </div>
                
                <div class="clustering lists" *ngIf="clustering">
                    <div *ngFor="let cluster of clustering.clusters">
                        <p> Cluster  : {{cluster.name}}</p>
                         <div id="cluster{{cluster.id}}" class="list-group">
                            <div *ngFor="let node of cluster.nodes" class="list-group-item">
                                {{node.label}} <a href="{{node.link}}" target="_blank">view</a>
                            </div>
                         </div>            
                    </div>
                </div>    
              `
})
export class ClusterListComponent {
    protected clusterings:Clustering[]
    protected clustering:Clustering



    constructor(private clusteringService:ClusteringService, private route:ActivatedRoute) {

    }

    ngOnInit():void {
        this.route.params.forEach((params: Params) => {
            let id = params['id'];
            this.clusteringService.getStoryClustering(id).then(cList=> {
                this.clusterings = cList.clusterings;
                this.clustering = cList.clusterings[0]
                let clustering=this.clustering
                let clust_nodes:{ [id: string] : Node[] } = {};

                for(let clust of clustering.clusters){
                    clust_nodes[clust.id]=[]
                }
                for(let node of clustering.nodes){
                    let scores=node.scores
                    for(let cid in scores){
                        if(scores[cid]>0.1){
                            clust_nodes[cid].push(node)
                        }
                    }
                }
                for(let clust of clustering.clusters){
                    clust.nodes=clust_nodes[clust.id]
                }

            })
        });
    }

    ngAfterViewInit() {


        // var bar = document.getElementById("bar");
        // Sortable.create(bar, {group: 'clusters'})
    }
}