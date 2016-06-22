function onSuccess(result){
    reRenderTable(result);
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function reRenderTable(result, tablePort){
    if ($.isEmptyObject(result)){
        return;
    }
    $('.tabla_'.concat(tablePort)).children().remove();
    if(result.date){
        $('.tabla_'.concat(tablePort)).append('<tr> <td> <b>Date:</b></td> <td class="table_date_'
            .concat(tablePort).concat('">').concat(result.date).concat('</td></tr>'));
    }
    if(result.error){
        $('.tabla_'.concat(tablePort)).append('<tr> <td> <b>Error:</b></td> <td> <span class="label label-danger table_error">'
            .concat(result.error).concat('</span></td></tr>'));
    }
    if(result.status){
        $('.tabla_'.concat(tablePort)).append('<tr> <td><b>Response:</b></td> <td class="table_response">'
            .concat(result.status.toString()));
    }
    if(result.parse_header){
        var header = "";
        for( var key in result.parse_header ) {
            header = header.concat(key).concat(': ').concat(result.parse_header[key]).concat('<br>');
        }
        $('.tabla_'.concat(tablePort)).append('<tr><td><b>Header:</b></td><td class="table_header">'.concat(header).concat('</td></tr>'));
    }
    if(result.raw_index){
        $('.tabla_'.concat(tablePort)).append('<tr> <td> <b>Index:</b></td> <td class="table_index">'
            .concat(escapeHtml(result.raw_index).substring(0,1000)).concat('</td></tr>'));
    }

    if(result.metadata){
        if(result.metadata.service.manufacturer){
            $('.tabla_'.concat(tablePort)).append('<tr> <td> <b>Manufacturer:</b></td> <td class="table_service_manufacturer">'
                .concat(result.metadata.service.manufacturer).concat('</td></tr>'));
        }
        if(result.metadata.service.product){
            $('.tabla_'.concat(tablePort)).append('<tr> <td> <b>Product:</b></td> <td class="table_service_product">'
                .concat(result.metadata.service.product).concat('</td></tr>'));
        }
        if(result.metadata.service.version){
            $('.tabla_'.concat(tablePort)).append('<tr> <td> <b>Version:</b></td> <td class="table_service_version">'
                .concat(result.metadata.service.version).concat('</td></tr>'));
        }
    }
}

function Left(port, ip) {
    return function(event) {
        event.defaultPrevented;
        var tmp_date = $('.table_date_'.concat(port)).html();
        var data = 'search/'.concat(port, '/', ip, '/', tmp_date, '/left');
        $.ajax({
            url: data, success: function (result) {
                reRenderTable(result, port);
            }
        });
    }
}

function Right(port, ip) {
    return function(event) {
        event.defaultPrevented;
        var tmp_date = $('.table_date_'.concat(port)).html();
        var data = 'search/'.concat(port, '/', ip, '/', tmp_date, '/right');
        $.ajax({url : data, success: function(result){
            reRenderTable(result, port);
        }});
    }
}