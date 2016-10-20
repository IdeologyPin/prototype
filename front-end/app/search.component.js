"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
/**
 * Created by sasinda on 9/10/16.
 */
var core_1 = require('@angular/core');
var service_1 = require('./service');
var models_1 = require('./models');
var SearchComponent = (function () {
    function SearchComponent(taxoService, myElement) {
        this.taxoService = taxoService;
        this.subjects = [];
        this.query = '';
        this.filteredList = [];
        this.subjectList = [''];
        var s = new models_1.Subject();
        s._id = 1212;
        s.name = 'Initializing';
        this.subjects = [s];
        this.elementRef = myElement;
    }
    SearchComponent.prototype.ngOnInit = function () {
        var _this = this;
        this.taxoService.getAllSubjects().then(function (subList) {
            _this.subjects = subList.subjects;
            for (var i = 0; i < subList.subjects.length; i++) {
                // console.log(subList.subjects[i]); 
                _this.subjectList.push(subList.subjects[i].name);
            }
        });
    };
    SearchComponent.prototype.filter = function () {
        if (this.query !== "") {
            this.filteredList = this.subjectList.filter(function (el) {
                return el.toLowerCase().indexOf(this.query.toLowerCase()) > -1;
            }.bind(this));
        }
        else {
            this.filteredList = [];
        }
    };
    SearchComponent.prototype.select = function (item) {
        this.query = item;
        this.filteredList = [];
        this.getStoriesBySubjectName(item);
    };
    SearchComponent.prototype.handleClick = function (event) {
        var clickedComponent = event.target;
        var inside = false;
        do {
            if (clickedComponent === this.elementRef.nativeElement) {
                inside = true;
            }
            clickedComponent = clickedComponent.parentNode;
        } while (clickedComponent);
        if (!inside) {
            this.filteredList = [];
        }
    };
    SearchComponent.prototype.getStoriesBySubjectName = function (name) {
        for (var i = 0; i < this.subjects.length; i++) {
            if (this.subjects[i].name == name) {
                this.selectedSubjectId = this.subjects[i]._id;
            }
        }
        console.log(this.selectedSubjectId);
        // OMRI | TBD: use this.this.selectedSubjectId to trigger call to stories API and generate the list of stories.
    };
    SearchComponent = __decorate([
        core_1.Component({
            selector: 'search-box',
            host: {
                '(document:click)': 'handleClick($event)',
            },
            template: " \n                <div class=\"container\" >\n                    <div class=\"dropdown-toggle\" data-toggle=\"dropdown\">\n                        <a href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\">\n                          <input id=\"subjects\" type=\"text\" [(ngModel)]=query (keyup)=filter()>\n                          <i class=\"fa fa-search\"></i>\n                        </a>\n                    </div>\n                    <div class=\"suggestions\" *ngIf=\"filteredList.length > 0\">\n                        <ul *ngFor='let item of filteredList; let i=index' >\n                            <li *ngIf=\"i<10\">\n                                <a (click)='select(item)' >{{item}}</a>\n                            </li>\n                        </ul>\n                    </div>\n                </div> \n               ",
            providers: []
        }), 
        __metadata('design:paramtypes', [service_1.TaxoService, core_1.ElementRef])
    ], SearchComponent);
    return SearchComponent;
}());
exports.SearchComponent = SearchComponent;
//# sourceMappingURL=search.component.js.map