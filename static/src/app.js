/**
 * Created by tripper on 2016/11/17.
 */

var liveApp = (function () {
    var icmt = 0, tstp = 0, rv = 0, tv = 0, st = false, lcmt = [], au_id = '',
        cmtbox = jQuery('.reviewTitle'),
        rvbox = jQuery('li#rv > span'),
        tvbox = jQuery('li#tv > span'),
        csrftoken;

    showCmt = function (s) {
        if (!s) {
            // console.log(au_id);
            if (lcmt.length > 0) {
                var cmt = lcmt.shift(), au = parseJSON(cmt['au']['exd']);
                // console.log(cmt['au']['uid']);
                cmtbox.html(au + ':' + cmt['body']);
                if (lcmt.length > 0) {
                    document.cookie = "icmt=" + lcmt[0].im;
                }
                else {
                    document.cookie = "icmt=" + cmt.im;
                }
            } else {
                cmtbox.html('');
            }
        } else {

        }


    };

    pCmt = function (e, d) {
        if (typeof d == "object") {
            if (d['body']) {
                jQuery.ajax({
                    url: e,
                    method: 'post',
                    dataType: 'json',
                    data: d,
                    success: function (ret) {
                        lcmt.unshift({'au':{'exd': ''}, 'body': d['body']});
                        // console.log(ret)
                    }
                });
                // console.log(e);
                // console.log(d);
            } else {
                console.log('empty');
            }
        }

    };
    gCmt = function () {
        if (lcmt.length < 3) {
            jQuery.ajax({
                url: '/api/',
                method: 'get',
                dataType: 'json',
                data: {'icmt': icmt, 'tstp': tstp},
                success: function (data) {
                    // console.log(data);
                    icmt = data['icmt'];
                    tstp = data['tstp'];
                    rvbox.html(data['rv'] + 10);
                    tvbox.html(data['tv']);

                    if(data['lcmt'] && au_id) {
                        // console.log(data['lcmt']);
                        // console.log(data['lcmt'][0]['au']['uid']);
                        for (var _i = 0; _i < data['lcmt'].length; _i++) {
                        if(data['lcmt'][_i]['au']['uid'] != au_id) {
                            lcmt.push(data['lcmt'][_i]);
                        }
                    }
                    }

                    // console.log(lcmt);
                }

            });
        }

    };


    gCk = function (cname) {
        var name = cname + "=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    };
    init = function (id) {
        au_id = id;
        icmt = gCk('icmt');
        csrftoken = gCk('csrftoken');
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        jQuery.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });
        gCmt();
    };
    (function () {
        setInterval(showCmt, 5000);
        setInterval(gCmt, 5000);
    })();

    parseJSON = function (string) {
        return string ? jQuery.parseJSON(jQuery.parseHTML(string)[0].data) : "訪客";
    };


    return {
        init: init,
        showCmt: showCmt,
        pCmt: pCmt,
        gCmt: gCmt,
        parseJSON: parseJSON,
        gCk: gCk
    }

})();
