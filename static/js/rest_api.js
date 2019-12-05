$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#accountid").val(res.id);
        $("#owner").val(res.owner);
        $("#account_id").val(res.account_id);
        $("#account_type").val(res.account_type);
        $("#institution_id").val(res.institution_id);
        $("#balance").val(res.balance);
        //if (res.status == false) {
        //    $("#order_status").val("In Progress");
        //} {
       // $("#isHidden").val(res.isHidden);
        //}
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#accountid").val("");
        $("#owner").val("");
        $("#account_id").val("");
        $("#account_type").val("");
        $("#institution_id").val("");
        $("#balance").val("");
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
    // Create an Account
    // ****************************************

    $("#create-btn").click(function () {

        var id = $("#accountid").val();
        var owner = $("#owner").val();
        var account_id = $("#account_id").val();
        var account_type = $("#account_type").val();
        var institution_id = $("#institution_id").val();
        var balance = $("#balance").val();

        var data = {
            "accountid": accountid,
            "owner": owner,
            "account_id": account_id,
            "account_type": account_type,
            "institution_id": institution_id,
            "balance": balance
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

        var accountid = $("#accountid").val();
        var owner = $("#owner").val();
        var account_id = $("#account_id").val();
        var account_type = $("#account_type").val();
        var institution_id = $("#institution_id").val();
        var balance = $("#balance").val();
       // var status = $("#order_status").val();

        var data = {
          "owner": owner,
          "account_id": account_id,
          "account_type": account_type,
          "institution_id": institution_id,
          "balance": balance,
         // "status": status
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

        var accountid = $("#accountid").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/accounts/" + accountid,
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
            flash_message("Order has been Deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#order_id").val("");
        clear_form_data()
        //update_order()
    });

    // ****************************************
    // Generate an uuid
    // ****************************************

    $("#generate-btn").click(function () {
        var uuid = createUUID();
        $("#order_uuid").val(uuid);
    });

    // ****************************************
    // Search for an Order
    // ****************************************

    $("#search-btn").click(function () {

        var owner = $("#owner").val();
        var account_id = $("#account_id").val();
        var account_type = $("#account_type").val();
        var institution_id = $("#institution_id").val();
        var balance = $("#balance").val();
        //var status = $("#order_status").val();

        var queryString = ""

        if (owner) {
            queryString += '/owners/' + owner
        }
        else if (account_id) {
            queryString += '/account_id/' + account_id
        }
        else if (account_type) {
            queryString += '/account_type/' + account_type
        }
        else if (institution_id) {
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
            header += '<th style="width:20%">Order ID</th>'
            header += '<th style="width:10%">Price</th>'
            header += '<th style="width:15%">Quantity</th>'
            header += '<th style="width:20%">Customer ID</th>'
            header += '<th style="width:20%">Product ID</th>'
            header += '<th style="width:20%">Status</th></tr>'
            $("#search_results").append(header);
            var firstAccount = "";
            for(var i = 0; i < res.length; i++) {
                var order = res[i];
                var row = "<tr><td>"+account.id+"</td><td>"+account.owner+"</td><td>"+account.account_id+"</td><td>"+account.account_type+"</td><td>"+account.institution_id+"</td><td>"+account.balance+"</td></tr>";
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
