# CDMS_2023_Project ：bookstore项目报告

| 课程名称：当代数据管理系统 | 项目名称：bookstore | 指导老师：周烜 |
| -------------------------- | ------------------- | -------------- |
| 成员：李嘉豪               | 学号：10204804434   | 年级：2021     |
| 成员：杨茜雅               | 学号：10215501435   | 年级：2021     |
| 成员：王溢阳               | 学号：10204602470   | 年级：2021     |

## 一. 实验要求

- 实现一个提供网上购书功能的网站后端
  - 网站支持书商在上面开商店，购买者可以通过网站购买。买家和卖家都可以注册自己的账号。一个卖家可以开一个或多个网上商店，买家可以为自已的账户充值，在任意商店购买图书。
  - 支持 下单->付款->发货->收货 流程

- 功能

  - 1.实现对应接口的功能，见项目的doc文件夹下面的.md文件描述 （60%），其中包括：

    - 1)用户权限接口，如注册、登录、登出、注销

    - 2)买家用户接口，如充值、下单、付款

    - 3)卖家用户接口，如创建店铺、填加书籍信息及描述、增加库存

      **通过对应的功能测试，所有test case都pass**

  - 2.为项目添加其它功能 ：（40%）
    - 1)实现后续的流程：发货 -> 收货
    - 2)搜索图书
      - 用户可以通过关键字搜索，参数化的搜索方式；
      - 如搜索范围包括，题目，标签，目录，内容；全站搜索或是当前店铺搜索。
      - 如果显示结果较大，需要分页 (使用全文索引优化查找)

  - 3)订单状态，订单查询和取消定单
    - 用户可以查自已的历史订单，用户也可以取消订单。取消定单可由买家主动地取消定单，或者买家下单后，经过一段时间超时仍未付款，定单也会自动取消。

- 要求

  - 2～3人一组，做好分工，完成下述内容：

    - 1.bookstore文件夹是该项目的demo，采用flask后端框架与sqlite数据库，实现了前60%功能以及对应的测试用例代码。

      - **要求大家创建本地 MongoDB 数据库，将`bookstore/fe/data/book.db`中的内容以合适的形式存入本地数据库，后续所有数据读写都在本地的 MongoDB 数据库中进行**
      - 书本的内容可自行构造一批，也可参从网盘下载，下载地址为：https://pan.baidu.com/s/1bjCOW8Z5N_ClcqU54Pdt8g

      提取码：hj6q

    - 2.在完成前60%功能的基础上，继续实现后40%功能，要有接口、后端逻辑实现、数据库操作、代码测试。对所有接口都要写test case，通过测试并计算测试覆盖率（尽量提高测试覆盖率）。

    - 3.尽量使用索引，对程序与数据库执行的性能有考量

    - 4.尽量使用git等版本管理工具

    - 5.不需要实现界面，只需通过代码测试体现功能与正确性

- 报告内容

  - 1.每位组员的学号、姓名，以及分工

  - 2.文档数据库设计：文档schema

  - 3.对60%基础功能和40%附加功能的接口、后端逻辑、数据库操作、测试用例进行介绍，展示测试结果与测试覆盖率。

  - 4.如果完成，可以展示本次大作业的亮点，比如要求中的“3 4”两点。

    注：验收依据为报告，本次大作业所作的工作要完整展示在报告中

- 考核标准

  1. 没有提交或没有实质的工作，得D
  2. 完成"要求"中的第1点，可得C
  3. 完成前3点，通过全部测试用例且有较高的测试覆盖率，可得B
  4. 完成前2点的基础上，体现出第3 4点，可得A
  5. 以上均为参考，最后等级会根据最终的工作质量有所调整

## 二. 项目运行

