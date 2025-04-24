from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder='project/templates',
    static_folder='project/static'
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/classes')
def classes():
    return render_template('classes.html')

@app.route('/deadlines')
def deadline():
    return render_template('deadline.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/subject')
def subject():
    return render_template('subject.html')

if __name__ == '__main__':
    app.run(debug=True)
