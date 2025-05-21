from flask import Flask, request, jsonify, json
import subprocess

app = Flask(__name__)

#Глав страница
@app.route('/')
def main_page():
    return '''
        <h1>Добро пожаловать!</h1>
        <a href="/add_device" style="
            display:inline-block;
            padding:10px 20px;
            margin:10px;
            background-color:#228B22;
            color:white;
            text-decoration:none;
            border-radius:4px;">Добавить устройство</a>
        <a href="/devices" style="
            display:inline-block;
            padding:10px 20px;
            margin:10px;
            background-color:#2196F3;
            color:white;
            text-decoration:none;
            border-radius:4px;">Список устройств</a>
        <a href="/info" style="
            display:inline-block;
            padding:10px 20px;
            margin:10px;
            background-color:#9400D3;
            color:white;
            text-decoration:none;
            border-radius:4px;">Неполная помощь</a>
    '''
@app.route('/info', methods=['GET'])
def info():
    return'''
     <h1>Добро пожаловать на информационную страницу!<br>Чтобы узнать свой ip, MAC-адреса нужно бла бла бла</h1>
     <a href="/" style="
            display:inline-block;
            padding:10px 20px;
            margin:10px;
            background-color:#FF8C00;
            color:white;
            text-decoration:none;
            border-radius:4px;">На главную</a>

    '''


@app.route('/wake', methods=['POST'])
def wake():
    data = request.json
    device_name = data.get('device_name')
    if not device_name:
        return jsonify({'status': 'error', 'message': 'Нет имени устройства'}), 400
    # запуск скрипта для включения устройства
    result = subprocess.run(['python', 'wake_device.py', device_name], capture_output=True)
    if result.returncode == 0:
        return jsonify({'status': 'success', 'message': f'{device_name} включен'}), 200
    else:
        return jsonify({'status': 'error', 'message': result.stderr.decode('utf-8')}), 500

@app.route('/wake', methods=['GET'])
def wake_get():
    return "Это API для включения устройств. Используйте POST-запрос для включения."

#Добавление нового устр-ва
@app.route('/add_device', methods=['GET'])
def add_device_form():
    return '''
        <h2>Добавить новое устройство</h2>
        <form action="/add_device" method="post">
            <label>Название устройства:</label><br>
            <input type="text" name="name"><br><br>
            <label>IP-адрес:</label><br>
            <input type="text" name="ip"><br><br>
            <label>MAC-адрес:</label><br>
            <input type="text" name="mac"><br><br>
            <input type="submit" value="Добавить" style="
             padding: 10px 20px;
             background-color: #228B22; /* зеленый цвет */
             color: white;
             border: none;
             border-radius: 4px;
             font-size: 16px;
             cursor: pointer;
             transition: background-color 0.3s;">
            <a href="/" style="
            display:inline-block;
            padding:10px 20px;
            margin:10px;
            background-color:#FF8C00;
            color:white;
            text-decoration:none;
            border-radius:4px;">На главную</a>
        </form>
    ''' 
@app.route('/add_device', methods=['POST'])
def add_device_submit():
    name = request.form.get('name')
    ip = request.form.get('ip')
    mac = request.form.get('mac')

    if not all([name, ip, mac]):
        return 'Пожалуйста, заполните все поля.', 400

    # Загружаем базу устройств
    with open('devices.json', 'r', encoding='utf-8') as f:
        devices = json.load(f)

    if name in devices:
        return f"Устройство с именем '{name}' уже есть.", 400

    # Добавляем и сохраняем
    devices[name] = {'ip': ip, 'mac': mac}
    with open('devices.json', 'w', encoding='utf-8') as f:
        json.dump(devices, f, ensure_ascii=False, indent=4)

    return f"Устройство '{name}' успешно добавлено. <a href='/add_device'>Добавить ещё</a>, <a href='/devices'>Список устройств</a>"

#список уст-тв
@app.route('/devices')
def show_devices():
    with open('devices.json', 'r', encoding='utf-8') as f:
        devices = json.load(f)

    html = '''
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 80%; margin-bottom: 20px; }
            th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
            th { background-color: #f2f2f2; }
            a.button {
                display: inline-block;
                padding: 8px 12px;
                background-color: #e74c3c; /* красный цвет */
                color: white;
                text-decoration: none;
                border-radius: 4px;
                transition: background-color 0.3s;
            }
            a.button:hover {
                background-color: #c0392b;
            }
        </style>
    </head>
    <body>
        <h2>Сохранённые устройства</h2>
        <table>
            <tr><th>Название</th><th>IP</th><th>MAC</th><th>Удаление</th></tr>
    '''

    for name, info in devices.items():
        html += '<tr>'
        html += f'<td>{name}</td>'
        html += f'<td>{info.get("ip")}</td>'
        html += f'<td>{info.get("mac")}</td>'
        # Кнопка удаления как стильная ссылка
        html += f'<td><a href="/delete_device/{name}" class="button">Удалить</a></td>'
        html += '</tr>'

    html += '''
        </table>
        <a href="/add_device" class="button" style="background-color:#228B22;">Добавить устройство</a>
        <a href="/" class="button" style="background-color:#FF8C00;">На главную</a>
    </body>
    </html>
    '''
    return html

#Удаление данных
@app.route('/delete_device/<name>')
def delete_device(name):
    # Загружаем базу устройств
    with open('devices.json', 'r', encoding='utf-8') as f:
        devices = json.load(f)

    # Удаляем устройство, если есть
    if name in devices:
        del devices[name]
        # Записываем обратно в файл
        with open('devices.json', 'w', encoding='utf-8') as f:
            json.dump(devices, f, ensure_ascii=False, indent=4)
        return f"Устройство '{name}' удалено. <a href='/devices'>Вернуться к списку</a>"
    else:
        return f"Устройство '{name}' не найдено. <a href='/devices'>Вернуться к списку</a>"
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

   