- 目录结构

  ```
  bookstore
    |-- be                            后端
          |-- model                     后端逻辑代码
          |-- view                      访问后端接口
          |-- ....
    |-- doc                           JSON API规范说明
    |-- fe                            前端访问与测试代码
          |-- access
          |-- bench                   效率测试
          |-- data
              |-- book.db             sqlite 数据库(book.db，较少量的测试数据)
              |-- scraper.py          从豆瓣爬取的图书信息数据的代码
          |-- test                    功能性测试（包含对前60%功能的测试，不要修改已有的文件，可以提pull request或bug）
          |-- conf.py                 测试参数，修改这个文件以适应自己的需要
          |-- conftest.py             pytest初始化配置，修改这个文件以适应自己的需要
          |-- ....
    |-- be_rewrite.py                 改写be.db
    |-- book_rewrite.py               改写book.db
    |-- ER图
    |-- 2023_ECNU_PJ1_report.pdf      项目报告
    |-- ....
  ```

- 安装配置

  - requirements

    ```python
    simplejson==3.19.2
    lxml==4.9.2
    codecov==2.1.13
    coverage==7.3.2
    flask==2.0.0
    pre - commit==1.3.0
    pytest==7.4.0
    PyJWT==2.4.0
    requests==2.31.0
    Werkzeug>=2.0==2.0.0
    Jinja2>=3.0==3.1.2
    itsdangerous>=2.0==2.1.2
    click>=7.1.2==8.1.7
    iniconfig==1.1.1
    packaging==23.0
    pluggy<2.0,>=0.12==1.0.0
    idna<4,>=2.5==3.4
    urllib3<3,>=1.21.1==1.26.16
    certifi>=2017.4.17==2023.7.22
    MarkupSafe>=2.0==2.1.1
    ```

  - python 3.12

    进入bookstore文件夹下：

    安装依赖

    ```
    pip install -r requirements.txt
    ```

    初始化数据库

    ```python
    python book_rewrite.py
    python be_rewrite.py
    ```

    运行后端服务器

    ```python
    python3 app.py
    ```

    执行测试

    ```
    bash script/test.sh
    ```

## 三. 文档数据库设计

### 3.1 设计思路及数据库转化



### 3.2 ER图

![ER图](C:\Users\86133\Desktop\CDMS-2023\ER图.png)

### 3.3 表格结构

#### 3.3.1 book

| id     | title            | author | publisher | original_title   | translator | pub_year | pages | price | currency_unit | binding   | isbn   | author_intro | book_intro | content | tags | picture  |
| ------ | ---------------- | ------ | --------- | ---------------- | ---------- | -------- | ----- | ----- | ------------- | --------- | ------ | ------------ | ---------- | ------- | ---- | -------- |
| 书本id | 书本名称（中文） | 作者   | 出版社    | 书本名称（原名） | 译者       | 出版年份 | 页数  | 价格  | 货币单位      | 精装/平装 | isbn码 | 作者简介     | 书本简介   | 目录    | 标签 | 书本图片 |

注意：书本id仅表示表里所有信息相同的书，不包含书名相同但是译者信息等不同的一类书。

#### 3.3.2 user

| user_id | password | balance | tocken       | terminal       |
| ------- | -------- | ------- | ------------ | -------------- |
| 用户id  | 用户密码 | 余额    | 终端信息记录 | 登录时的终端号 |

注意：一个用户既可以买书又可以卖书，user_id仅代表bookstore中一个用户的账号

#### 3.3.3 user_store

| user_id | store_id |
| ------- | -------- |
| 卖家id  | 店铺id   |

#### 3.3.4 new_order

| order_id | user_id | store_id | payment_time |
| -------- | ------- | -------- | ------------ |
| 订单id   | 买家id  | 店铺id   | 付款时间     |

#### 3.3.5 new_order_detail

| order_id | book_id | price | count | state                              | order_time | delivery_time | receipt_time | payment_time |
| -------- | ------- | ----- | ----- | ---------------------------------- | ---------- | ------------- | ------------ | ------------ |
|          | 书本id  | 价格  | 数目  | 状态（下单0、付款1、发货2、收货3） | 下单时间   | 发货时间      | 收货时间     | 付款时间     |

