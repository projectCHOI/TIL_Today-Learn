# pip install Flask
# Flask? = 기본적인 웹 서비스 기능을 제공


from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>로또 번호 생성기</title>
</head>
<body>
    <h1>로또 번호 생성기</h1>
    <form method="post">
        반드시 포함해야 하는 숫자(띄어쓰기로 구분): <input type="text" name="required"><br>
        반드시 제외할 숫자(띄어쓰기로 구분): <input type="text" name="excluded"><br>
        <input type="submit" value="생성하기">
    </form>
    {% if numbers %}
        <h2>출력된 번호: {{ numbers }}</h2>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def lotto():
    if request.method == 'POST':
        required_numbers = request.form.get('required', '')
        exclude_numbers = request.form.get('excluded', '')
        required_list = [int(num) for num in required_numbers.split()] if required_numbers else []
        exclude_list = [int(num) for num in exclude_numbers.split()] if exclude_numbers else []
        numbers = generate_numbers(required_list, exclude_list)
        return render_template_string(HTML, numbers=numbers)
    return render_template_string(HTML, numbers=None)

def generate_numbers(required_numbers, exclude_numbers):
    all_numbers = list(range(1, 46))
    for num in required_numbers:
        if num not in all_numbers:
            all_numbers.append(num)
    for num in exclude_numbers:
        if num in all_numbers:
            all_numbers.remove(num)
    return random.sample(all_numbers, 6)

if __name__ == '__main__':
    app.run(debug=True)
