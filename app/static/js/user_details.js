function userDetails() {
    var self = this;
    self.userUrl = window.location.origin+'/api'+window.location.pathname;
    self.user = ko.observableArray();
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

    self.ajax(self.userUrl, 'GET').done(function(data) {
            var status = 'success gradeX';
            var icon = 'fa fa-check';
            var user = data.username[0].username;
            var shell = data.username[0].shell;
            var domain = data.username[0].domain;
            var sudoer = data.username[0].sudoer;
            var first = data.username[0].user_details[0].first;
            var last = data.username[0].user_details[0].last;
            var phone = data.username[0].user_details[0].phone;
            var email = data.username[0].user_details[0].email;
            var company = data.username[0].user_details[0].company;
            var created = data.username[0].created[0];

            self.user.push({
                status: ko.observable(status),
                icon: ko.observable(icon),
                created: ko.observable(created),
                user: ko.observable(user),
                shell: ko.observable(shell),
                domain: ko.observable(domain),
                sudoer: ko.observable(sudoer),
                first: ko.observable(first),
                last: ko.observable(last),
                phone: ko.observable(phone),
                email: ko.observable(email),
                company: ko.observable(company),
            });
    });
}
ko.applyBindings(new userDetails(), $('#user')[0]);
