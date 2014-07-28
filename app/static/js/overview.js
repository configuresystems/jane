function logCount() {
    var self = this;
    self.countUrl = window.location.origin+'/api/overview/count';
    self.logs = ko.observableArray();
    self.filters = [];
    self.ajax = function(uri, method, data) {
        var request = {
            url: uri,
            type: method,
            contentType: "application/json",
            accepts: "application/json",
            cache: false,
            dataType: 'json',
            data: {"q": JSON.stringify({"filters":self.filters})},
            success: function(text) {
                $('#connection-danger').hide();
                $('#connection-lost').text("");
            },
            error: function(text) {
                $('#connection-danger').show();
                $('#connection-lost').text("Connection with the API has been lost.");
                console.log("ajax error " + jqXHR.status);
            }
        };
        return $.ajax(request);
    }

    self.ajax(self.countUrl, 'GET').done(function(data) {
        for (var i = 0; i < data.logs.length; i++) {
            if ( data.logs[i].name == 'success' ) {
                var status = 'panel panel-success';
                var icon = 'fa fa-check-circle fa-5x';
                var message = 'Success Logs';
                var uri = '/logging/success';
            } else if (data.logs[i].name == 'domains' ) {
                var status = 'panel panel-success';
                var icon = 'fa fa-globe fa-5x';
                var message = 'Domains';
                var uri = '/domains';
            } else if (data.logs[i].name == 'users' ) {
                var status = 'panel panel-success';
                var icon = 'fa fa-users fa-5x';
                var message = 'Users';
                var uri = '/users';
            } else {
                var status = 'panel panel-danger';
                var icon = 'fa fa-warning fa-5x';
                var message = 'Error Logs';
                var uri = '/logging/error';
            }
            self.logs.push({
                status: ko.observable(status),
                icon: ko.observable(icon),
                uri: ko.observable(uri),
                message: ko.observable(message),
                name: ko.observable(data.logs[i].name),
                count: ko.observable(data.logs[i].count)
            });
        }
    });
}
ko.applyBindings(new logCount(), $('#notifications')[0]);
