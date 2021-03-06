import {Injectable} from '@angular/core';
import {Headers, Http}    from '@angular/http';
import 'rxjs/add/operator/toPromise';
import {Clustering, ClusteringList, SubjectList, StoriesList, Annotation} from './models'


const API_HOST = 'http://localhost:5000'

@Injectable()
export class ClusteringService {
    private api_url = API_HOST + '/clustering/story/';
    constructor(private http:Http) {
    }
    
    getStoryClustering(storyId):Promise<ClusteringList> {
        return this.http.get(this.api_url+storyId)
            .toPromise()
            .then(response => response.json() as ClusteringList)
            .catch(this.handleError);
    }
    
    private handleError(error:any):Promise<any> {
        console.error('An error occurred', error); // for demo purposes only
        return Promise.reject(error.message || error);
    }
}

@Injectable()
export class AnalysisService {
    // private api_url = API_HOST + '/clustering/story/';
    constructor(private http:Http) {
    }
    
    getAllAnalysisMethods():string[] {
        return ["FV1", "LDA (TBD)"];
    }
    
    private handleError(error:any):Promise<any> {
        console.error('An error occurred', error); // for demo purposes only
        return Promise.reject(error.message || error);
    }
}

@Injectable()
export class StoryService {
    private api_url = API_HOST + '/story/trending/';
    constructor(private http:Http) {
    }

    getTrending(subjectId):Promise<StoriesList> {
        return this.http.get(this.api_url+subjectId)
            .toPromise()
            .then(response => response.json() as StoriesList)
            .catch(this.handleError);
    }

    

    private handleError(error:any):Promise<any> {
        console.error('An error occurred', error); // for demo purposes only
        return Promise.reject(error.message || error);
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
            .then(response => response.json() as SubjectList)
            .catch(this.handleError);
    }

    private handleError(error:any):Promise<any> {
        console.error('An error occurred', error); // for demo purposes only
        return Promise.reject(error.message || error);
    }
}

@Injectable()
export class EntityDiveService {

    // private api_url = API_HOST + '/taxonomy/subjects/';

    private title = "More minorities buying guns following Donald Trump’s election";
    private storyID = 801545936543309824;
    private entities = ["Donald Trump", "gun control measures", "Smith & Wesson", "minorities"];
    private clusters = {
        "Donald Trump": {"positive": [], "negative": [0,1,2]},
        "gun control measures": {"positive": [0,2], "negative": [1]},
        "Smith & Wesson": {"positive": [1,2], "negative": [0]},
        "minorities": {"positive": [0], "negative": [1,2]}
    };

    private articles = {
        0:{"id":"eL2Ks4|1479997942658201000", "title":"Trump's Presidency Is Likely To Have A Big Effect On US Gun Sales", "source":"Newsy Partner Feed", url:"http://www.newsy.com/videos/gun-stores-report-decrease-in-sales-after-trump-s-election/", "publish_date": "2016-11-24"},
        1:{"id":"A1fVb6|148002575367670500", "title":"Gun sales among black community surges after Trump’s victory due to fears of racism", "source":"TheBlaze.com", url:"http://www.theblaze.com/news/2016/11/24/gun-sales-among-black-community-surges-after-trumps-victory-due-to-fears-of-racism/", "publish_date": "2016-11-24"},
        2:{"id":"oaVWlG|1479963106856234000", "title":"Gun Store Owners Seeing Slow Down In Sales Since Trump Victory", "source":"CBS Pittsburgh", url:"http://pittsburgh.cbslocal.com/2016/11/23/gun-store-owners-seeing-slow-down-in-sales-since-trump-victory/", "publish_date": "2016-11-23"}
    };

    constructor(private http:Http) {
    }

    getArticleInfoByID(articleID):{} {
        return this.articles[articleID];
    }

    getAllEntities():String[] {
        return this.entities;
    }

    getClustersByEntity(entityName):{} {
        return this.clusters[entityName];
    }

    getAllClusterings():{} {
        return this.clusters;
    }

    getAllArticleDetails():{} {
        return this.articles;
    }

    getTitle():string {
        return this.title
    }


