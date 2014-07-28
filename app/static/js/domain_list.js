function domainList() {
    var self = this;
    self.domainUrl = window.location.origin+'/api/domains';
    self.domains = ko.observableArray();
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

    self.ajax(self.domainUrl, 'GET').done(function(data) {
        for (var i = 0; i < data.domains.length; i++) {
            var status = 'success gradeX';
            var icon = 'fa fa-check';
            var uri = '/domains/'+data.domains[i].domain_name;
            var domain_url = 'http://'+data.domains[i].domain_name;

            self.domains.push({
                status: ko.observable(status),
                icon: ko.observable(icon),
                uri: ko.observable(uri),
                name: ko.observable(data.domains[i].domain_name),
                domain_url: ko.observable(domain_url),
                count: ko.observable(data.count)
            });
        }
    });
}
ko.applyBindings(new domainList(), $('#domains')[0]);
