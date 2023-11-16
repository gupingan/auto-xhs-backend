**GET /api/test**

- Description: 测试接口，等待5秒后返回成功信息。
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "获取成功",
        "data": {
          "time": "当前时间戳"
        }
      }
      ```

**POST /api/user/login**

- Description: 用户登录接口。
- Request:
  - Headers:
    - Content-Type: application/json
  - Body:
    ```
    {
      "token": "用户令牌"
    }
    ```
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "登录成功",
        "token": "用户令牌",
        "data": {}
      }
      ```

**POST /api/admin/login**

- Description: 管理员登录接口。
- Request:
  - Headers:
    - Content-Type: application/json
  - Body:
    ```
    {
      "token": "管理员令牌"
    }
    ```
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "登录成功",
        "token": "管理员令牌",
        "data": {}
      }
      ```

**POST /api/user/register**

- Description: 用户注册接口。
- Request:
  - Headers:
    - Content-Type: application/json
  - Body:
    ```
    {
      "uname": "用户名",
      "upwd": "密码",
      "max_limit": 0
    }
    ```
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "注册成功",
        "data": {}
      }
      ```
  - 401 Unauthorized
    - Body: 
      ```
      {
        "success": false,
        "msg": "注册失败",
        "data": {}
      }
      ```

**POST /api/admin/init**

- Description: 初始化管理员账号接口。
- Request:
  - Headers:
    - Content-Type: application/json
  - Body: Empty
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "初始化管理员账号成功",
        "data": {}
      }
      ```
  - 401 Unauthorized
    - Body: 
      ```
      {
        "success": false,
        "msg": "初始化管理员账号失败",
        "data": {}
      }
      ```

**POST /api/user/password**

- Description: 修改用户密码接口。
- Request:
  - Headers:
    - Content-Type: application/json
  - Body:
    ```
    {
      "uname": "用户名",
      "upwd": "新密码"
    }
    ```
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "用户密码修改成功",
        "data": {}
      }
      ```
  - 401 Unauthorized
    - Body: 
      ```
      {
        "success": false,
        "msg": "用户密码修改失败",
        "data": {}
      }
      ```

**POST /api/admin/password**

- Description: 修改管理员密码接口。
- Request:
  - Headers:
    - Content-Type: application/json
  - Body:
    ```
    {
      "uname": "用户名",
      "upwd": "新密码"
    }
    ```
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "管理员密码修改成功",
        "data": {}
      }
      ```
  - 401 Unauthorized
    - Body: 
      ```
      {
        "success": false,
        "msg": "管理员密码修改失败",
        "data": {}
      }
      ```

**GET /api/admin/json**

- Description: 获取管理员的日志文件夹列表接口。
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "获取成功",
        "data": ["文件夹1", "文件夹2", ...]
      }
      ```
  - 403 Forbidden
    - Body: 
      ```
      {
        "success": false,
        "msg": "无权限查看日志",
        "data": {}
      }
      ```

**POST /api/admin/json**

- Description: 获取管理员指定文件夹下的文件列表接口。
- Request:
  - Headers:
    - Content-Type: application/json
  - Body:
    ```
    {
      "uname": "用户名"
    }
    ```
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "获取成功",
        "data": ["文件1", "文件2", ...]
      }
      ```
  - 403 Forbidden
    - Body: 
      ```
      {
        "success": false,
        "msg": "无权限查看日志",
        "data": {}
      }
      ```

**POST /api/admin/v/json**

- Description: 获取管理员指定文件夹下的指定文件的JSON内容接口。
- Request:
  - Headers:
    - Content-Type: application/json
  - Body:
    ```
    {
      "uname": "用户名",
      "spider_name": "爬虫名称"
    }
    ```
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "获取成功",
        "data": {"JSON数据"}
      }
      ```
  - 403 Forbidden
    - Body: 
      ```
      {
        "success": false,
        "msg": "无权限查看日志",
        "data": {}
      }
      ```
  - 404 Not Found
    - Body: 
      ```
      {
        "success": false,
        "msg": "配置文件不存在",
        "data": {}
      }
      ```

**GET /api/user/locate**

- Description: 获取用户的IP地址接口。
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "获取成功",
        "data": {"ip": "用户IP地址"}
      }
      ```

**GET /api/user/limit**

- Description: 获取用户的进程数量限制接口。
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "获取成功",
        "data": 用户进程数量限制
      }
      ```

