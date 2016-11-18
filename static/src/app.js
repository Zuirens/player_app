/**
 * Created by tripper on 2016/11/17.
 */

var liveApp = (function () {
    var lcmt = 0, tstp = 0;

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
                data: {'lcmt': lcmt, 'tstp': tstp},
                success: function(data) {
                    lcmt = data['lcmt'];
                    tstp = data['tstp'];
                    
                    // console.log('cmt init');
                    // console.log(lcmt);
                }

            })
    };
    init = (function () {
            gCmt();
        })();


    return {
        pCmt: pCmt,
        gCmt: gCmt
    }

})();
