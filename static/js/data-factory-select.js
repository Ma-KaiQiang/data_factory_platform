var that
var ip = '127.0.0.1:8001'


class Authentication{
    constructor() {
    }

    login(){
        

    }
    register(){



    }


}
class PageRouting {
    constructor() {
        this.login = document.querySelector('#btn-login')
        this.register_now = document.querySelector('#register_now')
    }


    main() {
        this.register_now.onclick = window.navigate(ip + '/register/')
    }

}

//下拉框动态加载及数据展示
class SelectHandle {
    constructor() {
        that = this
        //外网select元素
        this.ol_instance_id = document.querySelector('#ol_instance');
        this.ol_instance_opt_id = document.getElementById('instance');
        this.ol_db_id = document.getElementById('ol_db');
        this.ol_db_opt_id = document.getElementById('database');
        this.ol_tb_id = document.getElementById('ol_tb');
        this.ol_tb_opt_id = document.getElementById('table');
        this.ol_limit = document.getElementById('ol_limit');
        this.query = document.getElementById('btn-sqlquery')
        //内网select元素
        this.in_select_btn = document.getElementById('btn-add');
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

    }

    clearSelectItem(args) {
        for (var i = 0; i < args.length; i++) {
            args[i].selectpicker('val', ['noneSelectedText']);
            args[i].selectpicker('refresh');
        }
    }

    initSelect(sel, opt, instance, database, url, remove = null) {
        this.initSelectOptions($(sel), opt, instance, database, url)
        if (remove != null) {
            this.clearSelectItem(remove)
        }
    }

