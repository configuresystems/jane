function logList() {
    var self = this;
    self.Url = window.location.origin+'/api'+window.location.pathname;
    self.data_set = ko.observableArray();
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

    self.ajax(self.Url, 'GET').done(function(data) {
        for (var i = 0; i < data.logs.length; i++) {
            for (var x = 0; x < data.logs[i].logging_details.length; x++) {
                if (data.logs[i].logging_details[x].status_code == 'success') {
                    var status = 'success gradeX';
                    var icon = 'fa fa-check';
                } else {
                    var status = 'danger gradeX';
                    var icon = 'fa fa-warning';
                }
                if (data.logs[i].logging_details[x].module == 'domain') {
                    var module = 'text-center fa fa-globe';
                } else if ( data.logs[i].logging_details[x].module == 'user') {
                    var module = 'text-center fa fa-user';
                }

                self.data_set.push({
                    status: ko.observable(status),
                    icon: ko.observable(icon),
                    module: ko.observable(module),
                    action: ko.observable(data.logs[i].logging_details[x].action),
                    message: ko.observable(data.logs[i].logging_details[x].message),
                    count: ko.observable(data.count)
                });
            }
        }
    });
}
ko.applyBindings(new logList(), $('#logging')[0]);
