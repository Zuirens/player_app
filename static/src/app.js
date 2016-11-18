/**
 * Created by tripper on 2016/11/17.
 */

var liveApp = (function () {
    var icmt = 0, tstp = 0, rv = 0, tv = 0, st = false, lcmt = [],
        cmtbox = jQuery('.reviewTitle'),
        rvbox = jQuery('li#rv > span'),
        tvbox = jQuery('li#tv > span');

    showCmt = function () {
        if(lcmt.length > 0) {
            var cmt = lcmt.shift(), au = parseJSON(cmt['au']['exd']);
            // console.log(au['authResponse']['userID']);
            cmtbox.html(au['authResponse']['userID'] + ':' + cmt['body']);
            if(lcmt.length > 0) { document.cookie = "icmt=" + lcmt[0].im; }
            else { document.cookie = "icmt=" + cmt.im; }
        } else { cmtbox.html(''); }

    };

    pCmt = function (endpoint, data) {
            // console.log(a * a + a);
            // console.log(endpoint);
            // console.log(data);
    };
    gCmt = function () {
        if(lcmt.length < 3) {
            jQuery.ajax({
                url: '/api/',
                method: 'get',
                dataType: 'json',
                data: {'icmt': icmt, 'tstp': tstp},
                success: function(data) {
                    console.log(data);
                    icmt = data['icmt'];
                    tstp = data['tstp'];
                    rvbox.html(data['rv']+10);
                    tvbox.html(data['tv']);
                    Array.prototype.push.apply(lcmt, data['lcmt']);
                    console.log(lcmt.length);
                }

            })
        }

    };


    
    gCk = function(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length,c.length);
        }
    }
    return "";
    };
    init = (function () {
        icmt = gCk('icmt');
        gCmt();
    })();
    (function () {
        setInterval(showCmt, 5000);
        setInterval(gCmt, 5000);
    })();

    parseJSON = function (string) {
        return jQuery.parseJSON(jQuery.parseHTML(string)[0].data);
    };

    return {
        showCmt: showCmt,
        pCmt: pCmt,
        gCmt: gCmt,
        parseJSON: parseJSON,
        gCk: gCk
    }

})();
