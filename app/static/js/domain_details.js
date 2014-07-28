function domainDetails() {
    var self = this;
    self.domainUrl = window.location.origin+'/api'+window.location.pathname;
    self.domain = ko.observableArray();
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
            var status = 'success gradeX';
            var icon = 'fa fa-check';
            var domain_url = 'http://'+data.domain[0].domain_name;
            var domain = data.domain[0].domain_name;
            var created = data.domain[0].created[0];
            var group = data.domain[0].domain_details[0].group;
            var owner = data.domain[0].domain_details[0].owner;
            var port = data.domain[0].domain_details[0].port;
            var document_root = data.domain[0].domain_details[0].document_root;

            self.domain.push({
                status: ko.observable(status),
                icon: ko.observable(icon),
                created: ko.observable(created),
                document_root: ko.observable(document_root),
                group: ko.observable(group),
                owner: ko.observable(owner),
                port: ko.observable(port),
                name: ko.observable(domain),
                domain_url: ko.observable(domain_url),
            });
    });
}
ko.applyBindings(new domainDetails(), $('#domain')[0]);
