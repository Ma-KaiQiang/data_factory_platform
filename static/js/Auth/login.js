import {request} from '../data_factory_request.js'
var that
class Login {
    constructor() {
        //登录元素
        that=this
        this.login_username = document.getElementById('login-user')
        this.login_password = document.getElementById('login-pwd')
        this.login_button = document.getElementById('login_btn')
    }
    login() {
        let data={'username':that.login_username.value,'password':that.login_password.value}
        request('post', 'http://127.0.0.1:8001/login/', JSON.stringify(data), function (res) {
            if (res.status===false){
               window.location.href = "http://127.0.0.1:8001/index/"
            }
        })
    }
    main() {
        this.login_button.onclick = this.login
    }
}

var auth =new Login;
auth.main();