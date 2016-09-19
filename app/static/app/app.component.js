/**
 * Created by sasinda on 9/10/16.
 */
(function(app) {
  app.SearchComponent =
    ng.core.Component({
      selector: 'search-box',
      template: '<input type="text" >'
    })
    .Class({
      constructor: function() {}
    });
})(window.app || (window.app = {}));