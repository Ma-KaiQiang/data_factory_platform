import {request} from "../data_factory_request.js";

var that

class Register {
    constructor() {
        that = this
        //注册元素
        this.register_email = document.getElementById('email')
        this.register_username = document.getElementById('username')
        this.register_password = document.getElementById('password')
        this.register_button = document.getElementById('btn-register')
    }

    register() {
        let data = {'email':that.register_email.value,'username': that.register_username.value,'password':that.register_password.value}
        //var data = `email=${that.register_email.value}&username=${that.register_username.value}&password=${that.register_password.value}`
        request('post', 'http://127.0.0.1:8001/register/', JSON.stringify(data), function (res) {
            alert(res)
        })
    }

    main() {
        this.register_button.onclick = this.register
    }
}

var register = new Register
register.main()