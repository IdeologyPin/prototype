/**
 * Created by sasinda on 9/10/16.
 */
(function(app) {
  app.MainModule =
    ng.core.NgModule({
      imports: [ ng.platformBrowser.BrowserModule ],
      declarations: [ app.SearchComponent ],
      bootstrap: [ app.SearchComponent ]
    })
    .Class({
      constructor: function() {}
    });
})(window.app || (window.app = {}));