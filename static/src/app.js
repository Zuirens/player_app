/**
 * Created by tripper on 2016/11/17.
 */

var liveApp = (function () {
    var icmt = 0, tstp = 0, rv = 0, tv = 0, st = false, lcmt = [], au_id = '',
        globalStart = false,
        cmtbox = jQuery('.reviewTitle'),
        rvbox = jQuery('li#rv > span'),
        tvbox = jQuery('li#tv > span'),
        csrftoken;

    showCmt = function (s) {
        if (!globalStart) {
            return;
        }
        if (!s) {
            
            if (lcmt.length > 0) {
                cmtbox.fadeOut(1000, function () {
                    var cmt = lcmt.shift(), au = cmt['au'];
                    cmtbox.html("\<blockquote\>" + cmt['body'] + "\<cite\>\<a href=\"" + au['link'] + "\"\>" + au['name'] + "\<\/a\>\<\/cite\> \<\/blockquote\>").fadeIn(1000);
                });

                if (lcmt.length > 0) {
                    document.cookie = "icmt=" + lcmt[0].im;
                }
                else {
                    document.cookie = "icmt=" + cmt.im;
                }
            } else {
                cmtbox.fadeOut(1000);
            }
        } else {

        }

    };

    pCmt = function (e, d) {
        if (!globalStart) {
            console.log('skip msg');
            return;
        }
        if (typeof d == "object") {
            if (d['body']) {
                jQuery.ajax({
                    url: e,
                    method: 'post',
                    dataType: 'json',
                    data: d,
                    success: function (ret) {
                        lcmt.unshift(ret);
                    }
                });
            } else {
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
                    if (!globalStart) {
                        if (data['st']) {
                            document.location.href = "/";
                        }
                    }
                    globalStart = data['st'];
                    if (globalStart) {
                        icmt = data['icmt'];
                        tstp = data['tstp'];
                    }
                    rvbox.html(data['rv']);
                    tvbox.html(data['tv']);
                    if (data['lcmt'] && globalStart) {
                        for (var _i = 0; _i < data['lcmt'].length; _i++) {
                            if (data['lcmt'][_i]['au']['uid'] != au_id && !data['lcmt'][_i]['au']['isb'] && !data['lcmt'][_i]['isb']) {
                                lcmt.push(data['lcmt'][_i]);
                            }
                        }
                    }
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

    function statusChangeCallback(r) {
        if (r.status === 'connected') {
            if (!au_id || au_id == "AnonymousUser") {
                pAuth(r);
            }
        } else if (r.status === 'not_authorized') {
        } else {
            console.log('statusChangeCallback else');
        }
    }

    checkLoginState = function () {
        FB.getLoginStatus(function (r) {
            statusChangeCallback(r);
        });
    };

    fbAsyncInit = function () {
        console.log('fbAsyncInit');
        FB.init({
            appId: '1401988986704362',
            cookie: true,  // enable cookies to allow the server to access the session
            xfbml: true,  // parse social plugins on this page
            version: 'v2.8' // use graph api version 2.8
        });
        console.log('FB.inited');
        FB.getLoginStatus(function (response) {
            statusChangeCallback(response);
        });


    }();
    // Load the SDK asynchronously
    (function (d, s, id) {
        console.log('Load the SDK');
        var fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) return;
        js = d.createElement(s);
        js.id = id;
        js.src = "//connect.facebook.net/zh_TW/sdk.js";
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));

    // Here we run a very simple test of the Graph API after login is
    // successful.  See statusChangeCallback() for when this call is made.
    function pAuth(r) {
        var d = {};
        FB.api('/me', function (r1) {
            d = r1;
            FB.api('/me/picture', function (r2) {
                d['pic'] = r2.data.url;
                d['meta'] = r['authResponse']
                jQuery.ajax({
                    url: '/login/',
                    method: 'post',
                    dataType: 'json',
                    data: d,
                    success: function (ret) {

                        setTimeout(function () {
                            //your code to be executed after 1 second
                            document.location.href = '/';
                        }, 1000);
                    }

                })
            });
        });
    }

    init = function (id, st) {
        console.log('[1]app init');
        globalStart = st;
        au_id = id;
        icmt = gCk('icmt');

        console.log('[2]icmt should be got');

        // function getCookie(name) {
        //     var cookieValue = null;
        //     if (document.cookie && document.cookie !== '') {
        //         var cookies = document.cookie.split(';');
        //         for (var i = 0; i < cookies.length; i++) {
        //             var cookie = jQuery.trim(cookies[i]);
        //             // Does this cookie string begin with the name we want?
        //             if (cookie.substring(0, name.length + 1) === (name + '=')) {
        //                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        //                 break;
        //             }
        //         }
        //     }
        //     return cookieValue;
        // }

        csrftoken = gCk('csrftoken');
        console.log('[3]csrftoken should be set, csrftoken: ' + csrftoken);

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            console.log('[?]when to csrfSafeMethod?');
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        jQuery.ajaxSetup({
            beforeSend: function (xhr, settings) {
                console.log('[4]ajaxSetup set:');
                console.log(xhr);
                console.log(settings);
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
    checkLogin = function () {
        if (!au_id || au_id == 'AnonymousUser') {
            FB.login(function (r) {
                if (r['status'] == "connected") {
                    pAuth(r);
                }

            });

            return false;
        }
        return true;
    };

    return {
        init: init,
        showCmt: showCmt,
        pCmt: pCmt,
        gCmt: gCmt,
        parseJSON: parseJSON,
        gCk: gCk,
        checkLogin: checkLogin
    }

})();
