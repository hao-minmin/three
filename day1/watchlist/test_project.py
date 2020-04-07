import unittest   

from blog import app,db
from blog.models import User,Movie

class ProjectTestCase(unittest.TestCase):
    #测试固件 两个不同的函数

    def setUp(self):
        #调用app

        app.config.update(
            #处于测试环境
            TESTING=True,
            #用缓存数据库  memory 内存数据库
            SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

        )

        # 往库中

        db.create_all()
        user = User(name="Test",username="test")
        user.set_password("123456")

        movie = Movie(title="Test Movie Title",year="2020")
        #add一条上传  add_all 多条列表上传
        db.session.add_all([user,movie])

        db.session.commit()
        
        # 创建一个测试用的客户端模拟 浏览器  
        self.client = app.test_client()

        #创建测试命令运行器
        self.runner = app.test_cli_runner()

    def testDown(self):
        #数据库清除

        db.session.remove()
        db.drop_all()

    def test_app_exist(self):
        #测试app是不是空的

        self.assertIsNotNone(app)
        
    #测试是否处于测试模式
    def test_app_is_testing(self):
        self.assertTrue(app.config["TESTING"])

    #测试404页面是否存在
    def test_404_page(self):
        #通过找页面特征来判断
        response = self.client.get('/hhh')  #传入一个不存在的url 

        data= response.get_data(as_text=True)

        self.assertIn("页面跑丢了 ~~ 404",data)

        self.assertIn("返回首页",data)

        #状态码 
        self.assertEqual(response.status_code,404)
#测试主页
    def test_index_page(self):
        response = self.client.get('/')
        data=  response.get_data(as_text=True)

        self.assertIn("Test's watchlist",data)
        self.assertIn('Test Movie Title',data)

        self.assertEqual(response.status_code,200)

#测试登录登出  增删改查 测试命令运行器

if __name__=="__main__":
    unittest.main()



















