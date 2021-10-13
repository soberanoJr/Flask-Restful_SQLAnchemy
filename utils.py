from models import People


def insert(name, age):
    person = People(name=name, age=age)
    print(f"Person {person.name} (Age: {person.age}) inserted successfully!")
    person.save()


def show():
    people = People.query.all()
    print(people)


def query(name):
    person = People.query.filter_by(name=name).first()
    print(f"Id: {person.id}")
    print(f"Name: {person.name}")
    print(f"Age: {person.age}")



def delete(name):
    person = People.query.filter_by(name=name).first()
    person.delete()


if __name__ == '__main__':
    # insert("D", 4)
    show()
    # query("D")
    # change("C")
    # delete("A")
