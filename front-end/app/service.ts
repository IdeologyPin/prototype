import {Injectable} from '@angular/core';
import {Headers, Http}    from '@angular/http';
import 'rxjs/add/operator/toPromise';
import {Clustering, SubjectList} from './models'


const API_HOST = 'http://localhost:5000'

@Injectable()
export class ClusteringService {

    getStoryClustering():Clustering {
        return null;
    }
}

@Injectable()
export class StoryService {

    getTrending(subjectId):void {

    }
}


@Injectable()
export class TaxoService {

    private api_url = API_HOST + '/taxonomy/subjects/';

    constructor(private http:Http) {
    }

    getAllSubjects():Promise<SubjectList> {
        return this.http.get(this.api_url)
            .toPromise()
            .then(response => JSON.parse(response.json()) as SubjectList)
            .catch(this.handleError);
    }

    private handleError(error:any):Promise<any> {
        console.error('An error occurred', error); // for demo purposes only
        return Promise.reject(error.message || error);
    }
}