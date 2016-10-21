/**
 * Created by sasinda on 9/29/16.
 */
import {ModuleWithProviders}  from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {StoryComponent} from './story.component'
import {ClusterComponent}      from './clust.component';
import {ClusterListComponent} from "./clust-list.component";

const appRoutes:Routes = [
    // {
    //     path: '',
    //     // redirectTo: '/stories',
    //     pathMatch: 'full'
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
    }
];
export const routing:ModuleWithProviders = RouterModule.forRoot(appRoutes);