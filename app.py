# Flask web uygulaması - Ortak Arkadaş Bulucu
# Bu uygulama, kullanıcılar arasındaki ortak arkadaşları bulmak için bir web arayüzü sağlar.
# Kullanıcı ekleme, arkadaşlık ilişkisi kurma ve ortak arkadaş bulma işlemlerini gerçekleştirir.

from flask import Flask, render_template, request, jsonify
from ortakarkadasbulma import HashTable, find_common_friends


app = Flask(__name__)


friendship_table = HashTable()

@app.route('/')
def home():
    
    return render_template('index.html')

@app.route('/users', methods=['GET'])
def get_users():
   
    users = list(friendship_table.table.keys())
    return jsonify({
        'success': True,
        'users': users
    })

@app.route('/user/<username>/friends', methods=['GET'])
def get_user_friends(username):

    friends = friendship_table.get(username)
    if friends is None:
        return jsonify({
            'success': False,
            'error': f'Kullanıcı bulunamadı: {username}'
        })
    return jsonify({
        'success': True,
        'friends': friends
    })

@app.route('/user', methods=['POST'])
def add_user():
  
    username = request.form.get('username')
    if not username:
        return jsonify({
            'success': False,
            'error': 'Kullanıcı adı gerekli'
        })
    
    if username in friendship_table.table:
        return jsonify({
            'success': False,
            'error': 'Bu kullanıcı zaten mevcut'
        })
    
    friendship_table.insert(username, [])
    return jsonify({
        'success': True,
        'message': f'{username} başarıyla eklendi'
    })

@app.route('/friendship', methods=['POST'])
def add_friendship():
    
    user1 = request.form.get('user1')
    user2 = request.form.get('user2')
    
    if not user1 or not user2:
        return jsonify({
            'success': False,
            'error': 'İki kullanıcı adı da gerekli'
        })
    
    if user1 not in friendship_table.table:
        return jsonify({
            'success': False,
            'error': f'{user1} kullanıcısı bulunamadı'
        })
    
    if user2 not in friendship_table.table:
        return jsonify({
            'success': False,
            'error': f'{user2} kullanıcısı bulunamadı'
        })
    

    user1_friends = friendship_table.get(user1)
    user2_friends = friendship_table.get(user2)
    
    if user2 not in user1_friends:
        user1_friends.append(user2)
        friendship_table.insert(user1, user1_friends)
    
    if user1 not in user2_friends:
        user2_friends.append(user1)
        friendship_table.insert(user2, user2_friends)
    
    return jsonify({
        'success': True,
        'message': f'{user1} ve {user2} arkadaş oldular'
    })

@app.route('/find_friends', methods=['POST'])
def find_friends():
   
    user1 = request.form.get('user1')
    user2 = request.form.get('user2')
    
    try:
        common_friends = find_common_friends(user1, user2, friendship_table)
        return jsonify({
            'success': True,
            'common_friends': common_friends
        })
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=8080, debug=True) 