    initSelectOptions($sel, opt, instance, database, url) {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var configs = JSON.parse(xhr.responseText).data;
                that.clearSelectItem([$sel]);
                for (var i in configs) {
                    var optionValue = configs[i]
                    opt.append(new Option(optionValue, optionValue));
                }
                // 刷新select
                $sel.selectpicker('refresh');
            }
        }
        xhr.open("GET", url + '?' + "instance=" + instance + '&' + "database=" + database, false)
        xhr.send(null)
    }

    initOnlineSelect() {
        window.onload = function () {
            that.initSelect(that.ol_instance_id, that.ol_instance_opt_id, undefined, undefined, that.ol_url, [$(that.ol_db_id), $(that.ol_tb_id), $(that.ol_limit)])
        }
        this.ol_instance_id.onchange = function () {
            var instance = $(that.ol_instance_id).val()
            that.initSelect(that.ol_db_id, that.ol_db_opt_id, instance, undefined, that.ol_url, [$(that.ol_tb_id), $(that.ol_limit)])
        }
        this.ol_db_id.onchange = function () {
            var instance = $(that.ol_instance_id).val()
            var database = $(that.ol_db_id).val()
            that.initSelect(that.ol_tb_id, that.ol_tb_opt_id, instance, database, that.ol_url, [$(that.ol_limit)])
        }
    }

    initIntranetSelect() {
        var instance = null
        var database = null
        var table = null
        this.in_select_btn.onclick = function () {
            that.initSelect($(that.in_instance_id), $(that.in_instance_opt_id), undefined, undefined, that.in_url, [$(that.in_instance_id), $(that.in_db_id), $(that.in_tb_id)])
        }
        this.in_instance_id.onchange = function () {
            instance = $(that.in_instance_id).val()
            that.initSelect($(that.in_db_id), $(that.in_db_opt_id), instance, undefined, that.in_url, [$(that.in_tb_id), $(that.in_tb_id)])
        }
        this.in_db_id.onchange = function () {
            database = $(that.in_db_id).val()
            that.initSelect($(that.in_tb_id), $(that.in_tb_opt_id), instance, database, that.in_url, [$(that.in_tb_id)])
            table = $(that.in_tb_id).val()
        }
        return [instance, database, table]
    }

    select_validate() {
        let result = true;
        let instance_name = $(this.ol_instance_id).val();
        let db_name = $(this.ol_db_id).val();
        let sqlContent = editor.getValue();
        let select_sqlContent = editor.session.getTextRange(editor.getSelectionRange());
        if (select_sqlContent) {
            sqlContent = select_sqlContent
        }
        if (!instance_name) {
            alert("请选择实例！");
            result = false;
        } else if (!db_name) {
            alert("请选择数据库！");
            result = false;
        } else if (!sqlContent) {
            alert("SQL内容不能为空！");
            result = false;
        }
        return result;
    }

    //先做表单验证，验证成功再成功提交查询请求
    validate() {
        this.query.onclick = function () {
            if (that.select_validate()) {
                that.sqlquery();
            }
        }
    }

    display_data(data) {
        var result = data.data;
        if (result['column_list']) {
            //异步获取要动态生成的列
            var columns = [{
                field: '全选',
                checkbox: true,
            }];
            $.each(result['column_list'], function (i, column) {
                columns.push({
                    field: i,
                    title: column,
                    align: 'left',
                });
            })
            //初始化查询结果
            $("#" + ('query_result')).bootstrapTable('destroy').bootstrapTable({
                data: result['rows'],
                columns: columns,
                uniqueId: "id",                    //每一行的唯一标识，一般为主键列
                undefinedText: 'null',
                showColumns: true,   //是否显示所有的列
                showToggle: true,
                clickToSelect: true,
                striped: true,
                toolbar: '#toolbar',
                total: result.total,
                singleSelect: true,
                pagination: true,
                pageSize: 30,//每页的记录行数（*）
                pageList: [10, 20, 30, 50], //可供选择的每页的行数（*）
                paginationPreText: "上一页",
                paginationNextText: "下一页",
                search: true,                      //是否显示表格搜索
                strictSearch: false,                //是否全匹配搜索
                onLoadSuccess: function (data) { //加载成功时执行
                    var tool = document.getElementById("#toolbar")
                    tool.style.display = 'block'
                    console.log(data);
                },
                onLoadError: function (res) { //加载失败时执行
                    console.log(res);
                },
                //格式化详情
                detailFormatter: function (index, row) {
                    var html = [];
                    $.each(row, function (key, value) {
                        if (key === 0) {//mongodb这里要修改
                            html.push('<pre>' + highLight(value) + '</pre>');
                        }
                    });
                    return html.join('');
                },
                locale: 'zh-CN'
            });

        }
    }

    //向后端提交查询数据
    sqlquery() {
        var select_sqlContent = editor.session.getTextRange(editor.getSelectionRange());
        if (select_sqlContent) {
            sqlContent = select_sqlContent
        } else {
            var sqlContent = editor.getValue();
        }
        //提交请求
        $.ajax({
            type: "post",
            url: "http://127.0.0.1:8001/factory/query/",
            dataType: "json",
            data: JSON.stringify({
                instance_name: $(that.ol_instance_id).val(),
                db_name: $(that.ol_db_id).val(),
                tb_name: $(that.ol_tb_id).val(),
                sql_content: sqlContent,
                limit_num: $(that.ol_limit).val()
            }),
            success: function (data) {
                console.log(data)
                that.display_data(data)
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(errorThrown);
            }
        });
    }

    main() {
        this.initOnlineSelect()
        this.initIntranetSelect()
        this.validate()

    }
}

//数据同步
class DataSync extends SelectHandle {
    constructor() {
        super()
        this.sync_btn = document.querySelector('#sync-btn')
        this.query_table = document.querySelector('#query_result')

    }
    get_select($ele) {
        return ele.bootstrapTable('getSelections')
    }
    get_select_val(args) {
        var vals = []
        for (var i in args) {
            vals.push(args[i])
        }
        return vals
    }

    public() {
        var vals = this.get_select_val([$(this.in_instance_id), $(this.in_db_id), $(this.in_tb_id)])
        var rows = this.get_select($(this.query_table))
        console.log(vals, rows)
        this.sync_request('', rows, vals)
    }


    sync_request(url, data, sync_condition) {
        $.ajax({
            type: 'port',
            url: url,
            dataType: 'json',
            data: JSON.stringify({
                data: data,
                condition: sync_condition
            }),
            success: function (data) {
                console.log(data)
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert(errorThrown);
            }
        })
    }
}


var sel = new SelectHandle()
var page=new PageRouting()
page.main()
sel.main()
