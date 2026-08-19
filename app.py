import json
import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'bbs_secret_key_12345'

POSTS_FILE = 'posts.json'
USERS_FILE = 'users.json'

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'adminpassword'

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                return [] if filename == POSTS_FILE else {}
    return [] if filename == POSTS_FILE else {}

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def init_admin():
    users = load_data(USERS_FILE)
    if ADMIN_USERNAME not in users:
        users[ADMIN_USERNAME] = {
            'password': generate_password_hash(ADMIN_PASSWORD),
            'is_admin': True
        }
        save_data(USERS_FILE, users)

init_admin()

@app.route('/', methods=['GET', 'POST'])
def index():
    posts = load_data(POSTS_FILE)
    users = load_data(USERS_FILE)

    if request.method == 'POST':
        if 'user' not in session:
            flash('投稿するにはログインが必要です。')
            return redirect(url_for('login'))
        
        content = request.form.get('content')
        if content:
            new_post = {
                'id': len(posts) + 1,
                'author': session['user'],
                'content': content
            }
            posts.append(new_post)
            save_data(POSTS_FILE, posts)
            return redirect(url_for('index'))

    is_admin = False
    if 'user' in session:
        user_info = users.get(session['user'], {})
        is_admin = user_info.get('is_admin', False)

    return render_template('index.html', posts=posts, user=session.get('user'), is_admin=is_admin)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        terms = request.form.get('terms')

        if not terms:
            flash('利用規約への同意が必要です。')
            return render_template('register.html')

        users = load_data(USERS_FILE)
        if username in users:
            flash('このユーザー名は既に存在します。')
            return render_template('register.html')

        users[username] = {
            'password': generate_password_hash(password),
            'is_admin': False
        }
        save_data(USERS_FILE, users)
        flash('会員登録が完了しました！ログインしてください。')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        users = load_data(USERS_FILE)
        user = users.get(username)

        if user and check_password_hash(user['password'], password):
            session['user'] = username
            flash('ログインしました。')
            return redirect(url_for('index'))
        else:
            flash('ユーザー名またはパスワードが違います。')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('ログアウトしました。')
    return redirect(url_for('index'))

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    if 'user' not in session:
        return redirect(url_for('login'))

    users = load_data(USERS_FILE)
    current_user = session['user']
    is_admin = users.get(current_user, {}).get('is_admin', False)

    posts = load_data(POSTS_FILE)
    new_posts = [p for p in posts if not (p['id'] == post_id and (is_admin or p['author'] == current_user))]
    save_data(POSTS_FILE, new_posts)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
                <label style="font-weight: bold;">暗証番号（4桁）:</label><br>
                <input type="password" name="passcode" required placeholder="番号を入力" style="width: 100%; padding: 8px; margin: 5px 0 10px 0; box-sizing: border-box;"><br>
                
                <label style="font-weight: bold;">メッセージ:</label><br>
                <textarea name="content" rows="4" required style="width: 100%; padding: 8px; margin: 5px 0 15px 0; box-sizing: border-box;"></textarea><br>
                
                <input type="submit" value="書き込む" style="background-color: #007aff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
            </form>
        </div>
        
        <h2>みんなの投稿</h2>
        {{% for msg in messages %}}
            <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 10px;">
                <div style="margin-bottom: 5px;">
                    <strong style="color: #007aff;">{{{{ msg.author }}}}</strong> 
                    <span style="color: #999; font-size: 0.8em; margin-left: 10px;">{{{{ msg.time }}}}</span>
                </div>
                <p style="margin: 0; line-height: 1.5;">{{{{ msg.content }}}}</p>
            </div>
        {{% else %}}
            <p style="color: #666;">まだ投稿はありません。</p>
        {{% endfor %}}
    </body>
    </html>
    """
    return render_template_string(html, messages=messages)

@app.route('/post', methods=['POST'])
def post_message():
    author = request.form.get('author')
    passcode = request.form.get('passcode')
    content = request.form.get('content')
    
    # ★暗証番号が合っているかチェック！
    if passcode != SECRET_NUMBER:
        # 番号が違ったらエラーを出して元の画面に戻る
        return redirect(url_for('index', error=1))
    
    if author and content:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        messages.insert(0, {'author': author, 'content': content, 'time': now})
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    # 同じWi-Fiの友達からも入れる設定
    app.run(host='0.0.0.0', port=5000, debug=True)
