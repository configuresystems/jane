function userList() {
    var self = this;
    self.userUrl = window.location.origin+'/api/users';
    self.users = ko.observableArray();
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
        for (var i = 0; i < data.users.length; i++) {
            var status = 'success gradeX';
            var icon = 'fa fa-check';
            var uri = '/users/'+data.users[i].username;

            self.users.push({
                status: ko.observable(status),
                icon: ko.observable(icon),
                uri: ko.observable(uri),
                name: ko.observable(data.users[i].username),
                domain: ko.observable(data.users[i].domain),
                shell: ko.observable(data.users[i].shell),
                sudoer: ko.observable(data.users[i].sudoer),
                count: ko.observable(data.count)
            });
        }
    });
}
ko.applyBindings(new userList(), $('#users')[0]);
