from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home_page():
    return render_template('index.html')

@app.route('/math',methods=['POST'])
def arithmetic_operations():
    if request.method == 'POST':
        operation = request.form['operation']
        num1 = int(request.form['num1'])
        num2 = int(request.form['num2'])

        if operation == "sum":
            r = num1+num2
            result = "Sum of "+str(num1)+" and "+str(num2)+" is : "+str(r)
        if operation == "subtract":
            r = num1-num2
            result = "Subtraction of "+str(num1)+" and "+str(num2)+" is : "+str(r)
        if operation == "multiply":
            r = num1*num2
            result = "Product of "+str(num1)+" and "+str(num2)+" is: "+str(r)
        if operation == "division":
            r = num1/num2
            result = "Division of "+str(num1)+" and "+str(num2)+" is: "+str(r)
        if operation == "average":
            r = (num1+num2)/2
            result = "The average of "+str(num1)+" and "+str(num2)+" is : "+str(r)

        return render_template('result.html', result=result)

if __name__ == '__main__':
    print("Hello janu!! I'm Ok..Go Ahead :)")
    app.run(debug=True)