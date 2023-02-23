## 框架介绍

本框架主要是基于 Python + HttpRunner3 + Pytest + Allure + log + YAML + 钉钉通知 + Jenkins 实现的Web UI自动化框架。

* 项目地址：https://gitee.com/dajun2259/api_auto_httprunner.git

## 技术栈
* Python3.9、Python3.7
* HttpRunner3

## 目录结构

    ├── attach                                 // 存放附件
    ├── common                                 // 配置
        └── config.yaml                        // 公共配置
        └── setting.py                         // 环境路径存放区域
    ├── data                                   // 测试用例数据
    ├── har                                    // 存放har文件
    ├── logs                                   // 日志层
    ├── picture                                // 存放截图，用于给allure追加附件
    ├── report                                 // 测试报告
    ├── testcase                               // 测试用例代码
    └── utils                                  // 工具类
        ├── allure_utils                       // allure工具类
            ├── allure_report_data.py          // allure报告数据清洗
        ├── db_utils                           // 数据库工具类
            └── mysql_utils.py                 // mysql基本操作
        ├── file_utils                         // 文件工具类
            ├── case_auto_param.py             // 获取用例模板参数
            ├── csv_utils.py                   // csv文件读取
            ├── file_zip.py                    // 文件压缩
            ├── files_utils.py                 // 文件的处理
            ├── har_py_utils.py                // har文件转换为测试用例代码py文件
            ├── txt_utils.py                   // txt文件的读写
            ├── yaml_py_utils.py               // yaml文件转换为测试用例代码py文件
            └── yaml_utils.py                  // yaml文件读写
        ├── log_utils                          // 日志工具类
            ├── loguru_utils.py                // 日志封装
        ├── metersphere_utils
            ├── import_har.py                  // har文件导入metersphere平台生成接口用例
            └── record_import_har.py           // 接口录制
        ├── notify
            ├── dingtalk_utils.py              // 钉钉通知
            └── sendmail_utils.py              // 邮件通知
        ├── other_utils                        // 日志工具类
            ├── codes_utils.py                 // 加密解密
            └── time_utils.py                  // 邮件通知
        ├── recording_utils                    // 接口录制
            ├── async_call_utils.py            // 异步处理装饰器
            └── mitmproxy_utils.py             // 录制封装
        ├── update_utils                       // 数据更新
            ├── up_data.py                     // 更新录制接口的信息
        └── requirements_utils.py              // 批量安装第三方库
    ├── .gitignore                             // git push不上传的目录、文件
    ├── README.md                              // 帮助文档
    ├── requirements.txt                       // 存储项目所用的第三方库
    ├── run.py                                 // 程序运行入口