from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup2 import Users, Base, Posts, Questions

engine = create_engine('sqlite:///Blog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
sessions = DBSession()


# Menu for UrbanBurger
user1 = Users(name="abhishek9", password= "justatrail")

sessions.add(user1)
sessions.commit()

user2 = Users(name="abhi71", password= "justatrail")

sessions.add(user2)
sessions.commit()


users3 = Users(name="abhi321", password= "justatrail")

sessions.add(users3)
sessions.commit()

post1 = Posts(title ="Making a bridge", PostText =
"Kaizen is coming. Dont worry it would be soon be there on 21 and 22nd january",
Owner_name =user1.name, Owner_id = user1.id)
sessions.add(post1)
sessions.commit()

post2 = Posts(title ="Random post", PostText =
"Kaizen is coming. Dont worry it would be soon be there on 21 and 22nd january",
Owner_name =user2.name, Owner_id=user2.id)
sessions.add(post2)
sessions.commit()

post3 = Posts(title ="Treasure Hunt", PostText =
"It will be conducted on january 6 to 7 .A very interesting event where in you can do a lot more work of finding real treasure",
Owner_name =users3.name, Owner_id =users3.id)
sessions.add(post3)
sessions.commit()

question1 = Questions(Questioner_Id=user2.id,Owner_name=user2.name, Text = "why is kaizen always conducted in january?")
sessions.add(question1)
sessions.commit()

question2 = Questions(Questioner_Id=users3.id,Owner_name=users3.name, Text = "Placement updates in Civil engineering?")
sessions.add(question2)
sessions.commit()

print "added users!"

