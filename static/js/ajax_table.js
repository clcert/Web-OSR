function capitalizeFirstLetter(string) {
    string = string.toString();
    return string.charAt(0).toUpperCase() + string.slice(1);
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

function LeftHTTP(port, ip) {
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

function RightHTTP(port, ip) {
    return function(event) {
        event.defaultPrevented;
        var tmp_date = $('.table_date_'.concat(port)).html();
        var data = 'search/'.concat(port, '/', ip, '/', tmp_date, '/right');
        $.ajax({url : data, success: function(result){
            reRenderTable(result, port);
        }});
    }
}


function reRenderCertificate(result){
    console.log(result);
    if ($.isEmptyObject(result)){
        return;
    }
    $('.table_certificate').children().remove();
    if(result.date){
        $('.table_certificate').append('<tr> <td> <b>Date:</b></td> <td class="table_date_certificate">'
            .concat(result.date).concat('</td></tr>'));
    }
    if(result.error){
        $('.table_certificate').append('<tr> <td> <b>Error:</b></td> <td>'
            .concat(result.error, '</td></tr>'));
    }
    if(result.validate != null){
        $('.table_certificate').append('<tr><td><b>Validate Certificate:</b></td><td>'
            .concat(capitalizeFirstLetter(result.validate), '</td></tr>'));
    }
    if(result.validation_error){
        $('.table_certificate').append('<tr><td><b>Validation Error:</b></td><td>'
            .concat(result.validation_error, '</span></td></tr>'));
    }
    if(result.tls_protocol){
        $('.table_certificate').append('<tr> <td> <b>TLS Protocol:</b></td> <td>'
            .concat(result.tls_protocol, '</td></tr>'));
    }
    if(result.cipher_suite){
        $('.table_certificate').append('<tr> <td> <b>Cipher Suite:</b></td> <td>'
            .concat(result.cipher_suite, '</td></tr>'));
    }
    if(result.supported_protocols) {
        $('.table_certificate').append('<tr class="info"><td><b>Supported Protocols:</b></td><td></td></tr>');
        // TLS 1.2
        if (result.supported_protocols.TLS_12) {
            $('.table_certificate').append('<tr><td style="text-align: right"><b>TLS V1.2</b></td> ' +
                '<td><span class="label label-success" style="font-size: 14px">' + capitalizeFirstLetter(result.supported_protocols.TLS_12) +
                '</span></td></tr>');
        }
        else {
            $('.table_certificate').append('<tr><td style="text-align: right"><b>TLS V1.2</b></td> ' +
                '<td><span class="label label-danger" style="font-size: 14px">' + capitalizeFirstLetter(result.supported_protocols.TLS_12) +
                '</span></td></tr>');
        }
        // TLS 1.1
        if (result.supported_protocols.TLS_11) {
            $('.table_certificate').append('<tr><td style="text-align: right"><b>TLS V1.1</b></td> ' +
                '<td><span class="label label-success" style="font-size: 14px">' + capitalizeFirstLetter(result.supported_protocols.TLS_11) +
                '</span></td></tr>');
        }
        else {
            $('.table_certificate').append('<tr><td style="text-align: right"><b>TLS V1.1</b></td> ' +
                '<td><span class="label label-danger" style="font-size: 14px">' + capitalizeFirstLetter(result.supported_protocols.TLS_11) +
                '</span></td></tr>');
        }
        // TLS 1.0
        if (result.supported_protocols.TLS_10) {
            $('.table_certificate').append('<tr><td style="text-align: right"><b>TLS V1.0</b></td> ' +
                '<td><span class="label label-success" style="font-size: 14px">' + capitalizeFirstLetter(result.supported_protocols.TLS_10) +
                '</span></td></tr>');
        }
        else {
            $('.table_certificate').append('<tr><td style="text-align: right"><b>TLS V1.0</b></td> ' +
                '<td><span class="label label-danger" style="font-size: 14px">' + capitalizeFirstLetter(result.supported_protocols.TLS_10) +
                '</span></td></tr>');
        }
        // SSL 3.0
        if (result.supported_protocols.SSL_30) {
            $('.table_certificate').append('<tr><td style="text-align: right"><b>SSL V3.0</b></td> ' +
                '<td><span class="label label-success" style="font-size: 14px">' + capitalizeFirstLetter(result.supported_protocols.SSL_30) +
                '</span></td></tr>');
        }
        else {
            $('.table_certificate').append('<tr><td style="text-align: right"><b>SSL V3.0</b></td> ' +
                '<td><span class="label label-danger" style="font-size: 14px">' + capitalizeFirstLetter(result.supported_protocols.SSL_30) +
                '</span></td></tr>');
        }
    }
    if(result.chain) {
        $('.table_certificate').append('<tr class="info"><td><b>Chain:</b></td><td></td></tr>');
        for (i = 0; i < result.chain.length; i++) {
            if (result.chain[i].subject) {
                $('.table_certificate').append('<tr><td style="text-align: right"><b>Common Name Subject:</b></td><td>' +
                    result.chain[i].subject.common_name + '</td></tr>');
                $('.table_certificate').append('<tr><td style="text-align: right"><b>Organization Name Subject:</b></td><td>' +
                    result.chain[i].subject.organization_name + '</td></tr>');
            }
            if (result.chain[i].issuer) {
                $('.table_certificate').append('<tr><td style="text-align: right"><b>Common Name Issuer:</b></td><td>' +
                    result.chain[i].issuer.common_name + '</td></tr>');
                $('.table_certificate').append('<tr><td style="text-align: right"><b>Organization Name Issuer:</b></td><td>' +
                    result.chain[i].issuer.organization_name + '</td></tr>');
            }

            $('.table_certificate').append('<tr><td style="text-align: right"><b>Key Bits:</b></td><td>' + result.chain[i].key_bits + '</td></tr>');
            if (i < result.chain.length - 1) {
                $('.table_certificate').append('<tr class="firstLine"><td style="text-align: right"><b>Signature Algorithm:</b></td><td>' + result.chain[i].signature_algorithm + '</td></tr>');
            }
            else {
                $('.table_certificate').append('<tr><td style="text-align: right"><b>Signature Algorithm:</b></td><td>' + result.chain[i].signature_algorithm + '</td></tr>');
            }
        }
    }
    if(result.supported_cipher_suites) {
        $('.table_certificate').append('<tr class="info"><td><b>Supported Ciphers Suites:</b></td><td></td></tr>');

        //Nulls
        var null_cipher = 'Not Supported'
        if (result.supported_cipher_suites.null_ciphers) {
            null_cipher = capitalizeFirstLetter(result.supported_cipher_suites.null_ciphers);
        }
        $('.table_certificate').append('<tr><td style="text-align: right"><b>Null Ciphers</b></td> <td>' + null_cipher + '</td></tr>');

        // Anon Nulls
        var anonymous_null_ciphers = 'Not Supported'
        if (result.supported_cipher_suites.anonymous_null_ciphers) {
            anonymous_null_ciphers = capitalizeFirstLetter(result.supported_cipher_suites.anonymous_null_ciphers);
        }
        $('.table_certificate').append('<tr><td style="text-align: right"><b>Anonymous Null Ciphers</b></td> <td>' + anonymous_null_ciphers + '</td></tr>');

        // Anon DH
        var anonymous_dh_ciphers = 'Not Supported'
        if (result.supported_cipher_suites.anonymous_dh_ciphers) {
            anonymous_dh_ciphers = capitalizeFirstLetter(result.supported_cipher_suites.anonymous_dh_ciphers);
        }
        $('.table_certificate').append('<tr><td style="text-align: right"><b>Anonymous DH Ciphers</b></td> <td>' + anonymous_dh_ciphers + '</td></tr>');

        // Export 40
        var export_40_ciphers = 'Not Supported'
        if (result.supported_cipher_suites.export_40_ciphers) {
            export_40_ciphers = capitalizeFirstLetter(result.supported_cipher_suites.export_40_ciphers);
        }
        $('.table_certificate').append('<tr><td style="text-align: right"><b>Export 40 Ciphers</b></td> <td>' + export_40_ciphers + '</td></tr>');

        // Low
        var low_ciphers = 'Not Supported'
        if (result.supported_cipher_suites.low_ciphers) {
            low_ciphers = capitalizeFirstLetter(result.supported_cipher_suites.low_ciphers);
        }
        $('.table_certificate').append('<tr><td style="text-align: right"><b>Low Ciphers</b></td> <td>' + low_ciphers + '</td></tr>');

        // Medium
        var medium_ciphers = 'Not Supported'
        if (result.supported_cipher_suites.medium_ciphers) {
            medium_ciphers = capitalizeFirstLetter(result.supported_cipher_suites.medium_ciphers);
        }
        $('.table_certificate').append('<tr><td style="text-align: right"><b>Medium Ciphers</b></td> <td>' + medium_ciphers + '</td></tr>');

        // DES3
        var des3_ciphers = 'Not Supported'
        if (result.supported_cipher_suites.des3_ciphers) {
            des3_ciphers = capitalizeFirstLetter(result.supported_cipher_suites.des3_ciphers);
        }
        $('.table_certificate').append('<tr><td style="text-align: right"><b>DES3 Ciphers</b></td> <td>' + des3_ciphers + '</td></tr>');

        // High
        var high_ciphers = 'Not Supported'
        if (result.supported_cipher_suites.high_ciphers) {
            high_ciphers = capitalizeFirstLetter(result.supported_cipher_suites.high_ciphers);
        }
        $('.table_certificate').append('<tr><td style="text-align: right"><b>High Ciphers</b></td> <td>' + high_ciphers + '</td></tr>');

        // Freak
        var freak = 'Not Supported'
        if (result.supported_cipher_suites.freak) {
            freak = capitalizeFirstLetter(result.supported_cipher_suites.freak);
        }
        $('.table_certificate').append('<tr><td style="text-align: right"><b>FREAK</b></td> <td>' + freak + '</td></tr>');

        // logjam
        var logjam = 'Not Supported'
        if (result.supported_cipher_suites.logjam) {
            logjam = capitalizeFirstLetter(result.supported_cipher_suites.logjam);
        }
        $('.table_certificate').append('<tr><td style="text-align: right"><b>LogJam</b></td> <td>' + logjam + '</td></tr>');
    }
}

function LeftHTTPS(ip) {
    return function(event){
        event.preventDefault();
        var tempDate = $('.table_date_certificate').html();
        var data = "search/cert/"+ ip + "/" + tempDate + "/left";
        console.log(data);
        $.ajax({url : data, success: function(result) {
            reRenderCertificate(result);
        }});
    }
}

function RightHTTPS(ip) {
    return function(event) {
        event.preventDefault();
        var tempDate = $('.table_date_certificate').html();
        var data = "search/cert/" + ip + "/" + tempDate + "/right";
        console.log(data);
        $.ajax({url : data, success: function(result) {
            reRenderCertificate(result);
        }});
    }
}