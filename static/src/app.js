/**
 * Created by tripper on 2016/11/17.
 */

var liveApp = (function () {
    var icmt = 0, tstp = 0, rv = 0, tv = 0, st = false, lcmt = [],
        cmtbox = jQuery('.reviewTitle');

    showCmt = function () {
        if(lcmt.length > 0) {
            var cmt = lcmt.shift(), au = parseJSON(cmt['au']['exd']);
            // console.log(au['authResponse']['userID']);
            cmtbox.html(au['authResponse']['userID'] + ':' + cmt['body']);
        }
    };

    pCmt = function (endpoint, data) {
            // console.log(a * a + a);
            // console.log(endpoint);
            // console.log(data);
    };
    gCmt = function () {
        jQuery.ajax({
                url: '/api/',
                method: 'get',
                dataType: 'json',
                data: {'icmt': icmt, 'tstp': tstp},
                success: function(data) {
                    icmt = data['icmt'];
                    tstp = data['tstp'];
                    rv = data['rv'];
                    tv = data['tv'];
                    Array.prototype.push.apply(lcmt, data['lcmt']);
                    console.log(lcmt.length);
                }

            })
    };
    init = (function () {
            gCmt();
        })();
    

    (function () {
        setInterval(showCmt, 2000);
        setInterval(gCmt, 10000);
    })();

    parseJSON = function (string) {
        return jQuery.parseJSON(jQuery.parseHTML(string)[0].data);
    };
    return {
        showCmt: showCmt,
        pCmt: pCmt,
        gCmt: gCmt,
        parseJSON: parseJSON
    }

})();
