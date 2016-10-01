/**
 * Created by sasinda on 9/10/16.
 */
import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {ClusteringService} from './service'

import {AppComponent} from './app.component'
import {SearchComponent} from './search.component'
import {ClusterComponent} from './clust.component'
import {} from './clust-list.component'
import {} from './clust-pinned-map.componenet'
import {StoryComponent} from './story.component'
import { routing } from './app.routing';

@NgModule({
  imports:[ BrowserModule, routing ],
  declarations:[AppComponent, SearchComponent, ClusterComponent, StoryComponent],
  bootstrap:[AppComponent],
  providers:[ClusteringService]
})
export class AppModule { }