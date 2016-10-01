/**
 * Created by sasinda on 9/29/16.
 */
import {ModuleWithProviders}  from '@angular/core';
import {Routes, RouterModule} from '@angular/router';
import {StoryComponent} from './story.component'
import {ClusterComponent}      from './clust.component';

const appRoutes:Routes = [
    {
        path: '',
        redirectTo: '/stories',
        pathMatch: 'full'
    },
    {
        path: 'clustering/:id',
        component: ClusterComponent
    },
    {
        path: 'stories',
        component: StoryComponent
    }
];
export const routing:ModuleWithProviders = RouterModule.forRoot(appRoutes);