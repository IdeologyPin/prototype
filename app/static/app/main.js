/**
 * Created by sasinda on 9/10/16.
 */

(function(app) {
  document.addEventListener('DOMContentLoaded', function() {
    ng.platformBrowserDynamic
      .platformBrowserDynamic()
      .bootstrapModule(app.MainModule);
  });
})(window.app || (window.app = {}));