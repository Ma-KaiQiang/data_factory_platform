class Select {

    constructor(sel, opt) {
        this.sel = sel;
        this.opt = opt;

    }

    remove() {


    }

    request() {


    }


}

var that

class SelectHandle {

    constructor() {
        //外网select元素
        this.ol_instance_id = document.getElementById('ol_instance');
        this.ol_instance_opt_id = document.getElementById('instance');
        this.ol_db_id = document.getElementById('ol_db');
        this.ol_db_opt_id = document.getElementById('database');
        this.ol_tb_id = document.getElementById('ol_tb');
        this.ol_tb_opt_id = document.getElementById('table');
        this.ol_limit = document.getElementById('ol_limit');
        //内网select元素
        this.in_instance_id = document.getElementById('intranet_instance');
        this.in_instance_opt_id = document.getElementById('instance_sel');
        this.in_db_id = document.getElementById('intranet_db');
        this.in_db_opt_id = document.getElementById('db_sel');
        this.in_tb_id = document.getElementById('intranet_tb');
        this.in_tb_opt_id = document.getElementById('tb_sel');
        //外网select url
        this.ol_url = "http://127.0.0.1:8001/factory/online/data/";
        //内网select url
        this.in_url = "http://127.0.0.1:8001/factory/intranet/data/"
        that = this
    }

    clearSelectItem(args) {
        for (var i = 0; i < args.length; i++) {
            args[i].options.length = 0;
            args[i].selectpicker('refresh');
        }
    }

    initSelect(sel, opt, instance, database, url, remove = null) {
        this.initSelectOptions(sel, opt, instance, database, url)
        if (remove != null) {
            this.clearSelectItem(remove)
        }
    }

    initSelectOptions(sel, opt, instance, database, url) {
        $.ajax({
            url: url,
            async: false,
            type: "GET",
            data: "instance=" + instance + '&' + "database=" + database,
            success: function (result) {
                if (result.success) {
                    var configs = result.data;
                    that.clearSelectItem([sel]);
                    for (var i in configs) {
                        var optionValue = configs[i].name
                        opt.append(new Option(optionValue, optionValue));
                    }
                    // 刷新select
                    sel.selectpicker('refresh');
                } else {
                    console.log('获取[' + sel + ']信息失败，原因：' + result.errorMessage);
                }
            },
            error: function (result) {
                console.log('获取[' + sel + ']信息失败，原因：' + result.errorMessage);
            }
        });// ajax
    }

    initOnlineSelect() {
        this.ol_instance_id.onclick = function () {
            that.initSelect(that.ol_instance_id, that.ol_instance_opt_id, undefined, undefined, url = that.url, remove = [that.ol_db_id, that.ol_tb_id, that.ol_limit])
        }
        this.ol_db_id.onclick = function () {
            var instance = that.ol_instance_id.val()
            that.initSelect(that.ol_instance_id, that.ol_instance_opt_id, instance, undefined, url = that.url, remove = [that.ol_tb_id, that.ol_limit])
        }
        this.ol_tb_id.onclick = function () {
            var instance = that.ol_instance_id.val()
            var database = that.ol_db_id.val()
            that.initSelect(that.ol_instance_id, that.ol_instance_opt_id, instance, database, url = that.url, remove = [that.ol_limit])
        }
    }

    initIntranetSelect() {
        this.in_instance_id.onclick = function () {
            that.initSelect(that.in_instance_id, that.in_instance_opt_id, undefined, undefined, url = that.url, remove = [that.in_db_id, that.in_tb_id])
        }
        this.in_db_id.onclick = function () {
            var instance = that.in_instance_id.val()
            that.initSelect(that.in_instance_id, that.in_instance_opt_id, instance, undefined, url = that.url, remove = [that.in_tb_id])
        }
        this.in_tb_id.onclick = function () {
            var instance = that.in_instance_id.val()
            var database = that.in_db_id.val()
            that.initSelect(that.in_instance_id, that.in_instance_opt_id, instance, database, url = that.url)
        }
    }
}