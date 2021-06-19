
## 環境設定
python3.8 で仮想環境を作る。

設定からpython仮想環境を選択する  
- Windows  
  ファイル  
　　→　設定  
　　　→　プロジェクト  
　　　　→　pythonインタープリター    
- mac  
　PyCharm  
　　→　Preferenced...  
　　　→　プロジェクト  
　　　　→　pythonインタープリター  

## ライブラリインストール (仮想環境)
pip install Django==3.1.7   
pip install djangorestframework==3.12.2   
pip install django-cors-headers==3.7.0  
※バージョン指定しているが、

## プロジェクト作成
django-admin startproject task .

## アプリケーション作成（複数作成可）
django-admin startapp api


## setting.py の編集
動作するサーバ設定
```
ALLOWED_HOSTS = ['127.0.0.1']
```

INSTALLED_APPS に追加  
```
    'rest_framework',  
    'api.apps.ApiConfig',  
    'corsheaders',
```
MIDDLEWARE に追加
```
    'corsheaders.middleware.CorsMiddleware',  
```
フロントエンドのURLを定義する行を追加
ここで設定されたURLからのみアクセス可能になり、他のURLの場合はエラーになる。
```
CORS_ORIGIN_WHITELIST = ['http://localhost:3000']
```

###今回やっていないけど、サーバデプロイするならやること  
　次の値を環境変数（.env）にもたせる  
　SECRET_KEY：githubに公開しないため  
　DEBUG：ローカルとサーバで設定値を変更するため  
　ALLOWED_HOSTS：ローカルとサーバで設定値を変更するため
　CORS_ORIGIN_WHITELIST：ローカルとサーバで設定値を変更するため
　DATABASES：ローカルとサーバで設定値を変更するため  



## 開発サーバ起動
manage.py 右クリック  
    →　Modify Run Configuratiosn... (Macは実行構成の変更)  
        パラメーター欄に`runserver`と入力して、OKボタン
        
## モデルの定義

アプリケーションのフォルダ内にある models.py にモデルの定義を行う。
今回はTaskを作成する

## データベース作成用の定義ファイルを作成する。
python manage.py makemigrations

## データベース作成
python manage.py migrate

## 管理者ユーザ作成
python manage.py createsuperuser

```
Username (leave blank to use 'takas'): ＜ユーザ名を入力する＞
Email address:＜空白のままEnterキー＞
Password:＜パスワードを入力する（１回目）＞
Password (again):＜パスワードを入力する（確認用に２回目）＞
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: y　（簡単なパスワードの場合はこのまま進めてもよいか確認メッセージが表示されるため、yと入力してEnter）
Superuser created successfully.
```

## 管理ツール用設定

models.py で定義した内容を管理ツールから操作できるようにする。  
アプリケーションのフォルダ内にある admin.py にモデルの定義を行う。

## 開発サーバ起動する

下記のURLにアクセスする  
http://127.0.0.1:8000/admin/

テスト用にデータの追加、更新ができればＯＫ

## シリアライザー作成

アプリケーションのフォルダ内に新規にファイルを作成し、ファイル名をserializers.pyとする。  
REST API の定義を記述する。

今回はmodelを元に作成するため、ModelSerializerを継承する。

## ビュー作成

アプリケーションのフォルダ内にある views.py にビューの定義を行う。

今回はmodelを元に作成するため、ModelViewSetを継承する。

## URL設定

### 全体のURLに対して、アプリケーションの定義を行う。

プロジェクトフォルダ内のurls.pyに対して、アプリケーションフォルダを参照するように定義する。

### アプリケーション名に対して、ビューの定義を行う。

アプリケーションのフォルダ内に新規にファイルを作成し、ファイル名をurls.pyとする。

## 動作確認
http://127.0.0.1:8000/api/task/  
　GETメソッド：リスト表示されること  
　POSTメソッド：新規登録されること  
http://127.0.0.1:8000/api/task/[pk]/  
  ※pkは各データのidの値  
　GETメソッド：該当データが１件表示されること  
　PUTメソッド；更新されること  
　PATCHメソッド：指定した項目のみ更新されること  
　DELETEメソッド：削除されること  

# 自動テスト

プロジェクトフォルダ内のtest.pyに対して、テストスクリプトを記述する。  
ファイル名はtestで始まれば複数ファイル存在していても可  

ターミナルからと入力すると、テストパターン１件ずつの結果が確認できる。  
エラーが発生した際は、エラーの内容も確認可能  
`python manage.py test -v2`

下記のコマンドだと、テスト結果が表示される  
`python manage.py test`