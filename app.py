from flask import Flask, request, flash, render_template
from sqlalchemy import Column, create_engine
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()


class Person(Base):
    __tablename__ = "person"

    id_person = Column(Integer, primary_key=True)
    name = Column(String(255))
    email = Column(String(255))

    def __repr__(self):
        return f"Person(id_person={self.id_person!r}, name={self.name!r}, email={self.email!r})"


app = Flask(__name__)
app.secret_key = "secret"
engine = create_engine('postgresql://postgres@web-server.c4eriylmfwmr.sa-east-1.rds.amazonaws.com:5432/web_server')

people = []


def save_user(user: Person):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.close()


def save_user_mock(user: Person):
    people.append(user)


@app.route('/', methods=('GET', 'POST'))
def register_form():  # put application's code here
    if request.method == 'POST':
        name = request.form['nameInput']
        email = request.form['emailInput']

        if not name or not email:
            flash('All data required!')
        else:
            user = Person(name=name, email=email)
            save_user(user=user)
            return render_template('register.html', people=people)

    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
