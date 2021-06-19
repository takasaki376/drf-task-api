from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
# モデルとシリアライザー
from .models import Task
from .serializers  import TaskSerializer

TASK_URL = '/api/task/'

def create_task(**params):
    # 登録するデータのうち、固定値
    defaults = {
        'task': "dummy-task",
    }
    # パラメータを登録するデータに追加する
    defaults.update(params)

    return Task.objects.create(**defaults)

# キーを含むURLを作成する　（reverseはURLのパスを生成する）
def detail_url(task_id):
    return reverse('task-detail', args=[task_id])

## ==================================================================
## テスト毎の記述
##  各テストケースは「def test_」で始まる名前で定義する
## ==================================================================
class TaskApiTests(TestCase):

    # 今回は必要ないが、認証が必要なテストの場合は、記述する。
    def setUp(self):
        # 認証用のユーザ作成
        self.user = get_user_model().objects.create_user(username='dummy', password='dummy_pw123')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    # **************************************************************
    # テストケース１ GETメソッドでデータが取得できる事を確認する。
    def test_1_should_get_all_tast(self):
        # タスク登録（１件目）
        create_task()
        payload = {
            'task': "dummy2",
        }
        # タスク登録(２件目)
        create_task(**payload)
        # 登録後は登録件数が２件ある事を確認する。
        self.assertEqual(2, Task.objects.count())
        # GETメソッド実行
        res = self.client.get(TASK_URL)
        # 全データを取得する
        task_all = Task.objects.all().order_by('id')
        # task_allをシリアライザーを通した後のデータにする。（many=Trueは複数レコードの場合に指定する）
        serializer = TaskSerializer(task_all, many=True)
        # GETメソッドの結果が成功した事を確認する（HTTPステータスが200が返ってくる事を確認する）
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # 取得結果とセグメントのデータが一致するか確認する
        self.assertEqual(res.data, serializer.data)
        # 検索結果が２件ある事を確認する
        self.assertEqual(2, len(res.data))


    # **************************************************************
    # テストケース２ プライマリキーで取得する
    def test_2_should_get_single_task(self):
        # タスク登録（１件目）
        task = create_task()
        payload = {
            'task': "dummy2",
        }
        # タスク登録(２件目)
        create_task(**payload)
        # 登録後は登録件数が２件ある事を確認する。
        self.assertEqual(2, Task.objects.count())
        # データ取得用のURLを設定する
        url = detail_url(task.id)
        # task_allをシリアライザーを通した後のデータにする。
        serializer = TaskSerializer(task)
        # GETメソッド実行
        res = self.client.get(url)
        # GETメソッドの結果が成功した事を確認する（HTTPステータスが200が返ってくる事を確認する）
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # GETメソッドの取得結果と登録したデータが一致するか確認する
        self.assertEqual(serializer.data, res.data)


    # **************************************************************
    #テストケース３ 新規登録できる事を確認する
    def test_3_should_create_new_task_successfully(self):
        payload = {
            'task': "dummy2",
        }
        # POSTメソッド実行
        res = self.client.post(TASK_URL, payload)
        # POSTメソッドの結果が成功した事を確認する（HTTPステータスが201が返ってくる事を確認する）
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # データベースから名前で検索し、exists()を指定する事で存在している場合はTrueとなる
        exists = Task.objects.filter(
            task=payload['task']
        ).exists()
        # データが存在している場合はexistsにTrueが設定されているため、Trueだと正常
        self.assertTrue(exists)

    # **************************************************************
    #テストケース４ taskが空白の場合はエラーになる事を確認する
    def test_4_should_not_create_new_task_with_invalid(self):
        payload = {
            'task': "",
        }
        # POSTメソッド実行
        res = self.client.post(TASK_URL, payload)
        # POSTメソッドの結果がエラーになる事を確認する。（HTTPステータスが400が返ってくる事を確認する）
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # **************************************************************
    #テストケース５ PUTで更新できる事を確認する
    def test_5_should_allowed_by_PUT(self):
        # タスク登録
        task = create_task()
        # 更新用データ
        payload = {
            'task': "dummy2",
        }
        # データ取得用のURLを設定する
        url = detail_url(task.id)
        # PUTメソッド実行
        res = self.client.put(url, payload)
        # PUTメソッドの結果から正常に更新された事を確認する（HTTPステータスが200が返ってくる事を確認する）
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # 更新後のデータベースの内容を取得する
        task.refresh_from_db()
        # taskの値が変わっている事を確認する
        self.assertEqual(task.task, payload['task'])

    # **************************************************************
    # テストケース６ PATCHで更新できる事を確認する
    def test_6_should_allowed_by_PATCH(self):
        # タスク登録
        task = create_task()
        # 更新用データ
        payload = {
            'task': "dummy2",
        }
        # データ取得用のURLを設定する
        url = detail_url(task.id)
        # PUTメソッド実行
        res = self.client.patch(url, payload)
        # PUTメソッドの結果から正常に更新された事を確認する（HTTPステータスが200が返ってくる事を確認する）
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # 更新後のデータベースの内容を取得する
        task.refresh_from_db()
        # taskの値が変わっている事を確認する
        self.assertEqual(task.task, payload['task'])

    # **************************************************************
    # テストケース７ deleteで削除できる事を確認する
    def test_7_should_delete_task(self):
        # タスク登録
        task = create_task()
        # 削除前は登録件数が１件ある事を確認する。
        self.assertEqual(1, Task.objects.count())
        # URL生成する
        url = detail_url(task.id)
        # DELETEメソッド実行
        self.client.delete(url)
        # 削除後は登録件数が０件となっている事を確認する、
        self.assertEqual(0, Task.objects.count())