# A Personal app to allow conversation with ChatGPT3 from OPENAI via SMS/WhatsApp by Twilio 

## Flask folder layout 

- `flaskr/` a python package containing your app code and files 
- `tests/` a directory containing test modules 
- `venv/` a python virtual env where flask and other dependencies are installed 
- `.git/` for version control 
- `instance/` flask's `.env/` folder

## functions 

- `view` function is the code you write to respond to requests to your application 
  - flask uses patterns to match the incoming request URL to the view that should handle it 
  - it returns data that flasks turns into an outgoing response 
  - flask can also generate a URL to a view based on its name and arguments 
- `blueprint` is a way to organize a group of related views and other code 
  - it is then registered with the application when it is available in the factory function 
  - `Flaskr/` will have two blueprints, one for authentication and one for the blog posts functions.  

## Blueprints 

- [endpoints and URLs](https://flask.palletsprojects.com/en/2.2.x/tutorial/views/#endpoints-and-urls) 
- [require Authentication in other views by using wrappers](https://flask.palletsprojects.com/en/2.2.x/tutorial/views/#require-authentication-in-other-views) 

## Templates 

- They are located in the `flaskr/` folder  
- They are files that contain static data as well as placeholders for dynamic data 
- uses [Jinja](https://jinja.palletsprojects.com/templates/) template library 
  - they autoescape problematic inputs in HTML 
  - improves safety 
  - `{{ }}` is an expression that will be output to the final document 
  - `{% %}` denotes a control flow statement like `if` or `for` 
  - unlike Python, blocks are denoted by start and end tags rather than indentation 
- 