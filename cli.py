from main import app, db
from models import Admin
import click
from werkzeug.security import generate_password_hash

# Defines Custom Commands

@click.command(name='migrate')
def migrate():
    # Create Table
    db.create_all()
    click.echo('Migrated Successfully!')

app.cli.add_command(migrate)

@click.command(name='resetdb')
def resetdb():
    db.drop_all()
    click.echo('Database reseted successfully')

app.cli.add_command(resetdb)

@click.command(name='createsuperuser')
@click.argument("email")
def createsuperuser(email):
    check_email = Admin.query.filter(Admin.email == email).first()
    if check_email is not None:
        click.echo('Email already exists. Please try with another email.')
    else:
        admin = Admin(email=email, password=generate_password_hash('admin'))
        db.session.add(admin)
        db.session.commit()
        click.echo('Superuser created successfully! & default password set to "admin"')

app.cli.add_command(createsuperuser)