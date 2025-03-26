from flask import Flask, jsonify, request
from typing import List

app = Flask(__name__)

# 1. Функция для генерации первых n чисел Фибоначчи
def fibonacci(n: int) -> List[int]:
    fib_sequence = []
    a, b = 0, 1
    for _ in range(n):
        fib_sequence.append(a)
        a, b = b, a + b
    return fib_sequence

# 2. Функция для проверки, является ли число палиндромом
def is_palindrome(num: int) -> bool:
    return str(num) == str(num)[::-1]

# 3. Узел связного списка
class ListNode:
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next

# Функция для разворота связного списка
def reverse_linked_list(head: ListNode) -> ListNode:
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev

# API для получения первых n чисел Фибоначчи
@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    n = request.args.get('n', type=int)
    if n is None or n <= 0:
        return jsonify({'error': 'Invalid input'}), 400
    fib_sequence = fibonacci(n)
    return jsonify(fib_sequence)

# API для проверки числа на палиндром
@app.route('/palindrome', methods=['GET'])
def check_palindrome():
    num = request.args.get('number', type=int)
    if num is None:
        return jsonify({'error': 'Invalid input'}), 400
    result = is_palindrome(num)
    return jsonify({'number': num, 'is_palindrome': result})

# API для разворота связного списка
@app.route('/reverse_linked_list', methods=['POST'])
def reverse_list():
    data = request.json
    values = data.get('values', [])
    
    # Создание связного списка из входных данных
    head = None
    for value in reversed(values):
        head = ListNode(value, head)

    # Разворот связного списка
    reversed_head = reverse_linked_list(head)

    # Получение значений из развернутого списка
    reversed_values = []
    current = reversed_head
    while current:
        reversed_values.append(current.value)
        current = current.next

    return jsonify(reversed_values)

if __name__ == '__main__':
    app.run(debug=True)

# Пример тестов (можно использовать unittest или pytest)
import requests

def test_fibonacci():
    response = requests.get('http://127.0.0.1:5000/fibonacci?n=10')
    assert response.json() == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

def test_palindrome():
    response = requests.get('http://127.0.0.1:5000/palindrome?number=121')
    assert response.json() == {'number': 121, 'is_palindrome': True}

def test_reverse_linked_list():
    response = requests.post('http://127.0.0.1:5000/reverse_linked_list', json={'values': [1, 2, 3]})
    assert response.json() == [3, 2, 1]