**POST /api/spider/create**

- Description: 创建爬虫进程接口。
- Request:
  - Headers:
    - Content-Type: application/json
  - Body:
    ```
    {
      "count": 进程数量,
      "info": "爬虫信息JSON字符串"
    }
    ```
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "进程创建成功",
        "data": {}
      }
      ```
  - 403 Forbidden
    - Body: 
      ```
      {
        "success": false,
        "msg": "创建失败，进程数量余额不足",
        "data": {}
      }
      ```

**GET /api/qrcode/info**

- Description: 获取二维码信息接口。
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "获取成功",
        "data": {"二维码信息"}
      }
      ```

**GET /api/qrcode/state**

- Description: 获取二维码扫码状态接口。
- Request:
  - Query Parameters:
    - qrId: 二维码ID
    - code: 扫码结果
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "等待扫码",
        "data": {"登录信息"}
      }
      ```
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "登录成功",
        "data": {"登录信息"}
      }
      ```
  - 200 OK
    - Body: 
      ```
      {
        "success": false,
        "msg": "二维码已过期",
        "data": {}
      }
      ```
  - 200 OK
    - Body: 
      ```
      {
        "success": false,
        "msg": "未知错误",
        "data": 错误代码
      }
      ```

**POST /api/note/search**

- Description: 搜索笔记接口。
- Request:
  - Headers:
    - Content-Type: application/json
  - Body:
    ```
    {
      "keywords": ["关键词1", "关键词2", ...],
      "sort_type": "排序类型",
      "note_type": "笔记类型",
      "needs": 需要的结果数量
    }
    ```
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "获取成功",
        "data": ["搜索结果URL1", "搜索结果URL2", ...]
      }
      ```

**POST /api/note/uncollect**

- Description: 取消收藏笔记接口。
- Request:
  - Headers:
    - Content-Type: application/json
  - Body:
    ```
    {
      "noteId": "笔记ID"
    }
    ```
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "操作成功",
        "data": {}
      }
      ```
  - 401 Unauthorized
    - Body: 
      ```
      {
        "success": false,
        "msg": "操作失败",
        "data": {}
      }
      ```

**POST /api/note/collected**

- Description: 检查笔记是否已收藏接口。
- Request:
  - Headers:
    - Content-Type: application/json
  - Body:
    ```
    {
      "noteId": "笔记ID"
    }
    ```
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "操作成功",
        "data": 是否已收藏
      }
      ```
  - 404 Not Found
    - Body: 
      ```
      {
        "success": false,
        "msg": "操作频繁",
        "data": false
      }
      ```

**POST /api/note/comment**

- Description: 评论笔记接口。
- Request:
  - Headers:
    - Content-Type: application/json
  - Body:
    ```
    {
      "noteId": "笔记ID",
      "comment": "评论内容",
      "userId": "用户ID"
    }
    ```
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "操作成功",
        "data": true
      }
      ```
  - 401 Unauthorized
    - Body: 
      ```
      {
        "success": false,
        "msg": "操作失败",
        "data": false
      }
      ```

**POST /api/note/collect**

- Description: 收藏笔记接口。
- Request:
  - Headers:
    - Content-Type: application/json
  - Body:
    ```
    {
      "noteId": "笔记ID"
    }
    ```
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "操作成功",
        "data": {}
      }
      ```
  - 401 Unauthorized
    - Body: 
      ```
      {
        "success": false,
        "msg": "操作失败",
        "data": {}
      }
      ```

**POST /api/note/like**

- Description: 点赞笔记接口。
- Request:
  - Headers:
    - Content-Type: application/json
  - Body:
    ```
    {
      "noteId": "笔记ID"
    }
    ```
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "操作成功",
        "data": {}
      }
      ```
  - 401 Unauthorized
    - Body: 
      ```
      {
        "success": false,
        "msg": "操作失败",
        "data": {}
      }
      ```

**POST /api/note/follow**

- Description: 关注笔记作者接口。
- Request:
  - Headers:
    - Content-Type: application/json
  - Body:
    ```
    {
      "noteId": "笔记ID"
    }
    ```
- Response:
  - 200 OK
    - Body: 
      ```
      {
        "success": true,
        "msg": "操作成功",
        "data": {"authorId": "作者ID"}
      }
      ```
  - 401 Unauthorized
    - Body: 
      ```
      {
        "success": false,
        "msg": "操作失败",
        "data": {}
      }
      ```