注意：新增column有state\order_time\delivery_time\receipt_time\payment_time。主要用于订单状态的记录。

#### 3.3.6 store

| store_id | book_id | price | stock_level |
| -------- | ------- | ----- | ----------- |
| 店铺id   | 书本id  | 价格  | 库存        |

注意：由于之间注释过的书本id仅表示所有信息相同的书，不包括名字相同其他信息稍有不同的一类书。此处的库存仅代表该书本的数量。

## 四. 功能函数

### 4.1 用户功能

> 需求分析
>
> - 注册
>   - 生成终端标识
>   - 生成JWT Token(包含用户ID、终端标识和当前时间戳)
>   - 检查用户是否已经存在，可返回错误代码并显示“该账号已被注册”
>   - 创建用户（包含用户ID、密码、余额、TWT Token和终端标识）
>   - 异常处理901、成功执行200
>
> - 检查Token（安全措施：确认用户正确登录并持有有效Token）
>   - 获取用户信息、检查用户是否存在
>   - 从数据库中获取Token并解码
>   - 验证Token是否匹配并检查有效期（3600秒）
>
> - 检查user_id对应的密码是否正确
>   - 获取用户信息
>   - 获取密码并比较验证
>
> - 登录
>   - 校验密码
>   -  生成新Token
>   - 更新数据库记录
>
> - 登出
>   - 验证Token
>   - 生成新Token和终端标识
>   - 更新数据库记录
>
> - 注销账户 
>   - 删除用户记录
>
> - 更改密码
>   - 验证旧密码
>   - 生成新的Token和终端标识
>   - 更改数据库中的密码和Token



### 4.2 买家功能

> 需求分析
>
> - 充值
>   - 更新余额
>   - 更新数据库操作结果
>
> - 下单
>   - 生成订单id
>   - 遍历书籍列表、检查库存
>   - 创建订单详情和记录
>
> - 付款
>   - 验证订单有效性
>   - 检查订单状态是否未支付
>   - 验证用户信息及余额
>   - 计算订单总价
>   - 更新买家余额和订单状态



### 4.3 卖家功能

> - 创建店铺
>   - 检查店铺Id是否唯一
>   - 插入店铺记录
>
> - 添加书籍
>   - 检查书籍唯一性
>   - 解析书籍信息
>
> - 增加库存
>   - 检查书籍是否存在
>   - 更新库存



### 4.4 收货&发货

> 需求分析
>
> - 发货
>   - 检查订单是否存在
>   - 查询订单详情及状态
>   - 执行发货
>
> - 收货
>   - 验证订单状态
>   - 执行收货



### 4.5 搜索图书

> 需求分析
>
> - 全站搜索
>   - 验证搜索关键词
>   - 执行查询
>   - 返回结果
>
> - 当前店铺搜索
>   - 检查搜索关键词
>   - 确认店铺存在
>   - 执行搜索



### 4.6 订单

> 需求分析
>
> - 查询订单
>   - 判断订单是否存在
>   - 执行查询
>
> - 删除订单
>   - 查询订单状态
>     - 未付款（状态为0），则可以直接取消
>     - 已付款但未发货（状态为1），则需要执行退款流程。
>   - 删除订单
>     - 对于未付款订单，直接从订单详情和订单记录中删除订单，并调整库存。
>     - 对于已付款但未发货的订单，除了删除订单和调整库存外，还需要从卖家账户扣除相应金额并退款给买家。
>     - 如果订单已发货或已收货（状态大于1），则不能取消。



## 五. 测试

### 5.1 测试接口和样例

**测试fe/access/operations.py、be/model/operations.py中的所有函数以及绝大部分可能的error检查**

#### 5.1.1 发货&收货 test_delivery_receipt.py

#### 5.1.2 搜索 test_searchbook.py

#### 5.1.3 订单 test_order.py

**从创建订单、查询订单、删除订单以及卖家和买家等多个方面对功能进行测试：创建订单、删除不存在的订单、下单后查询订单、查询不存在的订单、发货后查询订单、收货后查询订单、下单未付款删除订单、下单并且付款之后删除订单等等。**

