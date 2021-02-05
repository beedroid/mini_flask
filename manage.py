import os
from app import app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

# 创建程序
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


# 增加shell和db两个命令，在命令行中可以直接使用
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
