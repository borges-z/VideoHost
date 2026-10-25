from app import app, db, bcrypt
from .modelos import Usuarios
from flask import session, redirect, url_for, render_template, flash, abort, send_from_directory
from app.services import user_service, app_services, video_service
from .forms import registro_form, login_form, upload_form
from werkzeug.utils import secure_filename

def login_required(func):
    def teste():
        if "id_usuario" not in session:
            return redirect(url_for('login'))
    return teste

@login_required
@app.route("/")
def home():
    id = session.get("id_usuario", None)
    user = user_service.get_user(id)
    if user:
        return render_template('home.html', user=user)
    return redirect(url_for('login'))

@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = registro_form.RegistroForm()
    if form.validate_on_submit():
        nome = form.nome.data
        email = form.email.data
        senha = bcrypt.generate_password_hash(form.senha.data).decode('utf-8') 
        if user_service.registrar_usuario(nome, email, senha):
            flash("registro feito com sucesso")
            return redirect(url_for('login'))
        flash("Ocorreu um erro ao fazer o seu cadastro!")
    return render_template("registro.html", form=form)

@login_required
@app.route('/uploads')
def meus_uploads():
    videos = video_service.obter_todos_videos_usuario(session["id_usuario"])
    return render_template('meus_videos.html', videos=videos)

@app.route("/login/", methods=["GET", "POST"])
def login():
    form = login_form.LoginForm()
    if form.validate_on_submit():
        user = user_service.get_user_email(form.email.data)
        if not user:
            return abort(500)
        session["id_usuario"] = user.id
        return redirect(url_for('home'))
    return render_template("login.html", form=form)

@login_required
@app.route("/upload", methods=['GET', 'POST'])
def upload():
    form = upload_form.VideoForm()
    if form.validate_on_submit():
        string = app_services.gerar_string_aleatoria()
        video_service.salvar_video(form.video.data, string, secure_filename(form.video.data.filename))
        tamanho = video_service.tamanho_video(form.video.data)
        video_service.registrar_video(form.titulo.data, string, tamanho, session['id_usuario'])
        flash("Video Salvo")
        return redirect(url_for("meus_uploads"))
    return render_template("upload.html", form=form)

@app.route("/stream/<string:cod>/<string:arquivo>")
def partes(cod, arquivo):
    parte = video_service.verificar_arquivo(cod, arquivo)
    if not parte:
        return abort(404)
    return send_from_directory(parte, arquivo)

@app.route("/stream/<string:cod>/playlist.m3u8")
def stream(cod):
    video = video_service.buscar_video(cod)
    if not video:
        return abort(404)
    print(video)
    return send_from_directory(video, "index.m3u8")

@login_required
@app.route("/logout")
def logout():
    session.pop("id_usuario", None)
    return redirect(url_for('login'))

@app.errorhandler(500)
def internal_server_error(erro):
    return render_template("500.html"), 500