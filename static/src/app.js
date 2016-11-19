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
        if(!globalStart) { return; }
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
        if(!globalStart) { return; }
        if (typeof d == "object") {
            if (d['body']) {
                jQuery.ajax({
                    url: e,
                    method: 'post',
                    dataType: 'json',
                    data: d,
                    success: function (ret) {
                        lcmt.unshift({'au': {'exd': ''}, 'body': d['body']});
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
                    globalStart = data['st'];
                    if(globalStart) {
                        icmt = data['icmt'];
                        tstp = data['tstp'];
                    }
                    rvbox.html(data['rv'] + 10);
                    tvbox.html(data['tv']);
                    // console.log(globalStart);
                    // console.log(data['lcmt']);
                    // console.log(au_id);
                    if (data['lcmt'] && au_id && globalStart) {
                        // console.log(data['lcmt']);
                        // console.log(data['lcmt'][0]['au']['uid']);
                        for (var _i = 0; _i < data['lcmt'].length; _i++) {
                            if (data['lcmt'][_i]['au']['uid'] != au_id) {
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

    function statusChangeCallback(response) {
        // console.log('statusChangeCallback');
        // console.log(response);
        // The response object is returned with a status field that lets the
        // app know the current login status of the person.
        // Full docs on the response object can be found in the documentation
        // for FB.getLoginStatus().
        if (response.status === 'connected') {
            // Logged into your app and Facebook.
            testAPI();
        } else if (response.status === 'not_authorized') {
            // The person is logged into Facebook, but not your app.
            document.getElementById('status').innerHTML = 'Please log ' +
                'into this app.';
        } else {
            // The person is not logged into Facebook, so we're not sure if
            // they are logged into this app or not.
            document.getElementById('status').innerHTML = 'Please log ' +
                'into Facebook.';
        }
    }

    // This function is called when someone finishes with the Login
    // Button.  See the onlogin handler attached to it in the sample
    // code below.
    function checkLoginState() {
        FB.getLoginStatus(function (response) {
            statusChangeCallback(response);
        });
    }

    window.fbAsyncInit = function () {
        FB.init({
            appId: '1401988986704362',
            cookie: true,  // enable cookies to allow the server to access
                           // the session
            xfbml: true,  // parse social plugins on this page
            version: 'v2.8' // use graph api version 2.8
        });

        // Now that we've initialized the JavaScript SDK, we call
        // FB.getLoginStatus().  This function gets the state of the
        // person visiting this page and can return one of three states to
        // the callback you provide.  They can be:
        //
        // 1. Logged into your app ('connected')
        // 2. Logged into Facebook, but not your app ('not_authorized')
        // 3. Not logged into Facebook and can't tell if they are logged into
        //    your app or not.
        //
        // These three cases are handled in the callback function.

        FB.getLoginStatus(function (response) {
            statusChangeCallback(response);
        });

    };
      // Load the SDK asynchronously
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'facebook-jssdk'));

  // Here we run a very simple test of the Graph API after login is
  // successful.  See statusChangeCallback() for when this call is made.
  function testAPI() {
    // console.log('Welcome!  Fetching your information.... ');
    FB.api('/me', function(response) {
      // console.log('Successful login for: ' + response.name);
      // console.log(response);
      // document.getElementById('status').innerHTML =
      //   'Thanks for logging in, ' + response.name + '!';
    });
    FB.api('/me/picture', function (r) {
        // console.log(r.data.url);
    });
  }
    init = function (id) {
        au_id = id;
        // console.log(au_id);
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
