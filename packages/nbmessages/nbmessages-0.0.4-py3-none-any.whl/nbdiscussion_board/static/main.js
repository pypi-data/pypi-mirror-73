define(['jquery', 'base/js/utils', 'require'], function ($, utils, require) {

    var tab = '<li><a href="#cluster_status" data-toggle="tab">Course Messages</a></li>'

    var load_ipython_extension = function () {
        $('#tabs').append(tab);
    };

    return {
        load_ipython_extension: load_ipython_extension,
    };
});
