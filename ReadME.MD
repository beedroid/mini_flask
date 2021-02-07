# Flask restful工程模板
## 目录结构
- app 工程源码文件
    - server
      - api
      - controller
    - config
    - dao
    - utils
    - models.py
- migrations 数据库迁移
- tests 单元测试
- venv python虚拟环境
- config.py 全局配置文件,包括数据库配置
- manage.py 执行入口
- requirements.txt 用于记录所有的依赖包和版本号，用于多设备上同步开发环境(pip freeze> requirements.txt / pip install -r requirements.txt)

## 依赖库
* `flask-script` 可以自定义命令行命令，用来启动程序或其它任务；
* `flask-login` sesion登录态管理，[文档](https://github.com/maxcountryman/flask-login/)
* `flask-sqlalchemy` 用来管理数据库的工具，支持多种数据库后台；
* `flask-migrate` 是数据库迁移工具，该工具命令集成到 `flask-script`中，方便在命令行中进行操作。

## 启动
`. ./venv/bin/activate && python manage.py runserver`