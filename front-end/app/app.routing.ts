/**
 * Created by sasinda on 9/29/16.
 */
import {ModuleWithProviders}  from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {StoryComponent} from './story.component'
import {ClusterComponent}      from './clust.component';
import {ClusterListComponent} from "./clust-list.component";
import {AnnotationComponent} from "./annotation.component";
import {EntityDiveComponent} from "./entitydive.component";
import {AppComponent} from "./app.component";

const appRoutes:Routes = [
    // {
    //     path: '',
    //     redirectTo: '/app',
    //     pathMatch: 'full'
    //     // component: AppComponent
    // },
    {
        path: 'clustering/:id',
        component: ClusterListComponent
    },
    {
        path: 'stories',
        component: StoryComponent
    },
    {
        path: 'subject/:subject_id',
        component: StoryComponent
    },
    {
        path: 'subject/:subject_id/stories',
        component: StoryComponent
    },
    {
        path: 'annotation/:story_id',
        component: AnnotationComponent
    },
    {
        path: 'deepdive/:story_id',
        component: EntityDiveComponent
    }
];
export const routing:ModuleWithProviders = RouterModule.forRoot(appRoutes);