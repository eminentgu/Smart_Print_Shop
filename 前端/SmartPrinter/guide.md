#### useful command
npx vue-cli-service serve
mocker ./mocker/index.js



#### api standard
* port ： 3721
* /api/login
  * params
    ```
    username
    password
    ```
  * return
    ``` 
        status: 'ok' / 'error',
        code: 0 / 403,
        type: 'admin'/'user',
        data: {id: int , username: str}
    ```
* /api/register
  * params
    ```
    username:str
    password:str
    confirmPassword:str
    userType:'user'/'admin'
    ```
  * return
    ```
    status : 'ok'
    code:0

    status :'error'
    code :443
    message : 失败的原因，这里传什么，前端就会显示什么。如账号昵称已被占用，密码不一致，密码为空之类。
    ```

* /api/profits
  * params
    ```
    没有
    ```
  * returns
    ```
    status:'ok'
    code: 0
    profits: str 有正负号的字符串，如"+114514"
    ```
  * 此外，需要生成一张profits图放在/src/assets/profits.png

* /api/printer
  * params
    ```
    没有
    ```
  * returns
    ```
    status:'ok'
    code: 0
    good: str "6" 好的打印机
    bad : str "2" 坏掉的打印机
    ```
  * 此外，需要生成一张printers图放在/src/assets/printers.jpg

* /api/printerlist
  * params
    ```
    没有
    ```
  * returns
    ```
    status:'ok'
    code: 0
    data:tableData,tableData是一个json，如
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
      }
* 