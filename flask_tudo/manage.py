from app import app,db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

manage = Manager(app)
migrate = Migrate(app, db)
manage.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manage.run()
