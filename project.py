from flask import Flask, render_template, redirect, url_for,request , session
from flask import escape, flash
from sqlalchemy import desc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup2 import Base, Users, Posts, Comments, Questions, Comments_questions
import random
import string
import os
import hashlib

def make_salt():
	return ''.join(random.choice(string.ascii_letters) for x in range(5))

def hash_pass(s,salt= None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(s.encode('utf-8') + salt.encode('utf-8')).hexdigest()
	return "%s,%s"%(h,salt)

def check_secure_pass(s,password):
	salt = password.split(',')[1]
	return password == hash_pass(s.encode('utf-8'),salt)


app = Flask(__name__)
engine = create_engine('sqlite:///Blog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
sessions = DBSession()
username_for_access = ["admin name here"]

@app.route('/')
@app.route('/index')
def index():
	all_post = sessions.query(Posts).order_by(desc(Posts.time_created))
	all_comments = sessions.query(Comments).all()
	if 'username' in session:
		username_session = escape(session['username']).capitalize()
		user = sessions.query(Users).all()
		return render_template('index.html',
			user=username_session, Post = all_post,comments=all_comments)
	return render_template('index.html', Post =all_post,comments=all_comments)


@app.route('/post', methods = ['GET', 'POST'])
def post():
	if request.method == 'POST':
		username_session = escape(session['username'])
		title = request.form['title']
		post = request.form['post_text']
		username = sessions.query(Users).all()
		value = ''
		for i in username:
			if username_session == i.name:
				value = i.id

		new_post = Posts(title=title , PostText=post,Owner_name=
			username_session, Owner_id=value)
		sessions.add(new_post)
		sessions.commit()

		return redirect(url_for('index'))
	else:
		if 'username' in session:
			username_session = escape(session['username'])
			value = 0
			for i in username_for_access:
				if username_session == i:
					value = 1
			if value == 1:
				user = sessions.query(Users).all()
				return render_template('post.html',user=user)
		
		return redirect(url_for('login'))


##comments for post starts here 
@app.route('/post/<int:postId>/', methods =['GET', 'POST'])
def Post_comments(postId):
	if request.method == 'POST':
		username_session = escape(session['username'])
		Commenter_id = sessions.query(Users).filter_by(name = username_session).one()

		message = request.form['message']
		new_comment = Comments(Comment = message, Commenter_Id= Commenter_id.id, Post_id= postId)
		sessions.add(new_comment)
		sessions.commit()
		users = sessions.query(Users).all()
		post = sessions.query(Posts).filter_by(id=postId).one()
		Comment = sessions.query(Comments).filter_by(Post_id=postId).order_by(desc(Comments.time_created))
		flash('Succesfully commented')
		return render_template('comment.html',user=username_session, post = post, comment=Comment, users=users)

	else:
		if 'username' in session:
			username_session = escape(session['username'])
			post = sessions.query(Posts).filter_by(id=postId).one()
			users = sessions.query(Users).all()
			Comment = sessions.query(Comments).filter_by(Post_id=postId).order_by(desc(Comments.time_created))
			return render_template('comment.html',post=post,users=users, user= username_session,comment=Comment)
		flash('You need to login to view comments')
		return redirect(url_for('login'))





#------------------------------------------------------------------------------------------------


#question and unanswerd question route begins here
@app.route('/questions')
def questions():
	all_post = sessions.query(Questions).order_by(desc(Questions.time_created))
	all_comments = sessions.query(Comments_questions).all()
	if 'username' in session:
		username_session = escape(session['username'])
		return render_template('questions.html',user=username_session, 
			post=all_post,comments=all_comments )
	return render_template('questions.html',post=all_post, comments=all_comments )


@app.route('/questions/post' , methods=['GET', 'POST'])
def questions_post():
	if request.method == 'POST':
		username_session = username_session = escape(session['username'])
		all_post = sessions.query(Users).filter_by(name = username_session).one()
		Text = request.form['text']
		new_question = Questions(Text = Text, Owner_name= username_session, Questioner_Id=all_post.id)

		sessions.add(new_question)
		sessions.commit()
		flash('Question added succesfully')
		return redirect(url_for('questions'))
	else:
		if 'username' in session:
			return render_template('question_post.html')
		else:
			flash('login is necessary to ask a question')
			return redirect(url_for('login'))

@app.route('/questions/<int:questionId>', methods=['GET','POST'])
def question_comment(questionId):
	if request.method == 'POST':
		username_session = escape(session['username'])
		Commenter_id = sessions.query(Users).filter_by(name = username_session).one()

		message = request.form['message']
		new_comment = Comments_questions(Comment = message, Commenter_Id= Commenter_id.id, Question_id= questionId)
		sessions.add(new_comment)
		sessions.commit()
		users = sessions.query(Users).all()
		question = sessions.query(Questions).filter_by(id=questionId).one()
		Comment = sessions.query(Comments_questions).filter_by(Question_id=questionId).order_by(desc(Comments_questions.time_created))
		flash('Succesfully commented')
		return render_template('questionComment.html',user=username_session, question=question, comment=Comment, users=users)

	else:
		if 'username' in session:
			username_session = escape(session['username'])
			question = sessions.query(Questions).filter_by(id=questionId).one()
			users = sessions.query(Users).all()
			Comment = sessions.query(Comments_questions).filter_by(Question_id=questionId).order_by(desc(Comments_questions.time_created))
			return render_template('questionComment.html',question=question,users=users, user= username_session,comment=Comment)

		flash('You need to login to view comments')
		return redirect(url_for('login'))


@app.route('/contactus')
def contact():
	if 'username' in session:
		username_session = escape(session['username'])
		return render_template('contact.html',user=username_session)
	return render_template('contact.html')


#login route
@app.route('/login', methods =['GET', 'POST'])
def login():
	if request.method == 'POST':
		name = request.form['username']
		password = request.form['password']
		user_password = ''
		username = sessions.query(Users).all()
		value = 0

		for i in username:
			if name == i.name:
				user_password = i.password
				value = 1

			

		if value == 0:
			return render_template('login.html', 
				error = 'invalid user name or password')

		else:
			check_password = check_secure_pass(password, user_password)

			if check_password:
				session['username'] = name
				flash('WELCOME BACK %s'%name)
				return redirect(url_for('index'))

			return render_template('login.html', error =
			  'invalid user name or password')





	else:
		if 'username' in session:
			username_session = escape(session['username']).capitalize()
			return redirect(url_for('index'))

		return render_template('login.html')





#logout route
@app.route('/logout')
def logout():
	session.clear()
	flash('You have succesfully logged out, fill the details to login again')
	return redirect(url_for('login'))





@app.route('/signup', methods =['GET', 'POST'])
def signup():
	if request.method == 'POST':
		name = request.form['username']
		password = request.form['password']
		verify_password = request.form['verify']
		email = request.form['email']
		value = 0
		username = sessions.query(Users).all()

		for i in username:
			if name == i.name:
				value = 1
			


		if password != verify_password:
			return render_template('signup.html', error="password doesn't match")

		elif value == 1:
			return render_template('signup.html', error=
			'username %s already exits try anyother username'%name)
			

		
		else:
			password_hash = hash_pass(password)
		
			new_user = Users(name= name , password =
			 password_hash, email = email)

			sessions.add(new_user)
			sessions.commit()
			session['username'] = name
			flash('Welcome to CES BLOG,help us to make this community more awesome')
			return redirect(url_for('index'))

			

		

	else:
		if 'username' in session:
			username_session = escape(session['username']).capitalize()
			return redirect(url_for('index'))
		
		return render_template('signup.html')
		
@app.route('/users', methods = ['GET','POST'])
def users():
	if request.method == 'POST':
		name = request.form['username']
		password = request.form['password']
		if (name == 'abhishek') and (password == 'abhishek'):
			username = sessions.query(Users).all()
			return render_template('users.html', user = username)
		return redirect(url_for('index'))
	else:
		if 'username' in session:
			username_session = escape(session['username'])
			value = 0
			for i in username_for_access:
				if username_session == i:
					value = 1
			if value == 1:
				user = sessions.query(Users).all()
				return render_template('user.html')
			return redirect(url_for('index'))
		return redirect(url_for('login'))




if __name__ == '__main__':
	app.secret_key = "unknown_cookie_values_present_here_so_that_it_remains_secret_so_dont worry_its still secret"
	app.debug = True
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)