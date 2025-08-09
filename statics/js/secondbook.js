jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


window.onload=function(){
    var bookid = $("#bookid").html();
}


function logout(){
    var csrfToken = window.csrfToken;
    $.ajax({
        type: "POST",
        url: "/BookStacks/logout_func/",
        data: {
            'csrfmiddlewaretoken': csrfToken  // 这一条是用于ssl的加密，在data中包含csrf_token来进行验证，防止跨站攻击
        },
        dataType: 'json',
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        success: function(result) {
            location.reload();
        }
    });
}

function comment_submit(){
    var csrfToken = window.csrfToken;
    var com_body = editor.getHtml();
    var bookid = $('#bookid').html();
    if (com_body.match(/^\s*$/)) {
    }else{
        $.ajax({
            type: "POST",
            url: "/BookStacks/commentbookstacks/",
            data: {
                'com_body': com_body,
                'bookid': bookid,
                'csrfmiddlewaretoken': csrfToken  // 这一条是用于ssl的加密，在data中包含csrf_token来进行验证，防止跨站攻击
            },
            dataType: 'json',
            contentType: "application/x-www-form-urlencoded; charset=utf-8",
            success: function(result) {
                var UserName = result['UserName'];
                var com_time = result['com_time'];
                var com_id = result['com_id'];
                
                // 获取评论div
                var comlist=document.getElementById('comlist');
                var com=comlist.getElementsByTagName('div');//获取所有的评论

                // 构建评论
                //{{ comment.create_time|date:"Y-m-d H:i:s" }}

                htm = '<hr><p><img src="https://ladder3.oss-cn-beijing.aliyuncs.com/%E5%A4%B4%E5%83%8F.png" alt="" style="border-radius:50%; height: 40px; width: 40px;">'+
                '<strong style="color: black;font-size: 20px; text-decoration: underline; font-family:"Courier New, Courier, monospace;">'+UserName+'</strong>'+com_body+'</pre>'+
                '<div style="text-align: right;"><div class="del_com" style="cursor:pointer;color: #206cfa;" onclick="del_com('+com_id+')">删除</div></div>'
                '<div style="color: rgb(95, 95, 95); text-align: right;">发布于：'+com_time+'</div>'

                let divs = window.document.createElement("div");
                divs.innerHTML = htm;
                divs.id = 'com'+com_id;

                if(com.length>0){
                    comlist.insertBefore(divs,com[0]);//第一个参数是要插入的元素，第二个参数是在哪个元素之前插入
                }else{
                    comlist.appendChild(divs);
                }
            }
        });
    }
}

function show_login_modal(){
    $('#LoginModal').modal('show')
}

function hide_loginmodal(){
    $('#LoginModal').modal('hide')
}

function hide_signupmodal(){
    $('#SignupModal').modal('hide')
}

function hide_recordmodal(){
    $('#RecordModal').modal('hide')
}
function persnoal_info(){
    $('#PersnoalInfo').modal('show')
}
function hide_pimodal(){
    $('#PersnoalInfo').modal('hide')
}

function login(){
    var un = $('#username_login').val();
    var pw = $('#password_login').val();
    var csrfToken = window.csrfToken;
    $.ajax({
        type: "POST",
        url: "/BookStacks/login_bookstacks/",
        data: {
            'username': un,
            'password': pw,
            'csrfmiddlewaretoken': csrfToken  // 这一条是用于ssl的加密，在data中包含csrf_token来进行验证，防止跨站攻击
        },
        dataType: 'json',
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        success: function(result) {
            if (result['res'] == 'suc'){
                $('#login_info').html(result['suc_message']);
                document.getElementById('login_info').classList.remove("login_info_err");
                document.getElementById('login_info').classList.add("login_info_suc");
                location.reload();

            }
            else if (result['res'] == 'error'){
                $('#login_info').html(result['error_message']);
                document.getElementById('login_info').classList.remove("login_info_suc");
                document.getElementById('login_info').classList.add("login_info_err")
            }
        }
    });
}