    private handleError(error:any):Promise<any> {
        console.error('An error occurred', error); // for demo purposes only
        return Promise.reject(error.message || error);
    }
}


@Injectable()
export class BratEmbedService {

    // TBD, create API endpoint
    private api_url = API_HOST + '/articles/';

    constructor(private http:Http) {
    }

    // TBD, make call to API and get article annotations!
    // getArticleAnnotation(articleId):Promise<Annotation> {
    //     return this.http.get(this.api_url + articleId)
    //         .toPromise()
    //         .then(response => response.json() as Annotation)
    //         .catch(this.handleError);

    // }

    // getArticleAnnotation(articleId):Annotation {
    getArticleAnnotation(articleId):Promise<Annotation> {
    return this.http.get(this.api_url + articleId)
        .toPromise()
        .then(response => response.json() as Annotation)
        .catch(this.handleError);
        // var tempData =  new Annotation();
        //     tempData._id = "GqaYlT1479246237866992000";
        //     // tempData.entities = [ [ "T1", "KeyTerm", [ [ 747, 765 ] ] ], [ "T2", "KeyTerm", [ [ 98, 119 ] ] ], [ "T3", "KeyTerm", [ [ 544, 556 ] ] ], [ "T4", "KeyTerm", [ [ 278, 289 ] ] ], [ "T5", "KeyTerm", [ [ 1037, 1052 ] ] ], [ "T6", "KeyTerm", [ [ 998, 1013 ] ] ], [ "T7", "KeyTerm", [ [ 1724, 1739 ] ] ], [ "T8", "KeyTerm", [ [ 57, 62 ] ] ], [ "T9", "KeyTerm", [ [ 323, 329 ] ] ], [ "T10", "KeyTerm", [ [ 1543, 1560 ] ] ], [ "T11", "Sentiment", [ [ 0, 183 ] ] ], [ "T12", "Sentiment", [ [ 184, 374 ] ] ], [ "T13", "Sentiment", [ [ 375, 499 ] ] ], [ "T14", "Sentiment", [ [ 500, 702 ] ] ], [ "T15", "Sentiment", [ [ 703, 881 ] ] ], [ "T16", "Sentiment", [ [ 882, 913 ] ] ], [ "T17", "Sentiment", [ [ 913, 1053 ] ] ], [ "T18", "Sentiment", [ [ 1054, 1185 ] ] ], [ "T19", "Sentiment", [ [ 1185, 1298 ] ] ], [ "T20", "Sentiment", [ [ 1299, 1538 ] ] ], [ "T21", "Sentiment", [ [ 1539, 1793 ] ] ], [ "T22", "Sentiment", [ [ 1794, 1915 ] ] ], [ "T23", "Sentiment", [ [ 1916, 2274 ] ] ], [ "T24", "Sentiment", [ [ 2275, 2276 ] ] ], [ "T25", "Sentiment", [ [ 2276, 2690 ] ] ], [ "T26", "Sentiment", [ [ 2691, 2835 ] ] ], [ "T27", "Sentiment", [ [ 2836, 2981 ] ] ], [ "T28", "Sentiment", [ [ 2982, 3044 ] ] ] ];
        //     tempData.entities = [
        //         [ "T1", "KeyTerm", [[87, 112 ]]],
        //         ["T2", "KeyTerm", [[19, 29]]],
        //         ["T3", "KeyTerm", [[91, 99]]],
        //         ["T4", "KeyTerm", [[387, 394]]],
        //         ["T5", "KeyTerm", [[556, 563]]],
        //         ["T6", "KeyTerm", [[742, 751]]],
        //         ["T7", "PosSentiment", [[0, 187]]],
        //         ["T8", "PosSentiment", [[188, 278]]],
        //         ["T9", "PosSentiment", [[407, 540]]],
        //         ["T10", "PosSentiment", [[541, 600]]],
        //         ["T11", "NegSentiment", [[279, 406]]],
        //         ["T12", "NegSentiment", [[601, 662]]],
        //         ["T13", "NegSentiment", [[663, 825]]],
        //         ["T14", "Entity", [[121, 144]]],
        //         ["T15", "Entity", [[279, 386]]],
        //         ["T16", "Entity", [[71, 79]]],
        //         ["T17", "Entity", [[785, 800]]]
        //     ];
        //     tempData.file_name = "GqaYlT|1479246237866992000";
        //     tempData.link = "http://www.commondreams.org/news/2016/11/15/local-gun-restrictions-could-be-eviscerated-under-trump"; 
        //     tempData.snippet = "Facing a looming Republican-dominated Congress under the right-wing President-elect Donald Trump, gun control advocates warn that local gun restrictions are about to be \"eviscerated.\"";
        //     tempData.source = "News";
        //     tempData.story = 798624024653807616;
        //     // tempData.text = "Facing a looming Republican-dominated Congress under the right-wing President-elect Donald Trump, gun control advocates warn that local gun restrictions are about to be \"eviscerated.\" Many Republican members of Congress have long sought to pass sweeping national right-to-carry legislation , to force \"reciprocity\" between states when it comes to right-to-carry legislation. Reciprocity legislation has been a major priority of the National Rifle Association (NRA), which endorsed Trump's candidacy. Under such a law, a person with a concealed-carry permit in West Virginia would be able to legally carry a firearm in New York City as well, avoiding the city's lengthy and expensive permitting process. It would also allow residents of areas with strict gun control to travel to states with loose restrictions, purchase a gun, and legally carry that gun when they return back home. The Guardian reported Monday: \"Trump, who himself has a permit to carry a concealed firearm, has already endorsed a new reciprocity law as part of his gun rights platform. Concealed-carry permits from one state 'should be valid in all 50 states,' his platform reads, calling the proposal 'common sense.'\" The president-elect also promised to appoint judges with a right-wing stance on guns to the U.S. Supreme Court. Purchasing a firearm in many locales is already extremely easy, and a \"growing number of states\u201410 and counting [...] require no permit at all to carry a concealed weapon, a policy often called 'constitutional carry,'\" writes the Guardian. The newspaper reports: The Law Center to Prevent Gun Violence argues reciprocity would create a ' lowest common denominator standard' for gun carrying across the country, 'eviscerating state authority to restrict who may carry guns within their borders.' Shannon Watts, the founder of Moms Demand Action for Gun Sense in America, called carry reciprocity 'a dangerous policy.' \"I only hope President-elect Trump recognizes that nine out of 10 Americans, regardless of who they supported for president, want to create a safer America by expanding Brady background checks to every gun sale,\" said Dan Gross, president of the Brady Campaign, a national group that fights for stricter gun control, in response to the presidential election. \"And while we're hopeful we can work with President-elect Trump to reduce gun deaths in this country, we are also prepared to fight with everything we've got to ensure the vision he described on the campaign trail of an America where every domestic abuser, terrorist, and felon can carry a loaded gun anytime, anywhere\u2014where problems are solved with bullets instead of words\u2014will never become reality,\" Gross added. Yet many gun control advocates are fairly pessimistic about their chances of fighting such a law in a Republican-dominated Congress under Trump. Adam Winkler, a gun politics expert at the University of California Los Angeles, explained to the Guardian : \"Right now, the NRA has got its way. It's not clear why it would be looking for major compromises.\"";
        //     tempData.text = "BELEN, N.M. (AP) - Democratic lawmakers have named Sen. Peter Wirth of Santa Fe as the new majority floor leader for the New Mexico state Senate to replace departing Sen. Michael Sanchez. Wirth was named majority leader by Democratic senators during a meeting Saturday in Belen. Senate Democrats re-nominated Mary Kay Papen of Las Cruces as Senate president, pending confirmation by the chamber in January. Sen. Michael Padilla of Bernalillo was chosen as majority whip and Sen. Jacob Candelaria of Bernalillo will be majority caucus chair. Democrats will control both legislative chambers next year. Republicans lost control of the House in the Nov. 8 election. Sanchez lost his seat to Republican Greg Baca amid a wave of attack ads from a political committee run by Republican Gov. Susana Martinez's top political adviser.";
        //     tempData.title = "Local Gun Restrictions Could be 'Eviscerated' Under Trump";

        // return tempData;

    }

    private handleError(error:any):Promise<any> {
        console.error('An error occurred', error); // for demo purposes only
        return Promise.reject(error.message || error);
    }
}