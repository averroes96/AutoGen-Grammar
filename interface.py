from flask import Flask,render_template

skills_app = Flask(__name__)

my_skills = [("Java", 85), ("PHP", 70), ("Python", 70)]

@skills_app.route("/")

def home_page():
    return render_template("home.html", title = "Home", custom_css = "home")
    
@skills_app.route("/skills")
def skills():
    return render_template(
        "skills.html", 
        title = "My Skills", 
        head = "Skills", 
        description = "These are my skills",
        skills = my_skills
        )

@skills_app.route("/add")
def add():
    return render_template("add.html", title = "Add", custom_css = "add")

@skills_app.route("/about")
def about():
    return render_template("about.html", title = "About")

if __name__ == "__main__":
    skills_app.run(debug=True)