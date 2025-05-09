from flask import Flask,request,url_for,render_template,redirect
app=Flask(__name__)
contacts={}
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        print(request.form)
        username=request.form.get('username')
        password=request.form.get('password')
        phoneno=request.form.get('phoneno')
        email=request.form.get('email')
        if not username in contacts:
            contacts[username]={'username':username,'password':password,'phoneno':phoneno,'email':email,'user_contacts':{}}
            return redirect(url_for('login'))
        else:
            return 'user already exists'
    return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        print(request.form)
        username=request.form.get('username')
        password=request.form.get('password')
        email=request.form.get('email')
        if username in contacts:
            if contacts[username]['password']==password:
                if contacts[username]['email']==email:
                    return redirect(url_for('navbar',uname=username))
                else:
                    return 'wrong email'
            else:
                return 'wrong password'
        else:
            return 'user not found'
    return render_template('login.html')
@app.route('/navbar/<uname>')
def navbar(uname):
    return render_template('navbar.html',uname=uname,user_contacts=contacts[uname]['user_contacts'])
@app.route('/add/<uname>',methods=['POST','GET'])
def add(uname):
    if request.method=='POST':
        print(request.form)
        name=request.form.get('name')
        phoneno=request.form.get('phoneno')
        email=request.form.get('email')
        if name not in contacts[uname]['user_contacts']: 
            contacts[uname]['user_contacts'][name] = {'phoneno': phoneno, 'email': email}
            return redirect(url_for('navbar', uname=uname)) 
        else:
            return 'name already exists..!'
    return render_template('add_contact.html')
@app.route('/edit/<uname>',methods=['POST','GET'])
def edit(uname):
    if request.method=='POST':
        print(request.form)
        name=request.form.get('name')
        if name in contacts[uname]['user_contacts']:
            print(request.form)
            phoneno=request.form.get('phoneno')
            email=request.form.get('email')
            contacts[uname]['user_contacts'][name]={'phoneno':phoneno,'email':email}
            return redirect(url_for('navbar',uname=uname))
        else:
            return 'name not found..!'
    return render_template('edit.html')
@app.route('/view/<uname>')
def view(uname):
    return render_template('view_contacts.html',contacts=contacts[uname]['user_contacts'])
@app.route('/delete/<uname>')
def delete(uname):
    return render_template('delete_contacts.html', uname=uname, contacts=contacts[uname]['user_contacts'])
@app.route('/delete_contact/<uname>/<contact_name>', methods=['POST'])
def delete_contact(uname, contact_name):
    if contact_name in contacts[uname]['user_contacts']:
        del contacts[uname]['user_contacts'][contact_name]
    return redirect(url_for('delete', uname=uname))
@app.route('/logout')
def logout():
    return redirect('login')
app.run(debug=True,use_reloader=True)