function RoutesModel() {
    let self = this;
    self.routes = ko.observableArray([]);
    self.newRoute = ko.observable();
    self.routeHits = ko.observableArray([]);
    self.noData = ko.observable(false);

    self.createRoute = function () {
        $.ajax({
            url: 'http://localhost:5000/api/v1/route/create',
            type: 'POST',
            error: function (jqXHR) {
                console.log("ajax error " + jqXHR.status);
            },
            success: function (data) {
                self.newRoute(data.id);
                self.loadRoutes();
            }
        });
    }

    self.loadRoutes = function () {
        $.getJSON('http://localhost:5000/api/v1/routes', function (data) {
            self.routes(data['data']);
        });
    }
    self.loadRoutes();

    self.showRouteDetails = function (uuid) {
        $.getJSON('http://localhost:5000/api/v1/hits/' + uuid, function (data) {
            self.routeHits(data['data']);
            if (self.routeHits()) {
                self.noData(false);
            }
            else {
                self.noData(true);
            }
        })
            .fail(function () { alert('URL expired, please refresh the page'); });
    }

}


let routesModel = new RoutesModel();
ko.applyBindings(routesModel, $('#routes')[0]);