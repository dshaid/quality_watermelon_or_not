# -*- coding: utf-8 -*-
from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
from watermelon import app, db
from watermelon.models import User
from watermelon.models import History
from watermelon.watermelon import pre


@app.route('/', methods=['GET', 'POST'])
def index():
    histories = History.query.all()
    return render_template('index.html', histories=histories)

# 修改用户名
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('更新用户名成功！')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()

        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('登录成功！')
            return redirect(url_for('index'))

        flash('账号或密码错误')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))


@app.route('/watermelon', methods=['POST', 'GET'])
@login_required
def watermelon():
    if request.method == 'POST':

        labels = ["color", 'gendi', 'voice', 'wenli', 'qibu', 'feeling']
        list_data = [['0' for i in range(6)]]
        list = []

        # 从表单获取到瓜的6个特征 加入到列表（一维）
        for label in labels:
            value = request.form[label]
            list.append(value)

        # 把一维特征列表转化成二维列表
        for index in range(6):
            list_data[0][index] = list[index]

        # 预测分析
        result = pre(list_data)  # 注意这里返回的是一个 Numpy 格式数组

        if result[0] == '是':
            quality = '好瓜😀😀'
            history = History(quality=quality)
            db.session.add(history)
            db.session.commit()

            flash('😀😀哇哦~ 恭喜您！')
            flash('👍👍您选择的瓜极大可能是一个好瓜！')
        elif result[0] == '否':
            quality = '坏瓜😥😥'
            history = History(quality=quality)
            db.session.add(history)
            db.session.commit()

            flash('😥😥根据您选择的瓜分析')
            flash('😥😥这可能是一个坏瓜~ ')
        return redirect(url_for('watermelon'))
    return render_template('watermelon.html')


# 删除西瓜查询记录
@app.route('/watermelon/delete/<int:history_id>', methods=['POST'])
@login_required
def delete_watermelon(history_id):
    history = History.query.get_or_404(history_id)
    db.session.delete(history)
    db.session.commit()
    flash('记录已删除！')
    return redirect(url_for('index'))