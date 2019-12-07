$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#accountid").val(res.id);
        $("#account_uuid").val(res.uuid);
        $("#account_owner").val(res.owner);
        $("#account_account_type").val(res.account_type);
        $("#account_institution_id").val(res.institution_id);
        $("#account_balance").val(res.balance);
        //if (res.status == false) {
        //    $("#account_status").val("In Progress");
        //} {
        $("#account_status").val(res.status);
        //}
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#account_uuid").val("");
        $("#account_owner").val("");
        $("#account_account_type").val("");
        $("#account_institution_id").val("");
        $("#account_balance").val("");
        $("#account_status").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    //generate an uuid
    function createUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    // ****************************************
    // Create an account
    // ****************************************

    $("#create-btn").click(function () {

        var uuid = $("#account_uuid").val();
        var owner = $("#account_owner").val();
        var account_type = $("#account_account_type").val();
        var institution_id = $("#account_institution_id").val();
        var balance = $("#account_balance").val();
        var status = $("#account_status").val();

        var data = {
            "uuid": uuid,
            "owner": owner,
            "account_type": account_type,
            "institution_id": institution_id,
            "balance": balance,
            "status": status
        };

        var ajax = $.ajax({
            type: "POST",
            url: "/accounts",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Update an account
    // ****************************************

    $("#update-btn").click(function () {

        var accountid = $("#account_id").val();
        var uuid = $("#account_uuid").val();
        var owner = $("#account_owner").val();
        var account_type = $("#account_account_type").val();
        var institution_id = $("#account_institution_id").val();
        var balance = $("#account_balance").val();
        var status = $("#account_status").val();

        var data = {
          "uuid": uuid,
          "owner": owner,
          "account_type": account_type,
          "institution_id": institution_id,
          "balance": balance,
          "status": status
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/accounts/" + accountid,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Retrieve an account
    // ****************************************

    $("#retrieve-btn").click(function () {

        var account_id = $("#account_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/accounts/" + account_id,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.message)
        });

    });

    // ****************************************
    // Delete an account
    // ****************************************

    $("#delete-btn").click(function () {

        var accountid = $("#accountid").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/accounts/" + accountid,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("Account has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#accountid").val("");
        clear_form_data()
        //update_order()
    });

    // ****************************************
    // Generate an uuid
    // ****************************************

    $("#generate-btn").click(function () {
        var uuid = createUUID();
        $("#accountuuid").val(uuid);
    });

    // ****************************************
    // Search for an account
    // ****************************************

    $("#search-btn").click(function () {

        var institution_id = $("#account_institution_id").val();
        var balance = $("#account_balance").val();
        //var status = $("#account_status").val();

        var queryString = ""

        if (institution_id) {
            queryString += '/institution_id/' + institution_id
        }
        else if (balance) {
            queryString += '/balance/' + balance
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/accounts" + queryString,
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:20%">Account ID</th>'
            header += '<th style="width:10%">Owner</th>'
            header += '<th style="width:15%">account Type</th>'
            header += '<th style="width:20%">Institution ID</th>'
            header += '<th style="width:20%">Balance</th>'
            header += '<th style="width:20%">Status</th></tr>'
            $("#search_results").append(header);
            var firstAccount = "";
            for(var i = 0; i < res.length; i++) {
                var account = res[i];
                var row = "<tr><td>"+account.id+"</td><td>"+account.owner+"</td><td>"+account.account_type+"</td><td>"+account.institution_id+"</td><td>"+account.balance+"</td><td>"+account.status+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstAccount = account;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstAccount != "") {
                update_form_data(firstAccount)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