function signup(){
    var un = $('#inputName').val();
    var email = $('#inputEmail').val();
    var pwd = $('#inputPassword').val();
    var pwd_conf = $('#inputPassword_conf').val();
    var csrfToken = window.csrfToken;

    // 判断格式是否合法，用户名不能有@ 和 .，邮箱不能没有 @ 和 .
    if (un.includes('@') || un.includes('.')){
        $('#rg_name_title').html("用户名不能包含'@' 或 '.'等特殊符号")
    }else{
        if (email.includes('@') && email.includes('.') ){
            if (pwd === pwd_conf){
                $.ajax({
                    type: "POST",
                    url: "/BookStacks/signup_bookstacks/",
                    data: {
                        'username': un,
                        'mailaddr': email,
                        'password': pwd,
                        'csrfmiddlewaretoken': csrfToken  // 这一条是用于ssl的加密，在data中包含csrf_token来进行验证，防止跨站攻击
                    },
                    dataType: 'json',
                    contentType: "application/x-www-form-urlencoded; charset=utf-8",
                    success: function(result) {
                        if (result['res'] == 'suc'){
                            //顺便登陆
                            $.ajax({
                                type: "POST",
                                url: "/BookStacks/login_bookstacks/",
                                data: {
                                    'username': un,
                                    'password': pwd,
                                    'csrfmiddlewaretoken':'{{ csrf_token }}'  // 这一条是用于ssl的加密，在data中包含csrf_token来进行验证，防止跨站攻击
                                },
                                dataType: 'json',
                                contentType: "application/x-www-form-urlencoded; charset=utf-8",
                                success: function(result) {
                                    if (result['res'] == 'suc'){
                                        $('#result_title').html('注册成功');
                                        var comm_top = document.getElementById('comm_top');
                                        comm_top.scrollIntoView({ vehavior:'smooth', block:'start' });
                                        location.reload();

                                    }
                                    // else if (result['res'] == 'error'){
                                    //     // 先试试刷新
                                    //     console.log(123)
                                    // }
                                }
                            });
                        }
                        else if (result['res'] == 'error_name_isexist'){
                            $('#rg_name_title').html('用户名已存在')
                        }
                        else if (result['res'] == 'error_mail_isexist'){
                            $('#rg_mail_title').html('邮箱已存在')
                        }
                    }
                });
            }else{
                $('#pwd_conf_title').html('两次输入的密码不一致')
            }
        }else{
            $('#rg_mail_title').html('邮箱格式有误')
        }
    }
}



function record_verify(){
    var recordmailaddr = $('#recordmailaddr').val();
    var recordcode = $('#recordcode').val();

    var ReinputPassword = $('#ReinputPassword').val();
    var ReinputPassword_conf = $('#ReinputPassword_conf').val();
    var csrfToken = window.csrfToken;
    
    if (ReinputPassword === ReinputPassword_conf){
        $.ajax({
        type: "POST",
        url: "/BookStacks/verifycode/",
        data: {
            'recordmailaddr': recordmailaddr,
            'recordcode': recordcode,
            'ReinputPassword': ReinputPassword,
            'csrfmiddlewaretoken': csrfToken  // 这一条是用于ssl的加密，在data中包含csrf_token来进行验证，防止跨站攻击
        },
        dataType: 'json',
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        success: function(result) {
            if (result['res'] == 'suc'){
                //顺便登陆
                $.ajax({
                    type: "POST",
                    url: "/BookStacks/login_bookstacks/",
                    data: {
                        'username': recordmailaddr,
                        'password': ReinputPassword,
                        'csrfmiddlewaretoken':'{{ csrf_token }}'  // 这一条是用于ssl的加密，在data中包含csrf_token来进行验证，防止跨站攻击
                    },
                    dataType: 'json',
                    contentType: "application/x-www-form-urlencoded; charset=utf-8",
                    success: function(result) {
                        if (result['res'] == 'suc'){
                            $('#result_title').html('修改成功');
                            var comm_top = document.getElementById('comm_top');
                            comm_top.scrollIntoView({ vehavior:'smooth', block:'start' });
                            location.reload();

                        }
                        // else if (result['res'] == 'error'){
                        //     // 先试试刷新
                        // }
                    }
                });

            }
            
            else if (result['res'] == 'error'){
                $('#send_status').html('验证码错误');
                document.getElementById('send_status').classList.remove("login_info_suc");
                document.getElementById('send_status').classList.add("login_info_err")
            }
        }
    });
    }
    
}

function change_signup(){
    $('#LoginModal').modal('hide');
    $('#SignupModal').modal('show');
    
}

function change_record(){
    $('#LoginModal').modal('hide');
    $('#RecordModal').modal('show');
    
}
function return_login(){
    $('#RecordModal').modal('hide');
    $('#LoginModal').modal('show');
}

function del_com(id){
    var bookcomID = id;
    var csrfToken = window.csrfToken;
    $.ajax({
        type: "POST",
        url: "/BookStacks/delcommentbook/",
        data: {
            'bookcomID': bookcomID,
            'csrfmiddlewaretoken': csrfToken  // 这一条是用于ssl的加密，在data中包含csrf_token来进行验证，防止跨站攻击
        },
        dataType: 'json',
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        success: function(result) {
            comid = 'com' + bookcomID
            document.getElementById(comid).remove();
        }
    });
}
function send_code(){
    var recordmailaddr = $('#recordmailaddr').val();
    var csrfToken = window.csrfToken;
    $.ajax({
        type: "POST",
        url: "/BookStacks/sendcode/",
        data: {
            'recordmailaddr': recordmailaddr,
            'csrfmiddlewaretoken': csrfToken  // 这一条是用于ssl的加密，在data中包含csrf_token来进行验证，防止跨站攻击
        },
        dataType: 'json',
        contentType: "application/x-www-form-urlencoded; charset=utf-8",
        success: function(result) {
            if (result == 200){
                $('#send_status').html('发送成功');
                document.getElementById('send_status').classList.add("login_info_suc");
                
            }
            
            else if (result == 500){
                $('#mailaddr_status').html('邮箱不存在');
                document.getElementById('mailaddr_status').classList.add("login_info_err")
            }
        }
    });
    
}

