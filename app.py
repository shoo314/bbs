from flask import Flask, request, redirect, url_for, render_template_string
from datetime import datetime

app = Flask(__name__)

# ★設定: ここで暗証番号を変更できます（例: '1234'）
SECRET_NUMBER = "1234"

messages = []

@app.route('/')
def index():
    # 失敗時のエラーメッセージがあれば取得
    error = request.args.get('error')
    
    html = f"""
    <html>
    <head><title>鍵付き掲示板</title></head>
    <body style="font-family: sans-serif; background-color: #f9f9f9; padding: 20px; max-width: 600px; margin: 0 auto;">
        <h1 style="color: #333;">🔒 仲間限定掲示板</h1>
        
        {"<p style='color: red; font-weight: bold;'>⚠️ 暗証番号が違います！</p>" if error else ""}
        
        <div style="background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px;">
            <form action="/post" method="POST" style="margin: 0;">
                <label style="font-weight: bold;">名前:</label><br>
                <input type="text" name="author" required style="width: 100%; padding: 8px; margin: 5px 0 10px 0; box-sizing: border-box;"><br>
                
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
