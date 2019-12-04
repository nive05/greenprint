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
    // Update an Order
    // ****************************************

    $("#update-btn").click(function () {

        var order_id = $("#order_id").val();
        var uuid = $("#order_uuid").val();
        var price = $("#order_price").val();
        var quantity = $("#order_quantity").val();
        var customer_id = $("#order_customer_id").val();
        var product_id = $("#order_product_id").val();
        var status = $("#order_status").val();

        var data = {
          "uuid": uuid,
          "price": price,
          "quantity": quantity,
          "customer_id": customer_id,
          "product_id": product_id,
          "status": status
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/orders/" + order_id,
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
    // Retrieve an Order
    // ****************************************

    $("#retrieve-btn").click(function () {

        var order_id = $("#order_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/orders/" + order_id,
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
    // Delete an Order
    // ****************************************

    $("#delete-btn").click(function () {

        var order_id = $("#order_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/orders/" + order_id,
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

        var customer_id = $("#order_customer_id").val();
        var product_id = $("#order_product_id").val();
        //var status = $("#order_status").val();

        var queryString = ""

        if (customer_id) {
            queryString += '/customers/' + customer_id
        }
        else if (product_id) {
            queryString += '/product/' + product_id
        }

        var ajax = $.ajax({
            type: "GET",
            url: "/orders" + queryString,
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
            var firstOrder = "";
            for(var i = 0; i < res.length; i++) {
                var order = res[i];
                var row = "<tr><td>"+order.id+"</td><td>"+order.price+"</td><td>"+order.quantity+"</td><td>"+order.customer_id+"</td><td>"+order.product_id+"</td><td>"+order.status+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstOrder = order;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstOrder != "") {
                update_form_data(firstOrder)
            }

            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });

})
