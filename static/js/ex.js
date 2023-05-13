 window.onload = function () {
            // 动态加载省份选项数据
            initSelectOptions("instance", "query_instance");
        };// onReady
        function removeAll(ele) {
            //根据id查找对象，
            var selectObj = document.getElementById(ele);
            //将select的options置为0
            selectObj.options.length = 0;
        }

        /**
         * 动态生成select选项
         * @param selectId
         * @param parentId
         * @param instance
         * @param database
         * @returns
         */

        function initSelectOptions(selectId, parentId, instance = null, database = null) {
            var selectObj = $("#" + selectId);
            var optgroupObj = $("#" + parentId);
            $.ajax({
                url: "http://127.0.0.1:8001/factory/online/data/",
                async: false,
                type: "GET",
                data: "instance=" + instance + '&' + "database=" + database,
                success: function (result) {
                    if (result.success) {
                        var configs = result.data;
                        selectObj.find().remove();
                        for (var i in configs) {
                            var optionValue = configs[i];
                            selectObj.append(new Option(optionValue, optionValue));
                        }
                        // 刷新select
                        optgroupObj.selectpicker('render');
                        optgroupObj.selectpicker('refresh');
                    } else {
                        console.log('获取[' + parentId + ']信息失败，原因：' + result.errorMessage);
                    }
                },
                error: function (result) {
                    console.log('获取[' + parentId + ']信息失败，原因：' + result.errorMessage);
                }
            });// ajax
        }

        function initDatabase() {
            // 当实例变更清除数据库，表并刷新
            removeAll('query_db');
            removeAll('query_tb');
            $("#query_tb").selectpicker('refresh');
            $("#limit_num").selectpicker('refresh');
            var instanceSel = $("#query_instance").val();
            initSelectOptions('database', 'query_db', instanceSel);


        }

        function initTable() {
            // 当数据库变更时，清空表并刷新
            var instanceSel = $("#query_instance").val();
            var dbSel = $("#query_db").val();
            removeAll('query_tb');
            $("#query_tb").selectpicker('refresh');
            initSelectOptions('table', 'query_tb', instanceSel, dbSel);
        }




        function sqlquery_validate() {
            var result = true;
            var instance_name = $("#query_instance").val();
            var db_name = $("#query_db").val();
            var sqlContent = editor.getValue();

            var select_sqlContent = editor.session.getTextRange(editor.getSelectionRange());
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
        var validate = function () {
            if (sqlquery_validate()) {
                sqlquery();
            }
        };

function tab() {
    var lis = document.querySelectorAll('#tab_>ul')
    for (var i = 0; i < lis.length; i++) {
        lis[i].index = i;
        lis[i].onclick = function (i) {
            lis[i].className = 'active'
        }
    }
}


function remove_tab_class() {
    var lis = document.querySelectorAll('#tab_>ul>li')
    for (var i = 0; i < lis.length; i++) {
        lis[i].removeAttribute('class')
    }

}

function tab() {
    var lis = document.querySelectorAll('#tab_>ul>li')

    for (var i = 0; i < lis.length; i++) {
        lis[i].index = i;
        lis[i].onclick = function () {
            remove_tab_class()
            this.className = 'active';

        }
    }
}


tab()

//初始化内网实例数据
function initInstance() {
    initIntranetSelectOptions("intranet_instance", "instance_sel");
}

//清除optgroup
function removeAll(ele) {
    //根据id查找对象，
    var selectObj = document.getElementById(ele);
    //将select的options置为0
    selectObj.options.length = 0;
}

/**
 * 动态生成select选项
 * @param selectId
 * @param optId
 * @param instance
 * @param database
 * @returns
 */
function initIntranetSelectOptions(selectId, optId, instance, database) {
    var selectObj = $("#" + selectId);
    var optgroupObj = $("#" + optId);
    $.ajax({
        url: "http://127.0.0.1:8001/factory/intranet/data/",
        async: false,
        type: "GET",
        data: "instance=" + instance + '&' + "database=" + database,
        success: function (result) {
            if (result.success) {
                var configs = result.data;
                removeAll(selectId)
                for (var i in configs) {
                    var optionValue = configs[i].name
                    optgroupObj.append(new Option(optionValue, optionValue));
                }
                // 刷新select
                selectObj.selectpicker('render');
                selectObj.selectpicker('refresh');
            } else {
                console.log('获取[' + selectId + ']信息失败，原因：' + result.errorMessage);
            }
        },
        error: function (result) {
            console.log('获取[' + selectId + ']信息失败，原因：' + result.errorMessage);
        }
    });// ajax
}

//初始化数据库列表
function initIntranetDatabase() {
    // 当实例变更清除数据库，表并刷新
    removeAll('intranet_db');
    removeAll('intranet_tb');
    $("#intranet_db").selectpicker('refresh');
    $("#intranet_tb").selectpicker('refresh');
    var instanceSel = $("#intranet_instance").val();
    initSelectOptions('db_sel', 'intranet_db', instanceSel);
}

//初始化内网数据表数据
function initIntranetTable() {
    // 当数据库变更时，清空表并刷新
    var instanceSel = $("#intranet_instance").val();
    var dbSel = $("#intranet_db").val();
    removeAll('intranet_db');
    $("#intranet_db").selectpicker('refresh');
    initSelectOptions('tb_sel', 'intranet_tb', instanceSel, dbSel);
}

//校验内网数据库配置
function sync_data_validate() {
    var result = true;
    var instance_name = $("#intranet_instance").val();
    var db_name = $("#intranet_db").val();
    if (!instance_name) {
        alert("请选择实例！");
        return result = false;
    } else if (!db_name) {
        alert("请选择数据库！");
        return result = false;
    }
    return result;
}

//同步数据至内网
function data_sync_to_intranet() {
    if (sync_data_validate()) {

    }
}