**共计14个测试，其中涉及访问接口以及直接访问，仅在报告中展示部分测试函数，具体内容查看fe/test/test_order.py**

```python
pre_run_initialization(self):初始化
```

>  `opera`: 传入名为`URL`的参数
>
> `uuid.uuid1()`: 生成唯一的UUID，与字"test_operations_seller_"拼接，得到唯一的`seller_id`、`buyer_id`、`store_id`。
>
> `seller_id`：卖家密码
>
> `buyer_id`：买家密码
>
> `register_new_buyer_auth()`：注册新的买家
>
> `gen_book`：将`seller_id`和`store_id`作为参数
>
> `get_seller()`：获取卖家对象
>
> `yield`：这些初始化操作包装为一个生成器

```python
test_cancel_order_ok(self):测试删除订单正常
test_cancel_non_exist_buyer_id(self):当买家id不存在时，测试删除订单，正确结果是无法删除
test_cancel_non_exist_buyer_direct_id(self):买家id不存在时，直接访问后端删除订单，正确结果是无法删除
test_cancel_non_exist_order_id(self):订单id不存在时，测试删除该订单。
test_processing_order(self): 下单后查询当前订单
test_processing_order_sent(self):发货后查询当前订单
test_processing_order_sent_error(self): 因为各种错误发货失败
test_sent_order_direct_cancer(self):发货后删除当前订单
test_processing_order_receive(self):收货后查询当前订单
test_processing_order_receipt_error(self): 因为各种错误收货失败
test_seller_processing_order_ok(self):卖家查询订单
```

### 5.2 测试结果截图

![image-20231102142243939](C:\Users\86133\AppData\Roaming\Typora\typora-user-images\image-20231102142243939.png)

![image-20231102142327658](C:\Users\86133\AppData\Roaming\Typora\typora-user-images\image-20231102142327658.png)

![image-20231102142420483](C:\Users\86133\AppData\Roaming\Typora\typora-user-images\image-20231102142420483.png)

共计61个测试用例，全部通过

![image-20231102142447708](C:\Users\86133\AppData\Roaming\Typora\typora-user-images\image-20231102142447708.png)

![image-20231102142532728](C:\Users\86133\AppData\Roaming\Typora\typora-user-images\image-20231102142532728.png)

![image-20231101002917340](C:\Users\86133\AppData\Roaming\Typora\typora-user-images\image-20231101002917340.png)

**紫色**：后40%要求的功能函数所在的文件，其中access给view发送请求，view转送给model处理请求，将处理结果返回给access。【100%】

**白色**: 整体覆盖率【71%】

**蓝色**：后端测试代码

- 新增功能代码：
  - be/model/operations.py: 功能【从view发送的请求，没有直接经过这里，因此覆盖率较低，但是功能都覆盖到了】
  - be/view/operations.py:发送请求
  - fe/access/operations.py: 后端接口【测试是对这里面的函数接口进行测试，五个接口全部覆盖，如图所示覆盖率100%】

- 新增测试代码：
  - fe/test/test_delivery_recipt.py:测试收货和发货
  - fe/test/test_booksearch.py:测试书本的搜索（全局和局部）
  - fe/test/test_order.py:测试订单（删除和搜索以及状态）

## 六. 遇到的问题

1.  `requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`

Q：① 传入接口的数据类型以及所需参数数量保持一致

​       ② 切换解释器至3.12及以上版本，重新配置环境

2. `assert 905 == 200`

Q：查看后端部分设置每种状态的返回值，与测试时返回的状态码保持一致。

3. `RuntimeError: Not running with the Werkzeug Server`

Q：flask版本太高，需要降低版本

       ```python
        pip install flask==2.0.0  
        pip install Werkzeug==2.0.0
       ```



## 七. 项目亮点

### 7.1 使用git版本管理工具



### 7.2 索引



## 八. 分工与合作

李嘉豪:

杨茜雅：

王溢阳：