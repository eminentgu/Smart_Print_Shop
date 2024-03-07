
let tableData = {
  "data": [
    {
      "id": 1,
      "filename": "伟大总理李克强.pdf",
      "condition": "未打印"
    },
    {
      "id": 2,
      "filename": "伟大领袖毛泽东.pdf",
      "condition": "未打印"
    },
    {
      "id": 3,
      "filename": "我的奋斗.word",
      "condition": "未打印"
    },
    {
      "id": 4,
      "filename": "你的奋斗.word",
      "condition": "已完成"
    },
    {
      "id": 5,
      "filename": "他的奋斗.word",
      "condition": "已完成"
    },
    {
      "id": 6,
      "filename": "我们的奋斗.word",
      "condition": "已完成"
    },
    {
      "id": 7,
      "filename": "他们的奋斗.word",
      "condition": "已完成"
    }
  ]
},

taskData = [
  {
    'taskID': '331231475382734',
    'description':{
      '创建时间': '2020-12-12 07:23:14',
      '取件码': '123456',
      '订单金额': '20.0 元',
      '打印文件': '伟大总理李克强，伟大领袖毛泽东，我的奋斗',
      '状态': '已完成',
    }
  },
  {
    'taskID': '426532521255290',
    'description':{
      '创建时间': '2020-12-10 12:12:12',
      '取件码': '123455',
      '订单金额': '25.0 元',
      '打印文件': '伟大李克强，伟大毛泽东，我的奋斗',
      '状态': '未完成',
    }, 
  },
  {
    'taskID': '426532521255290',
    'description':{
      '创建时间': '2020-12-10 12:12:12',
      '取件码': '123455',
      '订单金额': '25.0 元',
      '打印文件': '伟大李克强，伟大毛泽东，我的奋斗',
      '状态': '未完成',
    }, 
  }
],

detailData = [
  {
    'fileName': '伟大李克强',
    'description': {
      'paper': 'A4',
      'color': '彩色',
      'double': '单面',
      'note': '无'
    }
  },
  {
    'fileName': '伟大毛泽东',
    'description': {
      'paper': 'A3',
      'color': '彩色',
      'double': '双面',
      'note': '顺便打印一份毛主席语录'
    }
  }
]

module.exports = {
  'GET /api/user': {id: 1, username: 'kenny', sex: 6 },
  'GET /api/user/list': [
    {id: 1, username: 'kenny', sex: 6 },
    {id: 2, username: 'kenny', sex: 6 }
  ],
  'POST /api/login': (req, res) => {  // 后端写完后要改，请求后端username#id对应的密码
    const { password, username } = req.body;
    if (username === 'admin' && password === '111111' ) {
      return res.send({
        status: 'ok',
        code: 0,
        type: "admin",
        data: {id: 1, username: 'admin'} // id是用户唯一的标识
      });
    } else {
      if (username === 'user001' && password === '111111' ) {
        return res.send({
          status: 'ok',
          code: 0,
          type: "user",
          data: {id: 2, username: 'user001'}
        });
      }
      else{
        return res.send({status: 'error', code: 403 });
      }
    }
  },
  'POST /api/register': (req, res) => {  // 需要修改，administrator无法注册成为（administrator的增删只能通过后端数据库的记录增删进行），另外用户名可以重复，用#id唯一标识用户
    const { password, username, confirmPassword, userType} = req.body;
    if (username === 'admin' && password === '111111' &&confirmPassword == '111111' && userType == 'admin') {
      return res.send({
        status: 'ok',
        code: 0,
      });
    } else {
      return res.send({
        status: 'error',
        code: 403,
        message :'失败,失败的原因是XXX 这个后端处理咯！'
      });
    }
  },
  'POST /api/profits': (req, res) => {
    return res.send({
      status: 'ok',
      code: 0,
      profits:'+114514'
    });
  },

  'GET /api/printer': (req, res) => {
    return res.send({
      status: 'ok',
      code: 0,
      good : "6",
      bad: "2"
    });
  },

  'GET /api/printlist': (req, res) => {
    return res.send({
      status: 'ok',
      code: 0,
      data: tableData
    });
  },

  'DELETE /api/user/:id': (req, res) => {
    console.log('---->', req.body)
    console.log('---->', req.params.id)
    res.send({ status: 'ok', message: '删除成功！' });
  },

  'POST /api/upload': (req, res) => {  // 
    res.send({ status: 'ok', message: '上传成功！' , id: 1});
  },

  'POST /api/submitPrint': (req, res) => {  // 获取用户的一个打印任务中文件详细信息
    return res.send({ status: 'ok', message: 'get成功！', data: detailData});
  },

  'GET /api/historyPrint': (req, res) => {
    return res.send({
      status: 'ok',
      code: 0,
      message:'打印任务上传成功！',
      data: taskData
    });
  },
  'GET /api/printDetail': (req, res) => {  // 获取用户的一个打印任务中文件详细信息
    return res.send({ status: 'ok', message: 'get成功！', data: detailData});
  }
};

  
  